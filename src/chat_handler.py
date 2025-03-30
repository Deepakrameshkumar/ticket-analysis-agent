import ollama

class ChatHandler:
    def __init__(self, model_config):
        self.model = model_config['name']
        self.host = model_config['host']
        self.last_data = None
    
    def set_data(self, data):
        self.last_data = data
    
    def chat(self, message):
        if not self.last_data:
            return "Please upload data first"
            
        prompt = f"""Given this ticket analysis data:
        {str(self.last_data['summary'])}
        
        User question: {message}
        
        Answer: """
        
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={"max_tokens": 200}
        )
        return response['response']