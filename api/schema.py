from pydantic import BaseModel

class PumpModeRequest(BaseModel):
    mode : int

class PLCResponse(BaseModel):
    device_id : int
    name : str

    level : int
    pump : int
    pump_mode : int
    pump_manual : int