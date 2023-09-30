from pydantic import BaseModel

class CertificateBaseResponse(BaseModel):
    nome: str
    numeroSerie: str | None = None
    emissor: str
    validoNaoAntes: str 
    validoNaoDepois: str
