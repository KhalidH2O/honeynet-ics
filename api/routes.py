from fastapi import APIRouter

from services.PLC_service import PLCService
from api.schema import PumpModeRequest, PLCResponse

router = APIRouter()

service = PLCService()
service.connect()

@router.get("/")
def home():
    return {
        "message" : "Honeynet-ICS API"
    }

@router.get("/plcs")
def get_plcs():
    return service.read_all()

@router.get("/plcs/{device_id}")
def get_plcs(device_id:int, response : PLCResponse):
    plcs = service.read(device_id)
    

@router.post("/{device_id}/mode")
def set_mode(device_id : int, request : PumpModeRequest):
    service.set_mode(device_id, request.mode)
    return {
        "message" : "Pump mode updated"
    }