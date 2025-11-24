import modules.motors as motors
import modules.controlBT as controlBT
import asyncio

volatile_speed = 0
STEP = 10

async def procesar_comando(data):
    """Procesa los comandos recibidos por Bluetooth"""
    global volatile_speed
    speed_out_phased = 0
    try:
        comando = data.decode('utf-8').strip()
        print(f"Comando procesado: {comando}")

        if comando == '+':
            volatile_speed += STEP
            if(volatile_speed > 100):
                volatile_speed = 100
            print(volatile_speed)
            motorRight.set_speed(volatile_speed)
            motorLeft.set_speed(volatile_speed)

        elif comando == '-':
            volatile_speed -= STEP
            if(volatile_speed < 0):
                volatile_speed = 0
            print(volatile_speed)
            motorRight.set_speed(volatile_speed)
            motorLeft.set_speed(volatile_speed)

        elif comando == 'F':
            motorRight.go_forward()
            motorLeft.go_backward()

        elif comando == 'B':
            motorRight.go_backward()
            motorLeft.go_backward()
        
        elif comando == 'S':
            motorRight.stop()
            motorLeft.stop()
        
        else:
            print("Comando no reconocido :(")

    except Exception as e:
        print(f"Error al procesar el comando {e}")

async def control_iniciar(control):
    control.callback_procesar = procesar_comando
    await control.peripheral_mode()

motorRight = motors.Motor()
motorLeft = motors.Motor(16, 1000, 17, 18)
control = controlBT.controlBT()
asyncio.run(control_iniciar(control))