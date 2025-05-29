class Monitor:
    def __init__(self):
        self.history = []

    def aggregate_data(self, data):
        print("[Monitor] aggregateData()")
        temperature, turbidity, ph_value = data
        return temperature, turbidity, ph_value, self.history

    def update_history(self, ph_value):
        self.history.append(ph_value)
