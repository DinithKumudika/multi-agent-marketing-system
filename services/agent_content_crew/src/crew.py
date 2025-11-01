import os
from crewai import Crew, Process
from crewai.project import CrewBase, crew

from .config.settings import settings

os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY.get_secret_value()

if settings.GEMINI_API_KEY:
    os.environ["GEMINI_API_KEY"] = settings.GEMINI_API_KEY.get_secret_value()

if settings.OPENAI_API_KEY:
    os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY.get_secret_value()

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