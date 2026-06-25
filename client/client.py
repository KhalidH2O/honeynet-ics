from pymodbus.client.tcp import ModbusTcpClient
from time import sleep

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

client.write_registers(
    address=2,
    values=[1,0],
    device_id=2)

try:
    while True:
        for c in clients:
            print(c.read_register())
        sleep(1)

except KeyboardInterrupt:
    client.close()
    print("\nClient connection closed!")
