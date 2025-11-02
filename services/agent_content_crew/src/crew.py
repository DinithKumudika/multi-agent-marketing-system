import os
from crewai import Crew, Process
from crewai.project import CrewBase, crew, agent, task

from .config.settings import settings

os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY.get_secret_value()

if settings.GEMINI_API_KEY:
    os.environ["GEMINI_API_KEY"] = settings.GEMINI_API_KEY.get_secret_value()

if settings.OPENAI_API_KEY:
    os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY.get_secret_value()


class ValidationCrew:
    """
    The Market Validation Crew.
    This crew takes the initial brief and returns a validation report.
    """
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # Define the agents and tasks this crew uses
    @agent
    def validator(self):
        from crewai.agent import Agent  # Local import
        return Agent(config=self.agents_config['validator'])

    @task
    def validation_task(self):
        from crewai.task import Task  # Local import
        return Task(config=self.tasks_config['validation_task'])

    @crew
    def create_crew(self):
        return Crew(
            agents=[self.validator()],
            tasks=[self.validation_task()],
            process=Process.sequential,
            verbose=2,
        )

@CrewBase
class ContentCrew:
    """
    The Content Generation Crew.
    This crew assumes validation has passed and executes the full
    research, writing, and editing pipeline.
    """
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # Define the agents this crew uses
    @agent
    def researcher(self):
        from crewai.agent import Agent
        return Agent(config=self.agents_config['researcher'])

    @agent
    def copywriter(self):
        from crewai.agent import Agent
        return Agent(config=self.agents_config['copywriter'])

    @agent
    def editor(self):
        from crewai.agent import Agent
        return Agent(config=self.agents_config['editor'])

    # Define the tasks this crew uses
    @task
    def research_task(self):
        from crewai.task import Task
        return Task(config=self.tasks_config['research_task'])

    @task
    def writing_task(self):
        from crewai.task import Task
        return Task(config=self.tasks_config['writing_task'])

    @task
    def editing_task(self):
        from crewai.task import Task
        return Task(config=self.tasks_config['editing_task'])

    # The @crew decorator defines the crew process
    @crew
    def create_crew(self):
        return Crew(
            agents=[self.researcher(), self.copywriter(), self.editor()],  # self.agents and self.tasks are loaded from the YAMLs
            tasks=[self.research_task(), self.writing_task(), self.editing_task()],
            process=Process.sequential,
            verbose=2
        )