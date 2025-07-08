#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from mcp_agent_n8n_ia.crew import McpAgentN8NIa

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run(nome: str = "processos_executados"):
    """
    Run the crew.
    """
    inputs = {'nome': nome}
    
    try:

        # Initialize the ComplianceCrew
        crew_instance = McpAgentN8NIa()

        result = crew_instance.crew().kickoff(inputs=inputs)
        #inputs={"question": "What city does John live in and how old is he?"}
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

    return result

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        McpAgentN8NIa().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        McpAgentN8NIa().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        McpAgentN8NIa().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
