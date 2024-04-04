from crewai import Agent
from tools.search_tool import SearchTools
from tools.browser_tool import BrowserTools
from tools.calculator_tool import CalculatorTools
from tools.sheet_tool import GoogleSheetsTool
from crewai_tools import BaseTool
from crewai_tools import SerperDevTool

class SheetsCrew():
    def sheets_auditor_agent(self):
        # Initialize an instance of GoogleSheetsTool
        google_sheets_tool = GoogleSheetsTool()
        return Agent(
            role='Sheets Auditor',
            goal='Identify missing cells row by row and tell researcher to find the info and update missing information in the Google Sheet',
            verbose=True,
            memory=True,
            backstory="A meticulous auditor who not only identifies gaps in data but also fills them.",
            tools=[google_sheets_tool],  # Pass the instance of the tool, not the method
            allow_delegation=True
        )

    def researcher_agent(self):
        # Initialize instances of the tools
        search_tools = SearchTools()
        calculator_tools = CalculatorTools()
        return Agent(
            role='Lead Researcher',
            goal='Research and scrape the internet to find missing information to pass back to the sheets manager',
            verbose=True,
            memory=True,
            backstory='A savvy researcher skilled in navigating the vast information on the internet.',
            tools=[SearchTools.search_internet],
            allow_delegation=True
        )

search_tool = SerperDevTool()

# Initialize the agent with advanced options
agent = Agent(
  role='Research Analyst',
  goal='Provide up-to-date market analysis',
  backstory='An expert analyst with a keen eye for market trends.',
  tools=[search_tool],
  memory=True, # Enable memory
  verbose=True,
  max_rpm=None, # No limit on requests per minute
  max_iter=15, # Default value for maximum iterations
  allow_delegation=False
)