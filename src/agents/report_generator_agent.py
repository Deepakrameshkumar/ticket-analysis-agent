import pandas as pd
import logging

logger = logging.getLogger(__name__)

class ReportGeneratorAgent:
    def process(self, state):
        if state.get("error"):
            return {}
        df = state["data"]
        logger.debug("Generating report summary")
        summary = df.groupby(['category', 'automation_complexity']).agg({
            'potential_savings': ['sum', 'count'],
            'ticket_id': 'count'
        }).reset_index()
        
        summary['priority_score'] = (
            summary[('potential_savings', 'sum')] * 0.6 +
            summary[('ticket_id', 'count')] * 0.4
        )
        
        try:
            summary['priority'] = pd.qcut(
                summary['priority_score'], 3, 
                labels=['Now', 'Next', 'Later'],
                duplicates='drop'  # Drop duplicate bin edges
            )
        except ValueError as e:
            logger.warning(f"qcut failed: {str(e)}. Assigning default priority.")
            summary['priority'] = 'Now'  # Fallback if qcut fails
        
        logger.debug("Report summary generated")
        return {
            "summary": summary.to_dict(),
            "raw_data": df.to_dict()
        }