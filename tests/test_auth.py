from types import SimpleNamespace

import pytest

from api.V1.endpoints import usuario as usuario_endpoint


BASE_URL = "/api/v1/usuarios"


@pytest.mark.parametrize("email, senha", [("admin@email.com", "123456")])
def test_login_deve_retornar_token_quando_credenciais_validas(client, monkeypatch, email, senha):
    async def autenticar_fake(email: str, senha: str, db):
        return SimpleNamespace(id=1, email=email)

    def criar_token_fake(sub: str):
        return "token_fake"

    monkeypatch.setattr(usuario_endpoint, "autenticar", autenticar_fake)
    monkeypatch.setattr(usuario_endpoint, "criar_token_acesso", criar_token_fake)

    response = client.post(
        f"{BASE_URL}/login",
        data={"username": email, "password": senha},
    )

    assert response.status_code == 200
    assert response.json() == {"access_token": "token_fake", "token_type": "bearer"}


def test_login_deve_retornar_400_quando_credenciais_invalidas(client, monkeypatch):
    async def autenticar_fake(email: str, senha: str, db):
        return None

    monkeypatch.setattr(usuario_endpoint, "autenticar", autenticar_fake)

    response = client.post(
        f"{BASE_URL}/login",
        data={"username": "errado@email.com", "password": "senha_errada"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Dados de acesso incorretos."
