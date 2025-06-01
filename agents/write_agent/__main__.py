
from server.server import A2AServer

# Models for describing agent capabilities and metadata
from models.agent import AgentCard, AgentCapabilities, AgentSkill

# Task manager and agent logic
from agents.write_agent.task_manager import AgentTaskManager
from agents.write_agent.agent import WriteAgent

# CLI and logging support
import click           # For creating a clean command-line interface
import logging         # For logging errors and info to the console


# -----------------------------------------------------------------------------
# Setup logging to print info to the console
# -----------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Main Entry Function – Configurable via CLI
# -----------------------------------------------------------------------------

@click.command()
@click.option("--host", default="localhost", help="Host to bind the server to")
@click.option("--port", default=10000, help="Port number for the server")
def main(host, port):
    """
    This function sets up everything needed to start the agent server.
    You can run it via: `python -m agents.google_adk --host 0.0.0.0 --port 12345`
    """

    # Define what this agent can do – in this case, it does NOT support streaming
    capabilities = AgentCapabilities(streaming=False)

    # Define the skill this agent offers (used in directories and UIs)
    skill = AgentSkill(
        id="write agent",                                 # Unique skill ID
        name="writting Tool",                          # Human-friendly name
        description="Replies based on user input",    # What the skill does
        tags=["write"],                                  # Optional tags for searching
        examples=["write a message", "write a poem"]  # Example queries
    )

    # Create an agent card describing this agent’s identity and metadata
    agent_card = AgentCard(
        name="WriteAgent",                               # Name of the agent
        description="This agent replies with writting results.",  # Description
        url=f"http://{host}:{port}/",                       # The public URL where this agent lives
        version="1.0.0",                                    # Version number
        defaultInputModes=WriteAgent.SUPPORTED_CONTENT_TYPES,  # Input types this agent supports
        defaultOutputModes=WriteAgent.SUPPORTED_CONTENT_TYPES, # Output types it produces
        capabilities=capabilities,                          # Supported features (e.g., streaming)
        skills=[skill]                                      # List of skills it supports
    )

    # Start the A2A server:
    server = A2AServer(
        host=host,
        port=port,
        agent_card=agent_card,
        task_manager=AgentTaskManager(agent=WriteAgent())
    )

    # Start listening for tasks
    server.start()


# -----------------------------------------------------------------------------
# This runs only when executing the script directly via `python -m`
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
