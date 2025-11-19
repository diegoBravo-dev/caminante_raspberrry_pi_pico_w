import modules.motors as motors
import modules.controlBT as controlBT
import asyncio

async def control_iniciar(control):
    await control.peripheral_mode()

motorRight = motors.Motor()
motorLeft = motors.Motor(16, 1000, 17, 18)
control = controlBT.controlBT()
asyncio.run(control_iniciar(control))