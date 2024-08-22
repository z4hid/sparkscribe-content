from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
# Uncomment the following line to use an example of a custom tool
# from sparkscribe_content.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool


os.environ["OPENAI_API_KEY"] = "NA"


from langchain.llms import Ollama

llm = Ollama(
    model = "mistral-nemo",
    base_url = "http://localhost:11434",
    num_gpu=-1,
    num_predict=-1, #infinite generation
    num_thread=4,
    temperature=0.1,
    # max_tokens=8192,
    )


@CrewBase
class SparkscribeContentCrew():
	"""SparkscribeContent crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			llm=llm,
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True,
			llm=llm,
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			agent=self.researcher()
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			agent=self.reporting_analyst(),
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the SparkscribeContent crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)