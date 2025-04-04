from langgraph.graph import StateGraph, END
from typing import Dict, Any, TypedDict
from src.agents import (
    DataReaderAgent,
    TicketClassifierAgent,
    AutomationAnalyzerAgent,
    SavingsCalculatorAgent,
    ReportGeneratorAgent
)

# Define the state as a TypedDict
class WorkflowState(TypedDict):
    data: Any  # Will hold pandas DataFrame
    error: str
    summary: dict
    raw_data: dict
    file_path: str  # Add file_path to state

def create_workflow(config):
    data_reader = DataReaderAgent()
    ticket_classifier = TicketClassifierAgent(config['model'], config['categories'])
    auto_analyzer = AutomationAnalyzerAgent(config['automation_criteria'])
    savings_calc = SavingsCalculatorAgent(
        config['savings']['hourly_rate'],
        config['savings']['base_processing_time']
    )
    report_gen = ReportGeneratorAgent()

    workflow = StateGraph(WorkflowState)
    workflow.add_node("data_reader", lambda state: data_reader.process(state))
    workflow.add_node("ticket_classifier", lambda state: ticket_classifier.process(state))
    workflow.add_node("automation_analyzer", lambda state: auto_analyzer.process(state))
    workflow.add_node("savings_calculator", lambda state: savings_calc.process(state))
    workflow.add_node("report_generator", lambda state: report_gen.process(state))

    workflow.set_entry_point("data_reader")
    workflow.add_edge("data_reader", "ticket_classifier")
    workflow.add_edge("ticket_classifier", "automation_analyzer")
    workflow.add_edge("automation_analyzer", "savings_calculator")
    workflow.add_edge("savings_calculator", "report_generator")
    workflow.add_edge("report_generator", END)

    app = workflow.compile()
    return app

def run_workflow(workflow, initial_state: Dict[str, Any]):
    result = workflow.invoke(initial_state)
    return result