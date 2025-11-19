from machine import PWM, Pin

PWM_FREQ = 1000  # Frecuencia del PWM en HZ
pin_pwm = 15 # Número de pin GPIO para PWM, se puede cambiar según sea necesario

class Motor:
    def __init__(self, pin=pin_pwm, freq=PWM_FREQ):
        try:
            self.pwm = PWM(Pin(pin))
            self.pwm.freq(freq)
            self.speed = 0  # Velocidad inicial del motor en porcentaje (0-100)
            self.led_estatus = Pin("LED", Pin.OUT)
            self.led_estatus.value(1)  # Enciende el LED de estatus para indicar que el motor está inicializado
            print(pin)
            print(freq)
        except Exception as e:
            print("Error al inicializar el motor:", e)

    def set_speed(self, speed):
        """Establecer la velocidad del motor como un porcentaje (0-100)."""
        if speed < 0 or speed > 100:
            raise ValueError("La velocidad debe estar entre 0% y 100%")
        self.speed = speed
        duty_cycle = int((speed / 100) * 65535)  # Convierte porcentaje a valor de duty cycle (0-65535)
        self.pwm.duty_u16(duty_cycle)

    def stop(self):
        """Detener el motor."""
        self.set_speed(0)

    def cleanup(self):
        """Liberar los recursos de PWM."""
        self.pwm.deinit()