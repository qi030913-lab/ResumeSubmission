from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class HealthResponse(ORMModel):
    status: str
    service: str
    database: str | None = None
