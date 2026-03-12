from pydantic import BaseModel, Field


class LightModel(BaseModel):
    id: str
    name: str
    room: str
    is_on: bool
    brightness: int = Field(ge=0, le=100)
    color: str


class LightsListResponse(BaseModel):
    mode: str
    items: list[LightModel]


class HealthResponse(BaseModel):
    status: str
    app: str
    version: str
    mode: str


class LightActionResponse(BaseModel):
    success: bool
    message: str
    light: LightModel


class LightDetailsResponse(BaseModel):
    mode: str
    item: LightModel
