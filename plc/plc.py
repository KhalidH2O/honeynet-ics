# #PLC Devices Simulation

from pymodbus.simulator import SimData, SimDevice, DataType
from pymodbus.server import ModbusTcpServer
from pymodbus import FramerType

from time import sleep
import asyncio

import logging

logging.basicConfig(
    level=logging.DEBUG
)

class PLC:
    def __init__(self, dev_id):
        self.PLC_data = SimData(
            address=0,
            count=2,
            values=[0,0],
            datatype=DataType.REGISTERS
        )
        # values = [level, pump]

        self.PLC = SimDevice(
            id=dev_id,
            simdata=self.PLC_data
        )
        
class Tank:
    def __init__(self, dev_id, capacity, max_level, min_level, level, pump):
        self.dev_id = dev_id
        self.capacity = capacity
        self.max_level = max_level
        self.min_level = min_level

        self.level = level
        self.pump = pump

        self.plc = PLC(dev_id)
        self.device = self.plc.PLC

    def set_pump(self):
        if (self.level <= self.min_level):
            self.pump = 1
        elif (self.level >= self.max_level):
            self.pump = 0

class Plant:
    def __init__(self):
        #id, capacity, max_level, min_level, level, pump
        self.tank1 = Tank(1,6000,5920,1200,5050,1)
        self.tank2 = Tank(2,2000,1950,300,1233,1)
        self.tank3 = Tank(3,1200,1150,200,400,1)

        self.tanks = [self.tank1, self.tank2, self.tank3]
        
    def update_flows(self):
        # Outflows
        self.T1_outflow = 0
        self.T2_outflow = 1
        self.T3_outflow = 1
        
        # Tank 1
        if (self.tank1.pump):
            self.T1_inflow = 6
        else:
            self.T1_inflow = 0
        
        # Tank 2
        if (self.tank2.pump):
            self.T1_outflow += 2
            self.T2_inflow = 2
        else:
            self.T2_inflow = 0 

        # Tank 3
        if (self.tank3.pump):
            self.T1_outflow += 2
            self.T3_inflow = 2
        else:
            self.T3_inflow = 0
    
    def do_flows(self):
        self.tank1.level += self.T1_inflow
        self.tank1.level -= self.T1_outflow

        self.tank2.level += self.T2_inflow
        self.tank2.level -= self.T2_outflow

        self.tank3.level += self.T3_inflow
        self.tank3.level -= self.T3_outflow

    def tick(self):
        for t in self.tanks:
            t.set_pump()

        self.update_flows()
        self.do_flows()

async def process(plant, server):
    while True:
        plant.tick()

        #update the server values
        for tank in plant.tanks: 
            await server.async_setValues(
                device_id=tank.dev_id,
                func_code=3,
                address=0,
                values=[tank.level, tank.pump])

        await asyncio.sleep(1)
        print("Running process")


async def main():    
    plant = Plant()

    devices = [plant.tank1.device, plant.tank2.device, plant.tank3.device]

    server = ModbusTcpServer(
        context=devices,
        framer=FramerType.SOCKET,        
        address=("0.0.0.0", 5020)
    )
    
    asyncio.create_task(process(plant, server))
    
    await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())