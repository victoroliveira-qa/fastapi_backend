from types import SimpleNamespace

import pytest


BASE_URL = "/api/v1/usuarios"


def test_get_usuario_logado_deve_retornar_usuario_autenticado(client):
    response = client.get(f"{BASE_URL}/logado")

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "victor@email.com"
    assert "senha" not in body


def test_get_usuarios_deve_retornar_lista(client_with_db_result):
    usuario = SimpleNamespace(
        id=1,
        nome="Victor",
        sobrenome="Oliveira",
        email="victor@email.com",
        senha="hash_fake",
        eh_admin=True,
        artigos=[],
    )
    client, _ = client_with_db_result([usuario])

    response = client.get(f"{BASE_URL}/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["email"] == "victor@email.com"


def test_get_usuario_por_id_deve_retornar_200_quando_existir(client_with_db_result):
    usuario = SimpleNamespace(
        id=1,
        nome="Victor",
        sobrenome="Oliveira",
        email="victor@email.com",
        senha="hash_fake",
        eh_admin=False,
        artigos=[],
    )
    client, _ = client_with_db_result(usuario)

    response = client.get(f"{BASE_URL}/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_usuario_por_id_deve_retornar_404_quando_nao_existir(client_with_db_result):
    client, _ = client_with_db_result(None)

    response = client.get(f"{BASE_URL}/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado."


def test_signup_deve_criar_usuario(client):
    payload = {
        "nome": "Maria",
        "sobrenome": "Silva",
        "email": "maria@email.com",
        "senha": "123456",
        "eh_admin": False,
    }

    response = client.post(f"{BASE_URL}/signup", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "maria@email.com"
    assert "senha" not in body


def test_put_usuario_deve_atualizar_quando_existir(client_with_db_result):
    usuario = SimpleNamespace(
        id=1,
        nome="Victor",
        sobrenome="Oliveira",
        email="victor@email.com",
        senha="hash_fake",
        eh_admin=False,
        artigos=[],
    )
    client, fake_db = client_with_db_result(usuario)

    response = client.put(
        f"{BASE_URL}/1",
        json={
            "id": 1,
            "nome": "Victor Atualizado",
            "sobrenome": "Oliveira",
            "email": "victor@email.com",
            "eh_admin": False,
            "senha": "nova_senha",
        },
    )

    assert response.status_code == 202
    assert response.json()["nome"] == "Victor Atualizado"
    assert fake_db.committed is True


def test_delete_usuario_deve_retornar_204_quando_existir(client_with_db_result):
    usuario = SimpleNamespace(
        id=1,
        nome="Victor",
        sobrenome="Oliveira",
        email="victor@email.com",
        senha="hash_fake",
        eh_admin=False,
        artigos=[],
    )
    client, fake_db = client_with_db_result(usuario)

    response = client.delete(f"{BASE_URL}/1")

    assert response.status_code == 204
    assert len(fake_db.deleted) == 1
