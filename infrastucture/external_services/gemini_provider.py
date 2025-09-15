import asyncio
import os
from typing import Optional, AsyncGenerator
from google import genai
from google.genai import types


class GeminiProvider:
    def __init__(self):
        # Get API key from environment variable
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        self.client = genai.Client(api_key=self.api_key)
    
    async def chat(self, model: str, prompt: str, system_prompt: Optional[str] = None, streaming: bool = False) -> str:
        if streaming:
            return await self._chat_streaming(model, prompt, system_prompt)
        else:
            return await self._chat_sync(model, prompt, system_prompt)
    
    async def _chat_streaming(self, model: str, prompt: str, system_prompt: Optional[str] = None) -> str:
        def sync_streaming():
            result = ""
            config = None
            
            # Configure system instruction if provided
            if system_prompt:
                config = types.GenerateContentConfig(
                    system_instruction=system_prompt
                )
            
            # Generate content with streaming
            for chunk in self.client.models.generate_content_stream(
                model=model,
                contents=prompt,
                config=config
            ):
                if hasattr(chunk, 'text') and chunk.text:
                    result += chunk.text
            return result
        
        return await asyncio.to_thread(sync_streaming)
    
    async def _chat_sync(self, model: str, prompt: str, system_prompt: Optional[str] = None) -> str:
        def sync_chat():
            config = None
            
            # Configure system instruction if provided
            if system_prompt:
                config = types.GenerateContentConfig(
                    system_instruction=system_prompt
                )
            
            response = self.client.models.generate_content(
                model=model,
                contents=prompt,
                config=config
            )
            
            # Extract text from response
            if hasattr(response, 'text') and response.text:
                return response.text
            elif hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        return candidate.content.parts[0].text
            
            return str(response)
        
        return await asyncio.to_thread(sync_chat)
    
    async def chat_stream(self, model: str, prompt: str, system_prompt: Optional[str] = None) -> AsyncGenerator[str, None]:
        """
        Genera contenido en streaming, produciendo chunks de texto en tiempo real
        
        Args:
            model: Modelo a usar
            prompt: Prompt del usuario
            system_prompt: Prompt del sistema (opcional)
            
        Yields:
            Chunks de texto conforme se generan
        """
        import queue
        import threading
        
        # Cola para pasar chunks del hilo sincrónico al async
        chunk_queue = asyncio.Queue()
        exception_holder = [None]
        
        def sync_streaming():
            try:
                config = None
                
                # Configure system instruction if provided
                if system_prompt:
                    config = types.GenerateContentConfig(
                        system_instruction=system_prompt
                    )
                
                # Generate content with streaming
                for chunk in self.client.models.generate_content_stream(
                    model=model,
                    contents=prompt,
                    config=config
                ):
                    if hasattr(chunk, 'text') and chunk.text:
                        # Poner chunk en la cola de manera thread-safe
                        asyncio.run_coroutine_threadsafe(
                            chunk_queue.put(chunk.text), 
                            asyncio.get_event_loop()
                        )
                
                # Señal de que terminó
                asyncio.run_coroutine_threadsafe(
                    chunk_queue.put(None), 
                    asyncio.get_event_loop()
                )
                
            except Exception as e:
                exception_holder[0] = e
                asyncio.run_coroutine_threadsafe(
                    chunk_queue.put(None), 
                    asyncio.get_event_loop()
                )
        
        # Ejecutar streaming en un hilo separado
        thread = threading.Thread(target=sync_streaming)
        thread.start()
        
        try:
            # Yield chunks conforme llegan
            while True:
                chunk = await chunk_queue.get()
                if chunk is None:  # Señal de finalización
                    break
                if exception_holder[0]:
                    raise exception_holder[0]
                yield chunk
        finally:
            thread.join()