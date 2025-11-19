import modules.motors as motors

motorRight = motors.Motor()
motorLeft = motors.Motor(16, 1000, 17, 18)

"""PRUEBAS PARA VERIFICAR LOS MÉTODOS"""

motorRight.check_motor()