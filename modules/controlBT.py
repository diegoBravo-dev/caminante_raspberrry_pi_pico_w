import bluetooth
import struct
import aioble
import asyncio
from sys import exit

# Definir UUID.s para los servicios y características

_SERVICE_UUID = bluetooth.UUID(0x1848)
_CHARACTERISTIC_UUID = bluetooth.UUID(0x2A6E)

SOY = "Control_Caminante"
MESSAGE = f"Hola, soy {SOY}.\n"

class controlBT:
    def __init__(self, name = SOY, service_uuid = _SERVICE_UUID, 
                 charac_uuid = _CHARACTERISTIC_UUID, apariencia = 0x0300,
                 intervalo_advertencia = 2000, tamano_scan = 5000,
                 intervalo = 30000, window = 30000):
        self.BLE_NAME = name
        self.BLE_SVC_UUID = service_uuid
        self.BLE_CHARACTERISTIC_UUID = charac_uuid
        self.BLE_APPEARENCE = apariencia
        self.BLE_ADVERTISING_INTERVAL = intervalo_advertencia
        self.BLE_SCAN_LENGTH = tamano_scan
        self.BLE_INTERVALO = intervalo
        self.BLE_WINDOW = window

        self.message_count = 0
    
    def decode_message(mensaje):
        return mensaje.decode('utf-8')
    

    async def receive_data_task(self, characteristic):
        while True:
            try:
                data = await characteristic.read()

                if data:
                    print(f"{SOY} recibió el siguiente mensaje: {}")
            
            except: 
