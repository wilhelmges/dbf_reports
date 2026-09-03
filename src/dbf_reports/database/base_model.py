from sqlmodel import SQLModel


class BaseModel(SQLModel):
    @classmethod
    def key_fields(cls) -> tuple[str, ...]:
        raise NotImplementedError