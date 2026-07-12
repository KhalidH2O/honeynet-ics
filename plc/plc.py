# #PLC Devices Simulation
import asyncio
import logging

from .registers import Registers
from modbus.server import PLC, ModbusServer

logging.basicConfig(
    level=logging.DEBUG
)
        
class Tank:
    def __init__(self, dev_id, capacity, max_level, min_level, level, pump):
        
        # Static values
        self.dev_id = dev_id
        self.capacity = capacity
        self.max_level = max_level
        self.min_level = min_level

        # Dynamic values
        self.level = level
        self.pump = pump
        self.pump_mode = 0
        self.pump_manual = self.pump

        # PLC
        self.plc = PLC(dev_id)
        self.device = self.plc.PLC

    def set_pump(self, dev_id):
        # Automatic pump ON/OFF
        if (self.pump_mode == 0): 
            if (self.level <= self.min_level):
                self.pump = 1
            elif (self.level >= self.max_level):
                self.pump = 0

        # Manual pump operation
        else:
            self.pump = self.pump_manual
            print(f"Pump {dev_id} : Override ON!")

class Plant:
    def __init__(self):
        #id, capacity, max_level, min_level, level, pump
        self.tank1 = Tank(1,6000,5920,1200,5050,1)
        self.tank2 = Tank(2,2000,1950,300,1245,1)
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

        # Tank 3level
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
            t.set_pump(t.dev_id)

        self.update_flows()
        self.do_flows()

async def process(plant:Plant, server:ModbusServer):
    while True:
        # Read the client commands and store them in datastore
        await update_commands(plant, server)

        plant.tick()

        #update the server values
        for tank in plant.tanks:
            await server.set_values(tank)

        await asyncio.sleep(1)
        print("Running process")

async def update_commands(plant:Plant, server:ModbusServer):
    # Get pump values from server datastore
    for tank in plant.tanks:
        values = await server.get_values(tank.dev_id) #Edit
        
        # Store values in the tank process
        tank.pump_mode = values[Registers.PUMP_MODE]
        tank.pump_manual = values[Registers.PUMP_MANUAL]

        print(f"Pump[Manual] {tank.dev_id} : {tank.pump_manual}")

async def main():
    plant = Plant()

    devices = [plant.tank1.device, plant.tank2.device, plant.tank3.device]

    server = ModbusServer(devices)

    asyncio.create_task(process(plant, server))
    
    await server.serve()
    
if __name__ == "__main__":
    asyncio.run(main())