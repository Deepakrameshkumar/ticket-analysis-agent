from langgraph import Agent
import pandas as pd

class ReportGeneratorAgent(Agent):
    def __init__(self):
        super().__init__(name="report_generator")
    
    def process(self, state):
        if "error" in state:
            return state
            
        df = state["data"]
        summary = df.groupby(['category', 'automation_complexity']).agg({
            'potential_savings': ['sum', 'count'],
            'ticket_id': 'count'
        }).reset_index()
        
        summary['priority_score'] = (
            summary[('potential_savings', 'sum')] * 0.6 +
            summary[('ticket_id', 'count')] * 0.4
        )
        
        summary['priority'] = pd.qcut(
            summary['priority_score'], 3, 
            labels=['Now', 'Next', 'Later']
        )
        
        report = {"summary": summary.to_dict(), "raw_data": df.to_dict()}
        return report