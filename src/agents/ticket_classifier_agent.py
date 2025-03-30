from transformers import AutoModelForCausalLM, AutoTokenizer
from langgraph import Agent

class TicketClassifierAgent(Agent):
    def __init__(self, model_path, categories):
        super().__init__(name="ticket_classifier")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)
        self.categories = categories
    
    def process(self, state):
        if "error" in state:
            return state
        
        df = state["data"]
        def classify(description):
            prompt = f"""Classify ticket into: {', '.join(self.categories)}
            Description: {description}
            Category: """
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(**inputs, max_new_tokens=20)
            result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            for cat in self.categories:
                if cat.lower() in result.lower():
                    return cat
            return "Uncategorized"
        
        df['category'] = df['description'].apply(classify)
        return {"data": df}