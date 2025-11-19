from machine import PWM, Pin
from time import sleep

PWM_FREQ = 1000  # Frecuencia del PWM en HZ
pin_pwm = 15 # Número de pin GPIO para PWM, se puede cambiar según sea necesario
pin_enable1 = 14 # Número de pin GPIO para el enable 1/3, se puede cambiar según sea necesario
pin_enable2 = 13 # Número de pin GPIO para el enable 2/4, se puede cambiar según sea necesario


class Motor:
    def __init__(self, pin=pin_pwm, freq=PWM_FREQ, enable1=pin_enable1, enable2=pin_enable2):
        try:
            self.pwm = PWM(Pin(pin))
            self.pwm.freq(freq)
            self.speed = 0  # Velocidad inicial del motor en porcentaje (0-100)
            self.enable1 = Pin(enable1, Pin.OUT) # Habilita el pin 1 de control del motor
            self.enable2 = Pin(enable2, Pin.OUT) # Habilita el pin 2 de control del motor
            self.led_estatus = Pin("LED", Pin.OUT)
            self.enable1.value(0) # Enciende el enable 1
            self.enable2.value(0) # Enciende el enable 2
            self.led_estatus.value(1)  # Enciende el LED de estatus para indicar que el motor está inicializado
            print("Motor inicializado en el pin PWM:")
            print(pin)
            print("Frecuencia PWM:")
            print(freq)
            print("Confirmacion de pines de habilitacion:")
            print("Enable 1:", enable1)
            print("Enable 2:", enable2)
        except Exception as e:
            print("Error al inicializar el motor:", e)

    def set_speed(self, speed):
        """Establecer la velocidad del motor como un porcentaje (0-100)."""
        if speed < 0 or speed > 100:
            raise ValueError("La velocidad debe estar entre 0% y 100%")
        self.speed = speed
        duty_cycle = int((speed / 100) * 65535)  # Convierte porcentaje a valor de duty cycle (0-65535)
        self.pwm.duty_u16(duty_cycle)

    def go_forward(self):
        """Mover el motor hacia adelante."""
        self.enable1.value(1)
        self.enable2.value(0)
        print("adelante")
        print("Valor del Enable 1: ", self.enable1.value())
        print("Valor del Enable 2: ", self.enable2.value())

    def go_backward(self):
        """Mover el motor hacia atrás."""
        self.enable1.value(0)
        self.enable2.value(1)
        print("atras")
        print("Valor del Enable 1: ", self.enable1.value())
        print("Valor del Enable 2: ", self.enable2.value())

    def stop(self):
        """Detener el motor."""
        self.set_speed(0)

    def cleanup(self):
        """Liberar los recursos de PWM."""
        self.pwm.deinit()
    
    def check_motor(self):
        """Revisar si el PWM asignado está bien"""

        while True:
            for duty in range(0, 65535, 100): # Incrementa el ciclo de trabajo 
                self.pwm.duty_u16(duty)
                print(f"Duty cycle: {duty}\n")
                sleep(0.01)
            for duty in range(65535, 0, -100): # Decrementa el ciclo de trabajo
                self.pwm.duty_u16(duty)
                print(f"Duty cycle: {duty}\n")
                sleep(0.01)