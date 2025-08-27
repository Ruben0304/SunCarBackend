# Auth responses
from .auth_responses import LoginResponse, ChangePasswordResponse

# Brigadas responses
from .brigadas_responses import (
    BrigadaListResponse,
    BrigadaDetailResponse,
    BrigadaCreateResponse,
    BrigadaUpdateResponse,
    BrigadaDeleteResponse,
    BrigadaMemberResponse
)

# Trabajadores responses
from .trabajadores_responses import (
    TrabajadorListResponse,
    TrabajadorDetailResponse,
    TrabajadorCreateResponse,
    TrabajadorUpdateResponse,
    TrabajadorSearchResponse,
    TrabajadorBrigadaResponse
)

# Clientes responses
from .clientes_responses import ClienteCreateResponse, ClienteVerifyResponse, ClienteVerifyByIdentifierResponse

# Productos responses
from .productos_responses import (
    ProductoListResponse,
    CategoriaListResponse,
    MaterialListResponse,
    ProductoCreateResponse,
    CategoriaCreateResponse,
    MaterialAddResponse
)

# Reportes responses
from .reportes_responses import (
    InversionReportResponse,
    AveriaReportResponse,
    MantenimientoReportResponse,
    HoursWorkedResponse
)

# Updates responses
from .updates_responses import UpdateStatusResponse

# Contactos responses
from .contactos_responses import (
    ContactoCreateResponse,
    ContactoUpdateResponse,
    ContactoGetResponse,
    ContactoListResponse,
    ContactoDeleteResponse
)

__all__ = [
    # Auth
    "LoginResponse",
    "ChangePasswordResponse",
    
    # Brigadas
    "BrigadaListResponse",
    "BrigadaDetailResponse",
    "BrigadaCreateResponse",
    "BrigadaUpdateResponse",
    "BrigadaDeleteResponse",
    "BrigadaMemberResponse",
    
    # Trabajadores
    "TrabajadorListResponse",
    "TrabajadorDetailResponse",
    "TrabajadorCreateResponse",
    "TrabajadorUpdateResponse",
    "TrabajadorSearchResponse",
    "TrabajadorBrigadaResponse",
    
    # Clientes
    "ClienteCreateResponse",
    "ClienteVerifyResponse",
    "ClienteVerifyByIdentifierResponse",
    
    # Productos
    "ProductoListResponse",
    "CategoriaListResponse",
    "MaterialListResponse",
    "ProductoCreateResponse",
    "CategoriaCreateResponse",
    "MaterialAddResponse",
    
    # Reportes
    "InversionReportResponse",
    "AveriaReportResponse",
    "MantenimientoReportResponse",
    "HoursWorkedResponse",
    
    # Updates
    "UpdateStatusResponse",
    
    # Contactos
    "ContactoCreateResponse",
    "ContactoUpdateResponse",
    "ContactoGetResponse",
    "ContactoListResponse",
    "ContactoDeleteResponse"
] 