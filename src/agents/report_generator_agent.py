import pandas as pd

class ReportGeneratorAgent:
    def process(self, state):
        if state.get("error"):
            return {}
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
        
        return {
            "summary": summary.to_dict(),
            "raw_data": df.to_dict()
        }