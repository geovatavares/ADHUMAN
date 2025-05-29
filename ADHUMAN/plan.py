class Plan:
    def create_plan(self, ph_value):
        print(f"[Plan] Creating plan for pH {ph_value}")
        return "Add base" if ph_value < 6.5 else "Add acid"
