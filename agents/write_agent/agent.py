from datetime import datetime
from crewai import Agent, Task, Crew, LLM

from dotenv import load_dotenv
import os

load_dotenv()

class WriteAgent:
    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self):
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is not set.")

        self.model = LLM(model="gpt-3.5-turbo",
                         temperature=0.2,
                         api_key=os.getenv("OPENAI_API_KEY"))
        
        self._agent = self._build_agent()  
        self._user_id = "write_agent_user"

        self.write_task = Task(
            description=("Receive a user prompt: {user_prompt}.\n"
                         " Analyze the prompt and generate a response based on the user's request."
                         ),
            expected_output=f"The model's output.",
            agent=self._agent
        )

        self.write_crew = Crew(
            agents=[self._agent],
            tasks=[self.write_task],
            verbose=True
        )

        
    def _build_agent(self) -> Agent:
        return Agent(
            role="WriteAgent",
            goal=("WriteAgent is an AI agent that can write text based on user queries. \
                   It can handle various writing tasks and provide responses in a clear and concise manner."),
            backstory=("WriteAgent is designed to assist users with writing tasks. "
                       "It can generate text based on prompts, answer questions, and provide information. \
                       It is capable of understanding context and delivering relevant content."),
            verbose=True,
            allow_delegation=False,
            tools=[],
            llm=self.model
            )


    def invoke(self, query: str, session_id: str) -> str:

        inputs = {"user_prompt": query, "session_id": session_id}
        
        print(f"Inputs {inputs}")   
        
        result = self.write_crew.kickoff(inputs)

        #print(type(result))
        #print(dir(result))

        if hasattr(result, "raw"):
            return result.raw
        else:
            return str(result)





    async def stream(self, query: str, session_id: str):
        """Streaming is not supported by CrewAI."""
        raise NotImplementedError("Streaming is not supported by CrewAI.")