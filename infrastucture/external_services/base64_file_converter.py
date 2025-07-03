from typing import List
from fastapi import UploadFile
import base64

class FileBase64Converter:
    @staticmethod
    async def files_to_base64(files: List[UploadFile]) -> List[str]:
        base64_list = []
        for file in files:
            content = await file.read()
            base64_str = base64.b64encode(content).decode('utf-8')
            base64_list.append(base64_str)
        return base64_list 