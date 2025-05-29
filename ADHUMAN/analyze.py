from adhuman.adhuman import AdHuman
from adhuman.gui import GUI

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
