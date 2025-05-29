import random
import time

class ManagedSystem:
    def __init__(self):
        self.temperature = 26.5
        self.turbidity = 5.2

    def get_data(self):
        ph_value = None#round(random.uniform(5.0, 9.0), 2)  # Gera um novo valor de pH a cada chamada
        print("[Managed System] Sending data.")
        return self.temperature, self.turbidity, ph_value

class Monitor:
    def __init__(self):
        self.history = []

    def aggregate_data(self, data):
        print("[Monitor] aggregateData()")
        temperature, turbidity, ph_value = data
        return temperature, turbidity, ph_value, self.history

    def update_history(self, ph_value):
        self.history.append(ph_value)

class Analyze:
    def __init__(self):
        self.acceptable_range = (6.5, 7.5)

    def analyze(self, temperature, turbidity, ph_value, history):
        print("[Analyze] analyse()")
        if ph_value is None:
            print("[Analyze] pH unknown! unclear_analysis")
            predicted_ph = AdHuman().predict_ph(temperature, turbidity, history)
            confirmed_ph = GUI().ask_human_confirmation(predicted_ph)
            return self.analyze(temperature, turbidity, confirmed_ph, history)
        
        AdHuman().notify_human(ph_value)
        
        if self.acceptable_range[0] <= ph_value <= self.acceptable_range[1]:
            print(f"[Analyze] pH ({ph_value}) is within the acceptable range. No adaptation required.")
            return ph_value, False

        print(f"[Analyze] pH ({ph_value}) is out of acceptable range.")
        return ph_value, True

class AdHuman:
    def predict_ph(self, temperature, turbidity, history):
        print(f"[AdHuman] Predicting pH ")
        return sum(history) / len(history) if history else 7.0
    
    def notify_human(self, ph_value):
        print(f"[AdHuman] Notifying human: Current pH value is {ph_value}.")
        if ph_value <=7.5 and ph_value >= 6.5:
            print(f"[AdHuman] No adaptation required.")
        else: 
            print(f"[AdHuman] Adaptation required")

class GUI:
    def ask_human_confirmation(self, predicted_ph):
        print(f"[GUI] The system predicted a pH of {predicted_ph}. Human, is this value correct? (y/n)")
        resposta = input().strip().lower()
        if resposta == 'y':
            return predicted_ph
        else:
            return float(input("[GUI] Enter the correct pH value: "))

class Plan:
    def create_plan(self, ph_value):
        print(f"[Plan] Creating plan for pH {ph_value}")
        return "Add base" if ph_value < 6.5 else "Add acid"

class Execute:
    def execute_plan(self, action):
        print(f"[Execute] Executing action: {action}")
        print("----------------------------------------")

# Instanciando classes
managed_system = ManagedSystem()
monitor = Monitor()
analyze = Analyze()
plan = Plan()
execute = Execute()

# Loop contínuo do sistema
while True:
    data = managed_system.get_data()
    temperature, turbidity, ph_value, history = monitor.aggregate_data(data)
    ph_value, needs_action = analyze.analyze(temperature, turbidity, ph_value, history)
    monitor.update_history(ph_value)
    
    if needs_action:
        action = plan.create_plan(ph_value)
        execute.execute_plan(action)
    else:
        print("----------------------------------------")
    
    time.sleep(10)  # Aguarda 10 segundos antes do próximo ciclo
