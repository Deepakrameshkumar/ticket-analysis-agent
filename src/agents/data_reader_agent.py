import pandas as pd

class DataReaderAgent:
    def process(self, state):
        try:
            df = pd.read_csv(state['file_path'])
            required_columns = ['ticket_id', 'description', 'resolution_time']
            if not all(col in df.columns for col in required_columns):
                raise ValueError("CSV missing required columns")
            return {"data": df}
        except Exception as e:
            return {"error": f"Error reading CSV: {str(e)}"}