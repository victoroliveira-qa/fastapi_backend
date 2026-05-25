from types import SimpleNamespace
from unittest.mock import AsyncMock

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import pytest
from fastapi.testclient import TestClient

from main import app
from core.deps import get_current_user, get_session


class FakeScalarResult:
    def __init__(self, data=None):
        self.data = data

    def unique(self):
        return self

    def all(self):
        if self.data is None:
            return []
        if isinstance(self.data, list):
            return self.data
        return [self.data]

    def one_or_none(self):
        if isinstance(self.data, list):
            return self.data[0] if self.data else None
        return self.data


class FakeExecuteResult:
    def __init__(self, data=None):
        self.data = data

    def scalars(self):
        return FakeScalarResult(self.data)


class FakeAsyncSession:
    """Simula parte do comportamento de uma AsyncSession do SQLAlchemy."""
    def __init__(self, query_result=None):
        self.query_result = query_result
        self.added = []
        self.deleted = []
        self.committed = False
        self.add = AsyncMock(side_effect=self._add_sync)
        self.commit = AsyncMock(side_effect=self._commit_sync)
        self.delete = AsyncMock(side_effect=self._delete_sync)
        self.execute = AsyncMock(return_value=FakeExecuteResult(query_result))

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    def _add_sync(self, obj):
        self.added.append(obj)

    def _commit_sync(self):
        self.committed = True

    def _delete_sync(self, obj):
        self.deleted.append(obj)


@pytest.fixture
def usuario_logado_fake():
    return SimpleNamespace(
        id=1,
        nome="Victor",
        sobrenome="Oliveira",
        email="victor@email.com",
        senha="hash_fake",
        eh_admin=True,
        artigos=[],
    )


@pytest.fixture
def artigo_fake(usuario_logado_fake):
    return SimpleNamespace(
        id=1,
        titulo="Artigo sobre FastAPI",
        descricao="Introdução prática ao FastAPI",
        url_fonte="https://example.com/artigo",
        usuario_id=usuario_logado_fake.id,
    )


@pytest.fixture
def usuario_fake(usuario_logado_fake):
    return usuario_logado_fake


@pytest.fixture
def fake_session():
    return FakeAsyncSession()


@pytest.fixture
def client(usuario_logado_fake, fake_session):
    async def override_get_current_user():
        return usuario_logado_fake

    async def override_get_session():
        yield fake_session

    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def client_with_db_result(usuario_logado_fake):
    def _factory(result):
        fake_db = FakeAsyncSession(query_result=result)

        async def override_get_current_user():
            return usuario_logado_fake

        async def override_get_session():
            yield fake_db

        app.dependency_overrides[get_current_user] = override_get_current_user
        app.dependency_overrides[get_session] = override_get_session

        test_client = TestClient(app)
        return test_client, fake_db

    yield _factory
    app.dependency_overrides.clear()
