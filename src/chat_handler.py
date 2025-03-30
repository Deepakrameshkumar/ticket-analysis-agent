from transformers import AutoModelForCausalLM, AutoTokenizer

class ChatHandler:
    def __init__(self, model_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)
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
        
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=200)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)