from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated


class LightModel(BaseModel):
    id: str
    name: str
    room: str
    is_on: bool
    brightness: int = Field(ge=0, le=100)
    color: Annotated[str, StringConstraints(pattern=r'^#[0-9A-Fa-f]{6}$')]


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


class BrightnessUpdateRequest(BaseModel):
    brightness: int = Field(ge= 0, le=100)


class ColorUpdateRequest(BaseModel):
    color: Annotated[str, StringConstraints(pattern=r'^#[0-9A-Fa-f]{6}$')]


class RoomModel(BaseModel):
    name: str
    light_count: int


class RoomsListResponse(BaseModel):
    mode: str
    items: list[RoomModel]


class BridgeStatusResponse(BaseModel):
    mode: str
    bridge_configured: bool
    bridge_reachable: bool


class BulkLightActionRequest(BaseModel):
    light_ids: Annotated[list[str], Field(min_length=1)]


class BulkLightActionResponse(BaseModel):
    success: bool
    message: str
    updated_lights: list[LightModel]
    missing_light_ids: list[str]
