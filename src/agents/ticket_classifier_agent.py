import ollama

class TicketClassifierAgent:
    def __init__(self, model_config, categories):
        self.model = model_config['name']
        self.host = model_config['host']
        self.categories = categories
    
    def classify(self, description):
        prompt = f"""Classify the following ticket description into one of these categories:
        {', '.join(self.categories)}
        
        Description: {description}
        
        Category: """
        
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={"max_tokens": 20}
        )
        
        result = response['response']
        for category in self.categories:
            if category.lower() in result.lower():
                return category
        return "Uncategorized"
    
    def process(self, state):
        if state.error:
            return state
        
        df = state.data
        df['category'] = df['description'].apply(self.classify)
        state.data = df
        return state