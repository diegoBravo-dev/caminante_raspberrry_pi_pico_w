import bluetooth
import aioble
import asyncio

# Definir UUIDs para los servicios y características
# Usando UUIDs estándar de UART para mejor compatibilidad
_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")  # Nordic UART Service
_RX_CHARACTERISTIC_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")  # RX (recibir)
_TX_CHARACTERISTIC_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")  # TX (enviar)

SOY = "Control_Caminante"
MESSAGE = f"Hola, soy {SOY}.\n"

class controlBT:
    def __init__(self, name=SOY, service_uuid=_SERVICE_UUID, 
                 rx_uuid=_RX_CHARACTERISTIC_UUID,
                 tx_uuid=_TX_CHARACTERISTIC_UUID,
                 apariencia=0x0300,
                 intervalo_advertencia=250_000):  # microsegundos
        self.BLE_NAME = name
        self.BLE_SVC_UUID = service_uuid
        self.BLE_RX_UUID = rx_uuid
        self.BLE_TX_UUID = tx_uuid
        self.BLE_APPEARENCE = apariencia
        self.BLE_ADVERTISING_INTERVAL = intervalo_advertencia
        self.message_count = 0
        self.connection = None

    async def receive_data_task(self, rx_characteristic):
        """Tarea para recibir datos del celular"""
        print(f"{self.BLE_NAME} esperando datos...")
        
        while self.connection and self.connection.is_connected():
            try:
                # Esperar datos escritos por el cliente
                _, data = await rx_characteristic.written()
                
                if data:
                    try:
                        message = data.decode('utf-8')
                        print(f"{SOY} recibe: '{message}' (contador: {self.message_count + 1})")
                    except:
                        print(f"{SOY} recibie datos: {data.hex()} (contador: {self.message_count + 1})")
                    
                    self.message_count += 1

            except asyncio.CancelledError:
                print("Tarea de recepción cancelada")
                break
            except Exception as e:
                print(f"Error al recibir mensaje: {e}")
                await asyncio.sleep(0.1)

    async def send_data_task(self, tx_characteristic):
        """Tarea opcional para enviar datos al celular"""
        await asyncio.sleep(2)  # Esperar a que se establezca la conexión
        
        while self.connection and self.connection.is_connected():
            try:
                # Enviar confirmación o datos al celular
                response = f"Mensaje #{self.message_count} recibido OK\n"
                tx_characteristic.notify(self.connection, response.encode('utf-8'))
                await asyncio.sleep(5)  # Enviar cada 5 segundos
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error al enviar: {e}")
                await asyncio.sleep(0.1)

    async def peripheral_mode(self):
        """Modo periférico BLE"""
        # Registrar servicio y características
        self.BLE_SVC = aioble.Service(self.BLE_SVC_UUID)
        
        # RX: el celular ESCRIBE datos aquí (Pico recibe)
        self.BLE_RX_CHAR = aioble.Characteristic(
            self.BLE_SVC,
            self.BLE_RX_UUID,
            read=False,
            write=True,  # ¡Importante! Debe ser True para recibir
            notify=False,
            capture=True
        )
        
        # TX: el Pico NOTIFICA datos aquí (celular recibe)
        self.BLE_TX_CHAR = aioble.Characteristic(
            self.BLE_SVC,
            self.BLE_TX_UUID,
            read=True,
            write=False,
            notify=True,
            capture=False
        )
        
        aioble.register_services(self.BLE_SVC)
        print(f"{self.BLE_NAME} servicio registrado")

        while True:
            print(f"{self.BLE_NAME} comenzando a anunciar...")
            
            try:
                async with await aioble.advertise(
                    self.BLE_ADVERTISING_INTERVAL,
                    name=self.BLE_NAME,
                    services=[self.BLE_SVC_UUID],
                    appearance=self.BLE_APPEARENCE
                ) as connection:
                    
                    self.connection = connection
                    print(f"{self.BLE_NAME} conectado a: {connection.device}")
                    
                    # Crear tareas concurrentes
                    receive_task = asyncio.create_task(
                        self.receive_data_task(self.BLE_RX_CHAR)
                    )
                    # send_task = asyncio.create_task(
                    #     self.send_data_task(self.BLE_TX_CHAR)
                    # )
                    
                    # Esperar hasta que se desconecte
                    await connection.disconnected()
                    
                    # Cancelar tareas
                    receive_task.cancel()
                    # send_task.cancel()
                    
                    print(f"{SOY} se ha desconectado")
                    
            except asyncio.CancelledError:
                print("Anuncio cancelado")
                break
            except Exception as e:
                print(f"Error en peripheral_mode: {e}")
                await asyncio.sleep(1)
