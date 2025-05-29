import tkinter as tk
from tkinter import simpledialog, messagebox
import random

class ManagedSystem:
    def __init__(self):
        self.temperature = 26.5
        self.turbidity = 5.2

    def get_data(self):
        ph_value = None
        return self.temperature, self.turbidity, ph_value

class Monitor:
    def __init__(self):
        self.history = []

    def aggregate_data(self, data):
        temperature, turbidity, ph_value = data
        return temperature, turbidity, ph_value, self.history

    def update_history(self, ph_value):
        self.history.append(ph_value)

class Analyze:
    def __init__(self, gui):
        self.acceptable_range = (6.5, 7.5)
        self.gui = gui

    def analyze(self, temperature, turbidity, ph_value, history):
        if ph_value is None:
            predicted_ph = AdHuman().predict_ph(temperature, turbidity, history)
            confirmed_ph = self.gui.ask_human_confirmation(predicted_ph)
            return self.analyze(temperature, turbidity, confirmed_ph, history)

        AdHuman().notify_human(ph_value, self.gui)

        if self.acceptable_range[0] <= ph_value <= self.acceptable_range[1]:
            return ph_value, False
        return ph_value, True

class AdHuman:
    def predict_ph(self, temperature, turbidity, history):
        return round(sum(history) / len(history), 2) if history else 7.0

    def notify_human(self, ph_value, gui):
        if 6.5 <= ph_value <= 7.5:
            gui.display_message(f"Current pH: {ph_value} - No adaptation required.")
        else:
            gui.display_message(f"Current pH: {ph_value} - Adaptation required!")

class Plan:
    def create_plan(self, ph_value):
        return "Add base" if ph_value < 6.5 else "Add acid"

class Execute:
    def execute_plan(self, action, gui):
        gui.display_message(f"Executing action: {action}")

# GUI Class
class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("pH System")

        self.text = tk.Text(root, height=20, width=60, font=("Courier", 10))
        self.text.pack(padx=10, pady=10)

        self.button = tk.Button(root, text="Run Next Cycle", command=self.run_cycle)
        self.button.pack(pady=5)

        self.managed_system = ManagedSystem()
        self.monitor = Monitor()
        self.analyze = Analyze(self)
        self.plan = Plan()
        self.execute = Execute()

    def run_cycle(self):
        data = self.managed_system.get_data()
        temperature, turbidity, ph_value, history = self.monitor.aggregate_data(data)
        ph_value, needs_action = self.analyze.analyze(temperature, turbidity, ph_value, history)
        self.monitor.update_history(ph_value)

        if needs_action:
            action = self.plan.create_plan(ph_value)
            self.execute.execute_plan(action, self)
        self.display_message("-" * 50)

    def ask_human_confirmation(self, predicted_ph):
        answer = messagebox.askyesno("Human Validation", f"The system predicted pH = {predicted_ph}. Accept?")
        if answer:
            return predicted_ph
        else:
            try:
                value = float(simpledialog.askstring("Manual Input", "Enter the correct pH value:"))
                return value
            except:
                messagebox.showwarning("Invalid", "Invalid input. Using system prediction.")
                return predicted_ph

    def display_message(self, msg):
        self.text.insert(tk.END, msg + "\n")
        self.text.see(tk.END)

# Main loop
if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
