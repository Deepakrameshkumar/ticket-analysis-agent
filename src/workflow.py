from langgraph import Graph
from src.agents import *

def create_workflow(config):
    # Initialize agents
    data_reader = DataReaderAgent()
    ticket_classifier = TicketClassifierAgent(
        config['model']['path'], 
        config['categories']
    )
    auto_analyzer = AutomationAnalyzerAgent(config['automation_criteria'])
    savings_calc = SavingsCalculatorAgent(
        config['savings']['hourly_rate'],
        config['savings']['base_processing_time']
    )
    report_gen = ReportGeneratorAgent()
    
    # Create workflow
    workflow = Graph()
    workflow.add_node(data_reader)
    workflow.add_node(ticket_classifier)
    workflow.add_node(auto_analyzer)
    workflow.add_node(savings_calc)
    workflow.add_node(report_gen)
    
    # Define edges
    workflow.add_edge(data_reader, ticket_classifier)
    workflow.add_edge(ticket_classifier, auto_analyzer)
    workflow.add_edge(auto_analyzer, savings_calc)
    workflow.add_edge(savings_calc, report_gen)
    
    return workflow