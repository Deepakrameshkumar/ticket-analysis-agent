class SavingsCalculatorAgent:
    def __init__(self, hourly_rate, base_time):
        super().__init__(name="savings_calculator")
        self.hourly_rate = hourly_rate
        self.base_time = base_time
    
    def process(self, state):
        if "error" in state:
            return state
            
        df = state["data"]
        complexity_multipliers = {"Easy": 0.8, "Moderate": 0.6, "Difficult": 0.3}
        
        def calculate(row):
            multiplier = complexity_multipliers.get(row['automation_complexity'], 0.5)
            manual_cost = row['resolution_time'] * self.hourly_rate
            automated_cost = row['resolution_time'] * self.hourly_rate * (1 - multiplier)
            return manual_cost - automated_cost
        
        df['potential_savings'] = df.apply(calculate, axis=1)
        return {"data": df}