from typing import Optional
from typing import List

from pydantic import BaseModel, EmailStr, Field, field_validator

from schemas.artigo_schema import ArtigoSchema


class UsuarioSchemaBase(BaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr
    eh_admin: bool = False

    class Config:
        orm_mode = True


class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str = Field(
        min_length=6,
        max_length=72,
        description="Senha do usuário. Deve ter entre 6 e 72 caracteres."
    )

    @field_validator("senha")
    @classmethod
    def validar_senha_bcrypt(cls, senha: str) -> str:
        if len(senha.encode("utf-8")) > 72:
            raise ValueError("A senha não pode ultrapassar 72 bytes.")
        return senha


class UsuarioSchemaArtigos(UsuarioSchemaBase):
    artigos: Optional[List[ArtigoSchema]]


class UsuarioSchemaUp(UsuarioSchemaBase):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    eh_admin: Optional[bool]
