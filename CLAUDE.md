# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server locally
python main.py
# Server starts at http://127.0.0.1:8000

# Alternative with uvicorn directly
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Testing
- HTTP test files are located in `test/` directory (test_brigadas.http, test_main.http)
- Use VS Code REST Client extension or similar tools to execute the HTTP requests

### Deployment
- Application is configured for Vercel deployment via `vercel.json`
- Uses Python 3.9 runtime with 15MB lambda size limit
- Deployed via Vercel's Python runtime (`@vercel/python`)

## Architecture Overview

This is a **Clean Architecture** FastAPI application for SunCar company's backend system. The architecture follows strict separation of concerns across four main layers:

### 1. Domain Layer (`domain/`)
- Contains pure business entities with no external dependencies
- **Entities**: `Cliente`, `Producto`, `Trabajador`, `Brigada`, `Form`, `Update`
- All entities use Pydantic models for validation and serialization

### 2. Application Layer (`application/`)
- **Services**: Business logic coordinators (`client_service.py`, `product_service.py`, `worker_service.py`, `form_service.py`, `auth_service.py`, `update_service.py`, `brigada_service.py`)
- **PDF Use Cases**: Specialized PDF generation logic in `pdfUseCases/` with inheritance pattern using `BasePDFUseCase`

### 3. Infrastructure Layer (`infrastucture/`)
- **Database**: MongoDB connection handling via PyMongo (optimized for Vercel serverless)
- **Repositories**: Data access implementations following repository pattern
- **External Services**: File handling (`base64_file_converter.py`, `supabase_uploader.py`)
- **Dependencies**: Singleton dependency injection pattern in `dependencies.py`

### 4. Presentation Layer (`presentation/`)
- **Routers**: Feature-organized FastAPI routers (`auth_router.py`, `trabajadores_router.py`, `brigadas_router.py`, `clientes_router.py`, `productos_router.py`, `reportes_router.py`, `updates_router.py`, `admin_router.py`, `shared_router.py`, `pdf_router.py`)
- **Schemas**: Request/Response models organized in `requests/` and `responses/` subdirectories
- **Handlers**: Exception handling (`validation_exception_handler.py`)

## Key Technical Patterns

### Dependency Injection
- All services and repositories use singleton instances defined in `infrastucture/dependencies.py`
- FastAPI dependencies follow the pattern: Repository → Service → Router
- Services receive repositories via constructor injection

### Database Connection
- MongoDB connection is optimized for serverless environments (Vercel)
- Uses connection pooling with `maxPoolSize=1` for serverless efficiency
- Connection string from `MONGODB_URL` or `MONGODB_URI` environment variables
- Database name from `DATABASE_NAME` env var (defaults to "defaultdb")
- **Production database name**: `SunCar` (for MCP connections)

### API Organization
All endpoints are prefixed with `/api/` and organized by feature:
- `/api/auth` - Authentication
- `/api/trabajadores` - Workers management
- `/api/brigadas` - Work brigades
- `/api/clientes` - Clients
- `/api/productos` - Products/Materials catalog
- `/api/reportes` - Reports (inversion, averia, mantenimiento)
- `/api/update` - System updates
- `/api/admin` - Admin functions
- `/api/pdf` - PDF generation

### PDF Generation Architecture
- Uses Template Method pattern with `BasePDFUseCase` as base class
- Individual use cases: `GenerarSalariosPruebaUseCase`, `GenerarSalariosRealesUseCase`, `GenerarNominaPagosUseCase`
- PDF templates stored in `pdftemplates/` as HTML files
- Uses xhtml2pdf and Jinja2 for PDF generation

## Environment Variables Required
- `MONGODB_URL` or `MONGODB_URI`: MongoDB connection string
- `DATABASE_NAME`: Database name (optional, defaults to "defaultdb")
- Additional environment variables may be required based on external services (Supabase, etc.)

## Business Domain Context
SunCar is a company that manages:
- **Workers** (`trabajadores`) organized in **Work Brigades** (`brigadas`)
- **Clients** (`clientes`) with locations and service history
- **Products/Materials catalog** with categories and materials
- **Reports** of three types: Investment (`inversion`), Breakdown (`averia`), Maintenance (`mantenimiento`)
- **Time tracking** for worker hours and payroll generation

The system handles form submissions with file attachments, generates PDF reports, and provides comprehensive filtering and querying capabilities for reports and client data.