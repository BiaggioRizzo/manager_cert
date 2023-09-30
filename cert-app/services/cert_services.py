import logging
import os
from fastapi.responses import PlainTextResponse, FileResponse
from cryptography.hazmat.primitives import serialization
from fastapi import HTTPException, requests
from datetime import datetime
from OpenSSL import SSL
import exceptions.exceptions as exception
import services.schema as schema
import socket
import re
import requests
import utils.commons as commons


REGEX_PROCURA_CERT_ROOT = (
    r"((?:[NOME_ROOT])(.|\r|\n)*?(?<=-----END CERTIFICATE\-----\n))"
)
REGEX_TRATA_CERT_ROOT = (
    r"(?<=-----BEGIN CERTIFICATE-----)(.|\r|\n)*?(?=-----END CERTIFICATE-----)"
)
ENDPOINT_ROOT_CERT = "https://curl.se/ca/cacert.pem"
CAMINHO_ARQUIVO_CERT_ROOT = "cacert.pem"
PORT = 443


def download_certs_root():
    try:
        response = requests.get(ENDPOINT_ROOT_CERT)

    except Exception as error:
        commons.write_log(logging.ERROR,message={"mensagem":str(error)})
        raise exception.BadGatewayError()
    else:
        try:
            with open(CAMINHO_ARQUIVO_CERT_ROOT, "wb") as arquivo:
                arquivo.write(response.content)
            commons.write_log(message={"mensagem":"Certificado baixado com sucesso"})
        except FileNotFoundError:
            raise exception.InternalServerError()
        else:
            with open("cacert.pem", "r") as file:
                readfile = file.read()

            return readfile


def trata_cert_root(cert_root: str):
    match_cert_regex = re.search(REGEX_TRATA_CERT_ROOT, cert_root)
    content_cert_root = match_cert_regex.group()
    cert_line = []
    final_text = """-----BEGIN CERTIFICATE-----
[TEXTO_CERTIFICADO]
-----END CERTIFICATE-----"""

    current_line = ""
    for caractere in content_cert_root.replace("\n", "").replace(" ", ""):
        current_line += caractere
        if len(current_line) == 64:
            cert_line.append(current_line)
            current_line = ""
    if current_line:
        cert_line.append(current_line)

    cert_line_text = "\n".join(cert_line)
    final_text = final_text.replace("[TEXTO_CERTIFICADO]", cert_line_text)

    return final_text


def create_conection_ssl(host: str):
    ssl_conn = None

    try:
        socket_connection = socket.create_connection((host, PORT))
        context = SSL.Context(SSL.SSLv23_METHOD)

        # Criar conexão SSL
        ssl_conn = SSL.Connection(context, socket_connection)
        ssl_conn.set_connect_state()
        ssl_conn.set_tlsext_host_name(host.encode("utf-8"))
        # Realizar o handshake SSL/TLS
        ssl_conn.do_handshake()
    except:
        commons.write_log(logging.ERROR,message={"mensagem":"Sem conexão estabelecida"})
        raise exception.BadRequestError()
    else:
        commons.write_log(logging.DEBUG,message={"mensagem":"conexão estabelecida"})
        return ssl_conn
    finally:
        if ssl_conn:
            ssl_conn.shutdown()
            ssl_conn.close()


def get_chain_cert(host: str, download: bool = False):
    readfile = download_certs_root()
    certs_cadeia = create_conection_ssl(host).get_peer_cert_chain()
    certificate_chain = []

    for posicao, cert in enumerate(certs_cadeia):
        # print("Certificate #" + str(posicao))
        if posicao <= 1:
            certificate_pem = cert.to_cryptography().public_bytes(
                serialization.Encoding.PEM
            )
            certificate_chain.insert(0, certificate_pem.decode().strip("\n"))

            # for component in cert.get_subject().get_components():
            #     print("Subject %s: %s" % (component))
            # print("issuer:" + str(cert.get_issuer().get_components()[-1][-1]))
            root_cert_name = str(
                cert.get_issuer().get_components()[-1][-1].decode())

            if root_cert_name in readfile:
                regex_extrai_cert_root = REGEX_PROCURA_CERT_ROOT.replace(
                    "[NOME_ROOT]", root_cert_name
                )
                match_cert_regex = re.search(regex_extrai_cert_root, readfile)
                root_certificate = trata_cert_root(
                    match_cert_regex.group().split("=")[-1].strip("\n")
                )
                certificate_chain.insert(0, root_certificate)
                commons.write_log(logging.DEBUG,message={"mensagem":"cert encontrado"})
            else:
                commons.write_log(logging.DEBUG,message={"mensagem":"cert não encontrado"})

    consolidate_response = "\n".join(certificate_chain)
    if os.path.isfile(CAMINHO_ARQUIVO_CERT_ROOT):
        os.remove(CAMINHO_ARQUIVO_CERT_ROOT)
        commons.write_log(logging.INFO,message={f"mensagem":"O arquivo {CAMINHO_ARQUIVO_CERT_ROOT} foi excluído com sucesso."})
    else:
        commons.write_log(logging.INFO,message={f"mensagem":"O arquivo {CAMINHO_ARQUIVO_CERT_ROOT} não existe."})


    if download == True:
        print("chegou aquiiii")
        with open(f"certificate_todos.pem", "w") as pem_file:
            pem_file.write(consolidate_response)

        file_path = "certificate_todos.pem"
        return FileResponse(file_path, filename="arquivo.pem")
    else:
        return PlainTextResponse(consolidate_response)


def get_certificate_information(host: str):
    cert = create_conection_ssl(host).get_peer_certificate()

    host_name = cert.get_subject().get_components()[-1][-1]
    not_before = datetime.strptime(
        cert.get_notBefore().decode("utf-8"), "%Y%m%d%H%M%SZ")
    not_after = datetime.strptime(
        cert.get_notAfter().decode("utf-8"), "%Y%m%d%H%M%SZ")
    issuer = str(cert.get_issuer().get_components()[-1][-1].decode())
    # print("version:" + str(cert.get_version()))
    # print("sigAlg:" + cert.get_signature_algorithm().decode("utf-8"))
    # print("digest:" + cert.digest('sha256').decode("utf-8"))
    serial_number = "0" + str(hex(cert.get_serial_number()))[2:].upper()
    formatted_serial = ":".join(
        serial_number[i: i + 2] for i in range(0, len(serial_number), 2))
    try:
        response = schema.CertificateBaseResponse(
            nome=host_name,
            numeroSerie=formatted_serial,
            emissor=issuer,
            validoNaoAntes=not_before.strftime("%d/%m/%Y"),
            validoNaoDepois=not_after.strftime("%d/%m/%Y"),
        )
        print(type(response))
    except Exception as error:
        commons.write_log(logging.ERROR,message={"mensagem":str(error)})
        exception.BadGatewayError()

    return response
