import pandas as pd

class DataReaderAgent:
    def process(self, state):
        try:
            df = pd.read_csv(state.file_path)
            required_columns = ['ticket_id', 'description', 'resolution_time']
            if not all(col in df.columns for col in required_columns):
                raise ValueError("CSV missing required columns")
            state.data = df
            return state
        except Exception as e:
            state.error = f"Error reading CSV: {str(e)}"
            return state