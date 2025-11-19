import modules.motors as motors

motorRight = motors.Motor()
motorLeft = motors.Motor(16, 1000, 17, 18)

"""PRUEBAS PARA VERIFICAR LOS MÉTODOS"""

motorRight.set_speed(50)
motorLeft.set_speed(50)

motorRight.go_forward()
motorLeft.go_forward()