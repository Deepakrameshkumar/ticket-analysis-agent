class AutomationAnalyzerAgent:
    def __init__(self, criteria):
        super().__init__(name="automation_analyzer")
        self.criteria = criteria
    
    def process(self, state):
        if "error" in state:
            return state
            
        df = state["data"]
        def analyze(description):
            desc_lower = description.lower()
            word_count = len(description.split())
            if (any(kw in desc_lower for kw in self.criteria['easy']['keywords']) 
                and word_count <= self.criteria['easy']['max_steps'] * 10):
                return "Easy"
            elif (any(kw in desc_lower for kw in self.criteria['moderate']['keywords']) 
                  and word_count <= self.criteria['moderate']['max_steps'] * 10):
                return "Moderate"
            return "Difficult"
        
        df['automation_complexity'] = df['description'].apply(analyze)
        return {"data": df}