class AdHuman:
    def predict_ph(self, temperature, turbidity, history):
        print(f"[AdHuman] Predicting pH ")
        return sum(history) / len(history) if history else 7.0
    
    def notify_human(self, ph_value):
        print(f"[AdHuman] Notifying human: Current pH value is {ph_value}.")
        if 6.5 <= ph_value <= 7.5:
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

