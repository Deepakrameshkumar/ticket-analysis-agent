import ollama
import logging

logger = logging.getLogger(__name__)

class TicketClassifierAgent:
    def __init__(self, model_config, categories):
        self.model = model_config['name']
        self.host = model_config['host']
        self.categories = categories
    
    def classify_batch(self, descriptions):
        prompt = "Classify these ticket descriptions into one of: " + ', '.join(self.categories) + "\n\n"
        for i, desc in enumerate(descriptions, 1):
            prompt += f"{i}. {desc}\n"
        prompt += "\nReturn results as numbered list (e.g., '1. Technical Support'):"
        
        logger.debug(f"Sending batch prompt with {len(descriptions)} descriptions")
        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={"max_tokens": 200}
            )
            logger.debug(f"Batch result: {response['response']}")
        except Exception as e:
            logger.error(f"Batch classification failed: {str(e)}")
            return ["Uncategorized"] * len(descriptions)
        
        results = response['response'].split('\n')
        categories = []
        for line in results:
            for cat in self.categories:
                if cat.lower() in line.lower():
                    categories.append(cat)
                    break
            else:
                categories.append("Uncategorized")
        return categories[:len(descriptions)]
    
    def process(self, state):
        if state.get("error"):
            return {}
        df = state["data"]
        logger.info(f"Starting batch classification of {len(df)} tickets")
        batch_size = 10
        results = []
        for i in range(0, len(df), batch_size):
            batch = df['description'][i:i + batch_size].tolist()
            batch_results = self.classify_batch(batch)
            results.extend(batch_results)
        df['category'] = results
        logger.info("Batch classification complete")
        return {"data": df}