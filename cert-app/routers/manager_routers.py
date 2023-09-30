import uuid
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse, PlainTextResponse
import services.schema as schema
import services.cert_services as service_cert
import utils.commons as commons
import logging
import utils.functions_redis as cache_redis
import json

shared_variables = { 
    "requestId":None,
    "consumidor": "desconhecido"    
}

def header_validation(requestId = None, consumidor = None):
    if consumidor:
        shared_variables["consumidor"] = consumidor
    
    if(requestId or requestId is None):
        if len(str(requestId)) == 0 or requestId is None:
            shared_variables["requestId"] = uuid.uuid4()
        else:
            shared_variables["requestId"] = requestId
         
        

router = APIRouter(prefix="/certificado")


@router.get("/v1/cadeia/{url_website}")
async def cadeia_certificado(url_website:str, download:bool = False):
    header_validation()
    response = None
    commons.write_log(level=logging.DEBUG,message={"mensagem":"Inicio operacao", "requestId":shared_variables["requestId"] })
    cache = cache_redis.connection_redis()
    retorno_cache = cache.get(url_website)
    
    if retorno_cache and download == False:
        response = retorno_cache
        return PlainTextResponse(response)
    
    if not retorno_cache :
        cert = service_cert.get_chain_cert(host=url_website, download=download)
        if download == False:
        # Converta cert para string, se necessário
            cert_str = cert.decode('utf-8') if isinstance(cert, bytes) else cert
            cache.set(url_website, str(cert_str))
        else:
            response = cert
            print(type(response))
  
    commons.write_log(level=logging.DEBUG,message={"mensagem":"Fim operacao"})
    return response


@router.get("/v1/informacao/{url_website}", response_model=schema.CertificateBaseResponse)
async def informacao_certificado_base(url_website):
        header_validation()
        response = None
        
        commons.write_log(message={"mensagem":"Inicio operacao","requestId":shared_variables["requestId"]})
        
        cache = cache_redis.connection_redis()
        retorno_cache = cache.get(url_website)

        if not retorno_cache:
            response_information = service_cert.get_certificate_information(url_website)
            cache.set(url_website, json.dumps(response_information.dict())) # usando string array / json
            
        if retorno_cache:
            response = json.loads(retorno_cache) 
        else:
            response = response_information
            
        commons.write_log(message={"mensagem":"Fim operacao"})
        return response
    


