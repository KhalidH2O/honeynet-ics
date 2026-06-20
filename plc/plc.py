# #PLC Devices Simulation

from pymodbus.simulator import SimData, SimDevice, DataType
from pymodbus.server import StartTcpServer

import logging

logging.basicConfig(
    level=logging.DEBUG
)

class PLC:
    def __init__(self, dev_id, temperature, pressure, motor):

        self.PLC_data = SimData(
            address=0,
            count=3,
            values=[temperature, pressure, motor],
            datatype=DataType.REGISTERS
        )

        self.PLC = SimDevice(
            id=dev_id,
            simdata=self.PLC_data
        )


PLC1 = PLC(1,24,100,1)
PLC2 = PLC(2,39,132,1)
PLC3 = PLC(3,22,121,1)

devices = [PLC1.PLC, PLC2.PLC, PLC3.PLC]

for d in devices:
    print(d.simdata)

StartTcpServer(
    context=devices,
    address=("0.0.0.0", 5020)
)