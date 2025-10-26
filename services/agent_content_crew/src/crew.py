import os
from crewai import Crew, Process
from crewai.project import CrewBase, agent, task, crew
from dotenv import load_dotenv

load_dotenv()

os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

@CrewBase
class ContentCrew:
    """ContentCrew class"""
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # The @crew decorator defines the crew process
    @crew
    def create_crew(self):
        return Crew(
            agents=self.agents,  # self.agents and self.tasks are loaded from the YAMLs
            tasks=self.tasks,
            process=Process.sequential,
            verbose=2
        )