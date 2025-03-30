import pandas as pd

class DataReaderAgent:
    def process(self, state):
        try:
            # First try UTF-8
            df = pd.read_csv(state['file_path'], encoding='utf-8')
        except UnicodeDecodeError:
            # If UTF-8 fails, try Windows-1252 (common for Windows CSVs)
            try:
                df = pd.read_csv(state['file_path'], encoding='windows-1252')
            except Exception as e:
                return {"error": f"Failed to decode CSV with UTF-8 or Windows-1252: {str(e)}"}
        except Exception as e:
            return {"error": f"Error reading CSV: {str(e)}"}
        
        required_columns = ['ticket_id', 'description', 'resolution_time']
        if not all(col in df.columns for col in required_columns):
            return {"error": f"CSV missing required columns. Found: {list(df.columns)}, Required: {required_columns}"}
        
        return {"data": df}