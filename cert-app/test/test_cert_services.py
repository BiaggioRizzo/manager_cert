from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_sucess_get_certificate_information():
    response = client.get("/certificado/v1/informacao/www.medium.com")
    key_word = "'nome': 'medium.com'"
    assert response.status_code == 200, f'HTTP STATUS INVÁLIDO'
    assert key_word in str(response.json())


def test_err_invalid_endpoint_get_certificate_information():
    response = client.get("/certificado/v1/informacao/1234")
    print(response.json())
    key_word = "{'detail': 'Requisição Inválida'}"
    assert response.status_code == 400
    assert key_word in str(response.json())