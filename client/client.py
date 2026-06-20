from pymodbus.client.tcp import ModbusTcpClient

client = ModbusTcpClient(
    "localhost", port=5020
)

client.connect()

class Client:
    def __init__(self, address, count, device_id):
        self.result = client.read_holding_registers(
            address=address,
            count=count,
            device_id=device_id
        )

PLC1 = Client(0,3,1)
PLC2 = Client(0,3,2)
PLC3 = Client(0,3,3)

clients = [PLC1, PLC2, PLC3]

for c in clients:
    print(c.result.registers)

client.close()