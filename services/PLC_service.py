import sys
from dataclasses import dataclass

from pymodbus.client.tcp import ModbusTcpClient
from plc.registers import Registers
from pymodbus import exceptions

@dataclass
class PLCStatus:
    id: int
    name: str

    level: int
    pump: int
    pump_mode: int
    pump_manual: int

class PLCService:
    def __init__(self):
        self.client = ModbusTcpClient(
            "localhost", port=5020
        )

        self.devices = {
            1 : "Tank 1",
            2 : "Tank 2",
            3 : "Tank 3"
            }
    
    def connect(self) -> None:
        try:
            self.client.connect()
        except:
            if not self.client.connect():
                raise ConnectionError("Could not connect to PLC server.")

    def disconnect(self) -> None:
        self.client.close()
        print("\nClient disconnected!")
        sys.exit(0)

    def get_plcs(self):
        return self.devices

    def read(self, device_id:int) -> PLCStatus:
        try:
            result = self.client.read_holding_registers(
                address=0,
                count=4,
                device_id=device_id
            )

        except exceptions.ConnectionException as e:
            raise ConnectionError("Connection to PLC server lost.") from e
        
        if result.isError():
            raise RuntimeError(result)
        
        values = result.registers

        return PLCStatus(
            id=device_id,
            name=self.devices[device_id],

            level=values[Registers.LEVEL],
            pump=values[Registers.PUMP],
            pump_mode=values[Registers.PUMP_MODE],
            pump_manual=values[Registers.PUMP_MANUAL]
        )
    
    def read_all(self) -> list[PLCStatus]:
        all_plcs = []

        for plc_id in self.devices:
            all_plcs.append(self.read(plc_id))
        
        return all_plcs
    

    def _write_registers(self, address:int, values:list, device_id:int):
        self.client.write_registers(
            address=address,
            values=values,
            device_id=device_id
        )
    
    def set_mode(self, device_id:int, mode:int):
        self._write_registers(address=Registers.PUMP_MODE,
                   values=[mode],
                   device_id=device_id)
    
    def set_pump_cmd(self, device_id:int, cmd:int):
        self._write_registers(address=Registers.PUMP_MANUAL,
                   values=[cmd],
                   device_id=device_id)