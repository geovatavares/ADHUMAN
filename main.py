from adhuman.managed_system import ManagedSystem
from adhuman.monitor import Monitor
from adhuman.analyze import Analyze
from adhuman.plan import Plan
from adhuman.execute import Execute
import time

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
    
    time.sleep(10)
