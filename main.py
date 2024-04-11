import os
import openai
from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from agents import SheetsCrew
from tasks import SheetsTasks
from file_io import save_markdown
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = "NULL"
os.environ["openai_api_base"] = "http://localhost:1234/v1"

# Initialize the agents and tasks
agents = SheetsCrew()
tasks = SheetsTasks()

# Initialize the OpenAI GPT-4 language model
Mixtral = ChatOpenAI(
    model="Mixtral"
)


# Instantiate the agents
editor = agents.editor_agent()
news_fetcher = agents.news_fetcher_agent()
news_analyzer = agents.news_analyzer_agent()
newsletter_compiler = agents.newsletter_compiler_agent()

# Instantiate the tasks
fetch_news_task = tasks.fetch_news_task(news_fetcher)
analyze_news_task = tasks.analyze_news_task(news_analyzer, [fetch_news_task])
compile_newsletter_task = tasks.compile_newsletter_task(
    newsletter_compiler, [analyze_news_task], save_markdown )

# Form the crew
crew = Crew(
    agents=[editor, news_fetcher, news_analyzer, newsletter_compiler],
    tasks=[fetch_news_task, analyze_news_task, compile_newsletter_task],
    process=Process.hierarchical,
    manager_llm=Mixtral,
    verbose=2
)

# Kick off the crew's work
results = crew.kickoff()

# Print the results
print("Crew Work Results:")
print(results)