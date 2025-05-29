import random

class ManagedSystem:
    def __init__(self):
        self.temperature = 26.5
        self.turbidity = 5.2

    def get_data(self):
        ph_value = None # Simula falha no sensor
        round(random.uniform(5.0, 9.0), 2)  # Gera um novo valor de pH a cada chamada
        print("[Managed System] Sending data.")
        return self.temperature, self.turbidity, ph_value
