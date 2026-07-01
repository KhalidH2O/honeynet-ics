import sys
from time import sleep

from pymodbus.client.tcp import ModbusTcpClient
from plc.registers import Registers

client = ModbusTcpClient(
    "localhost", port=5020
)

class Client:
    def __init__(self, dev_id):
        self.dev_id = dev_id

    def read_register(self):
        self.result = client.read_holding_registers(
            address=0,
            count=4,
            device_id=self.dev_id
        )
        return self.result.registers

client.connect()

PLC1 = Client(1)
PLC2 = Client(2)
PLC3 = Client(3)

clients = [PLC1, PLC2, PLC3]

def read_plant():
    while True:
        for c in clients:
            values = c.read_register()
            print(f"\n--- PLC {c.dev_id} ---")
            print(f"Tank Level   : {values[Registers.LEVEL]}")
            print(f"Pump State   : {values[Registers.PUMP]}")
            print(f"Pump Mode    : {values[Registers.PUMP_MODE]}")
            print(f"Pump Command : {values[Registers.PUMP_MANUAL]}")
            print("\n")
        print("-------------------------")
        print("Press Ctrl+C to exit...")
        print("-------------------------")
        sleep(1)

def set_pump_mode():
    # Pump Selection
    while True:
        try:
            print("\nSelect the pump to set the mode:")
            for c in clients:
                print(f"{c.dev_id}. Pump {c.dev_id}")

            print(" ")
            pump_option = int(input())

            # Pump selection validation
            if not (0 < pump_option <= c.dev_id):
                continue

        except ValueError:
            print("\nInvalid input!\n")
            continue

        else:
            break
    
    # Get current Pump mode
    current_mode = client.read_holding_registers(
        address=2,
        count=1,
        device_id=pump_option
        ).registers[0]
    
    # Get Pump mode
    while True:    
        try:
            print("Set Pump:")
            print("0. Automatic")
            print("1. Manual\n")

            mode_option = int(input())

            if not (mode_option == 0 or mode_option == 1):
                continue
        
        except ValueError:
            print("\nInvalid Input!\n")
        
        else:
            break
    
    # Set Pump mode
    if (mode_option == current_mode):
        print(f"\nPump already set to {mode_option}!\n")
    else:
        client.write_registers(
            address=2,
            values=[mode_option],
            device_id=pump_option
            )

def set_pump_cmd():
    # Set Pump ON/OFF
    while True:
        try:
            print("Select the pump to turn ON/OFF:")
            
            for c in clients:
                print(f"{c.dev_id}. Pump {c.dev_id}")
            
            pump_option = int(input())

            if not (0 < pump_option <= c.dev_id):
                continue

        except ValueError:
            print("\nInvalid input!\n")
            continue
        else:
            break
        
    pump_mode = client.read_holding_registers(
        address=2,
        count=1,
        device_id=pump_option).registers[0]
    
    while True:
        try:
            print("Select Pump command:")
            print("0. OFF")
            print("1. ON")
        
        except ValueError:
            print("\nInvalid input!\n")
        
        else:
            break
        


def end_client():
    client.close()
    print("\nClient connection closed!")
    sys.exit(0)

while True:
    try:
        print("=== SCADA ===")
        print("             ")
        print("1. Read Plant values")
        print("2. Set Pump AUTO/MANUAL")
        print("3. Set Pump Command")
        print("4. Exit\n")

        option = int(input())
        
        match option:
            case 1:
                read_plant()
            case 2:
                set_pump_mode()
            case 3:
                set_pump_cmd()
            case 4:
                end_client()
            case _:
                print("\nInvalid Input!\n")

    except ValueError:
        print("\nInvalid Input!\n")
        continue

    except KeyboardInterrupt:
        end_client()