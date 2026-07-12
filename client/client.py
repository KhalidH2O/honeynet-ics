from time import sleep
from services.PLC_service import PLCService

service = PLCService()

try:
    service.connect()
except ConnectionError as e:
    print(e)
    exit(1)

def read_plant():
    while True:
        plcs = service.read_all()

        for plc in plcs:
            print(f"\n--- PLC {plc.id} ---")
            print(f"Tank Level   : {plc.level}")
            print(f"Pump State   : {plc.pump}")
            print(f"Pump Mode    : {plc.pump_mode}")
            print(f"Pump Command : {plc.pump_manual}")
        print("\n")
        print("-------------------------")
        print("Press Ctrl+C to exit...")
        print("-------------------------")
        sleep(1)

def set_pump_mode():
    # Pump Selection
    while True:
        try:
            plcs = service.read_all()
            print("\nSelect the pump to set the mode:")
            for plc in plcs:
                print(f"{plc.id}. Pump {plc.id}")

            print(" ")
            pump_option = int(input())

            # Pump selection validation
            if not (0 < pump_option <= plc.id):
                continue

        except ValueError:
            print("\nInvalid input!\n")
            continue

        else:
            break
    
    # Get Pump mode
    while True:    
        try:
            print("\nSet Pump:")
            print("0. Automatic")
            print("1. Manual\n")

            mode_option = int(input())

            if not (mode_option == 0 or mode_option == 1):
                continue
        
        except ValueError:
            print("\nInvalid Input!\n")
        
        else:
            break

    # Get current Pump mode
    current_mode = service.read(pump_option).pump_mode
    
    # Set Pump mode
    if (mode_option == current_mode):
        print(f"\nPump already set to {mode_option}!\n")
    else:
        service.set_mode(pump_option, mode_option)

def set_pump_cmd():
    # Set Pump ON/OFF
    while True:
        try:
            plcs = service.read_all()
            
            print("\nSelect the pump to turn ON/OFF:")
            for plc in plcs:
                print(f"{plc.id}. Pump {plc.id}")
            
            print(" ")
            pump_option = int(input())

            if not (0 < pump_option <= plc.id):
                continue

            pump_mode = service.read(pump_option).pump_mode
        
            if (pump_mode == 0):
                print(f"\nPump {pump_option} is in AUTO mode!")
                print("Set the pump to MANUAL mode to input commands...")
                
                break

        except ValueError:
            print("\nInvalid input!\n")
            continue
        else:
            break
        
    while (pump_mode):
        try:
            print("\nSelect Pump command:")
            print("0. OFF")
            print("1. ON\n")

            cmd_option = int(input())

            if (cmd_option in [0,1]):
                service.set_pump_cmd(pump_option, cmd_option)
                print(f"\nPump {pump_option} set to {cmd_option}!")
                
                break

            else:
                continue

        except ValueError:
            print("\nInvalid input!\n")
        
        else:
            break

while True:
    try:
        print("\n=== SCADA ===")
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
                service.disconnect()
            case _:
                print("\nInvalid Input!\n")

    except ValueError:
        print("\nInvalid Input!\n")
        continue

    except KeyboardInterrupt:
        service.disconnect()