from langgraph.graph import StateGraph, END
from typing import Dict, Any
from src.agents import (
    DataReaderAgent,
    TicketClassifierAgent,
    AutomationAnalyzerAgent,
    SavingsCalculatorAgent,
    ReportGeneratorAgent
)

# Define the state that will be passed between agents
class WorkflowState:
    def __init__(self):
        self.data = None
        self.error = None
        self.summary = None
        self.raw_data = None

def create_workflow(config):
    # Initialize agents
    data_reader = DataReaderAgent()
    ticket_classifier = TicketClassifierAgent(config['model'], config['categories'])
    auto_analyzer = AutomationAnalyzerAgent(config['automation_criteria'])
    savings_calc = SavingsCalculatorAgent(
        config['savings']['hourly_rate'],
        config['savings']['base_processing_time']
    )
    report_gen = ReportGeneratorAgent()

    # Create workflow graph
    workflow = StateGraph(WorkflowState)

    # Add nodes (agents)
    workflow.add_node("data_reader", lambda state: data_reader.process(state))
    workflow.add_node("ticket_classifier", lambda state: ticket_classifier.process(state))
    workflow.add_node("automation_analyzer", lambda state: auto_analyzer.process(state))
    workflow.add_node("savings_calculator", lambda state: savings_calc.process(state))
    workflow.add_node("report_generator", lambda state: report_gen.process(state))

    # Define edges
    workflow.set_entry_point("data_reader")
    workflow.add_edge("data_reader", "ticket_classifier")
    workflow.add_edge("ticket_classifier", "automation_analyzer")
    workflow.add_edge("automation_analyzer", "savings_calculator")
    workflow.add_edge("savings_calculator", "report_generator")
    workflow.add_edge("report_generator", END)

    # Compile the workflow
    app = workflow.compile()

    return app

def run_workflow(workflow, initial_state: Dict[str, Any]):
    state = WorkflowState()
    state.__dict__.update(initial_state)
    result = workflow.invoke(state)
    return result.__dict__