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

service_account_file = os.getenv('SERVICE_ACCOUNT_FILE')

# Initialize the agents and tasks
agents = SheetsCrew()
tasks = SheetsTasks()

# Initialize the OpenAI GPT-4 language model
Mixtral = ChatOpenAI(
    model="Mixtral"
)

# Instantiate the agents
sheets_auditor_agent = agents.sheets_auditor_agent()
researcher_agent = agents.researcher_agent()

# Instantiate the tasks
identify_research_task = tasks.identify_research_task(sheets_auditor_agent)
research_task = tasks.research_task(researcher_agent)
update_sheet_task = tasks.update_sheet_task(sheets_auditor_agent)

spreadsheet_id = 'spreadsheet_id'

crew = Crew(
    agents=[sheets_auditor_agent, researcher_agent],
    tasks=[identify_research_task, research_task, update_sheet_task],
    process=Process.sequential,
    manager_llm=Mixtral,
    verbose=2
)

# Kick off the crew's work
results = crew.kickoff(inputs={'spreadsheet_id': spreadsheet_id})
print(results)