class SavingsCalculatorAgent:
    def __init__(self, hourly_rate, base_time):
        self.hourly_rate = hourly_rate
        self.base_time = base_time
    
    def calculate(self, row):
        complexity_multipliers = {"Easy": 0.8, "Moderate": 0.6, "Difficult": 0.3}
        multiplier = complexity_multipliers.get(row['automation_complexity'], 0.5)
        manual_cost = row['resolution_time'] * self.hourly_rate
        automated_cost = row['resolution_time'] * self.hourly_rate * (1 - multiplier)
        return manual_cost - automated_cost
    
    def process(self, state):
        if state.error:
            return state
        df = state.data
        df['potential_savings'] = df.apply(self.calculate, axis=1)
        state.data = df
        return state