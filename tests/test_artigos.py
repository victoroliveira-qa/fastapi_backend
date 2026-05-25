from types import SimpleNamespace

BASE_URL = "/api/v1/artigos"

def artigo_payload():
    return {
        "titulo": "FastAPI na prática",
        "descricao": "Criando APIs modernas com Python",
        "url_fonte": "https://example.com/fastapi",
        "usuario_id": 1,
    }


def test_post_artigo_deve_criar_artigo_autenticado(client, fake_session):
    response = client.post(f"{BASE_URL}/", json=artigo_payload())

    assert response.status_code == 201
    body = response.json()
    assert body["titulo"] == "FastAPI na prática"
    assert body["usuario_id"] == 1
    assert fake_session.committed is True


def test_get_artigos_deve_retornar_lista(client_with_db_result):
    artigo = SimpleNamespace(
        id=1,
        titulo="Artigo sobre FastAPI",
        descricao="Introdução prática ao FastAPI",
        url_fonte="https://example.com/artigo",
        usuario_id=1,
    )
    client, _ = client_with_db_result([artigo])

    response = client.get(f"{BASE_URL}/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["titulo"] == "Artigo sobre FastAPI"


def test_get_artigo_por_id_deve_retornar_200_quando_existir(client_with_db_result):
    artigo = SimpleNamespace(
        id=1,
        titulo="Artigo sobre FastAPI",
        descricao="Introdução prática ao FastAPI",
        url_fonte="https://example.com/artigo",
        usuario_id=1,
    )
    client, _ = client_with_db_result(artigo)

    response = client.get(f"{BASE_URL}/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_artigo_por_id_deve_retornar_404_quando_nao_existir(client_with_db_result):
    client, _ = client_with_db_result(None)

    response = client.get(f"{BASE_URL}/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Artigo não encontrado"


def test_put_artigo_deve_atualizar_quando_existir(client_with_db_result):
    artigo = SimpleNamespace(
        id=1,
        titulo="Título antigo",
        descricao="Descrição antiga",
        url_fonte="https://example.com/antigo",
        usuario_id=1,
    )
    client, fake_db = client_with_db_result(artigo)

    response = client.put(f"{BASE_URL}/1", json=artigo_payload())

    assert response.status_code == 202
    assert response.json()["titulo"] == "FastAPI na prática"
    assert fake_db.committed is True


def test_delete_artigo_deve_retornar_204_quando_existir_e_pertencer_ao_usuario(client_with_db_result):
    artigo = SimpleNamespace(
        id=1,
        titulo="Artigo sobre FastAPI",
        descricao="Introdução prática ao FastAPI",
        url_fonte="https://example.com/artigo",
        usuario_id=1,
    )
    client, fake_db = client_with_db_result(artigo)

    response = client.delete(f"{BASE_URL}/1")

    assert response.status_code == 204
    assert len(fake_db.deleted) == 1
