# Modbus Service
from pymodbus.simulator import SimData, SimDevice, DataType
from pymodbus.server import ModbusTcpServer
from pymodbus import FramerType

class PLC:
    def __init__(self, dev_id):
        self.PLC_data = SimData(
            address=0,
            count=4,
            values=[0,0,0,0],
            datatype=DataType.REGISTERS
        )

        # values = [level, auto_pump, pump_mode, manual_pump]

        self.PLC = SimDevice(
            id=dev_id,
            simdata=self.PLC_data
        )

class ModbusServer:
    def __init__(self, devices):
        self._server = ModbusTcpServer(
            context=devices,
            framer=FramerType.SOCKET,        
            address=("0.0.0.0", 5020)
        )

    async def serve(self):
        await self._server.serve_forever()

    async def set_values(self, tank):
        await self._server.async_setValues(
        device_id=tank.dev_id,
        func_code=3,
        address=0,
        values=[tank.level, tank.pump, tank.pump_mode, tank.pump_manual])
        
    async def get_values(self, device_id):
        values = await self._server.async_getValues(
            device_id=device_id,
            func_code=3,
            address=0,
            count=4,
        )

        return values