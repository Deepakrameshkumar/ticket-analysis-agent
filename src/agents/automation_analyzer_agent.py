class AutomationAnalyzerAgent:
    def __init__(self, criteria):
        self.criteria = criteria
    
    def analyze(self, description):
        desc_lower = description.lower()
        word_count = len(description.split())
        if (any(kw in desc_lower for kw in self.criteria['easy']['keywords']) 
            and word_count <= self.criteria['easy']['max_steps'] * 10):
            return "Easy"
        elif (any(kw in desc_lower for kw in self.criteria['moderate']['keywords']) 
              and word_count <= self.criteria['moderate']['max_steps'] * 10):
            return "Moderate"
        return "Difficult"
    
    def process(self, state):
        if state.get("error"):
            return {}
        df = state["data"]
        df['automation_complexity'] = df['description'].apply(self.analyze)
        return {"data": df}