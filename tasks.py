from datetime import datetime
from crewai import Task
from tools.sheet_tool import GoogleSheetsTool  # Assuming this is your custom tool for Google Sheets operations
from tools.search_tool import SearchTools  # Ensure this is the correct path and class name

class SheetsTasks():
    def __init__(self):
        # Correct tool initialization
        self.sheet_read_tool = GoogleSheetsTool()  
        self.search_tool = SearchTools()  
        self.sheet_write_tool = GoogleSheetsTool()

    def identify_research_task(self, agent, spreadsheet_id, range):
        # Use the correct tool and pass proper context
        return Task(
            description=f'Identify rows with missing information in the Google Sheet as of {datetime.now()} and specify the information that needs to be researched.',
            agent=agent,
            async_execution=True,
            tools=[self.sheet_read_tool],  # Correct tool reference
            context={'spreadsheet_id': spreadsheet_id, 'range': range},  # Pass necessary context for the task
            expected_output="""A structured request for the Researcher, detailing what information needs to be gathered for each missing entry in the Google Sheet. 
            Example Output: 
            [
                {'row': 3, 'data': {'Date': '2024-04-03', 'Summary': 'An overview of AI advancements.'}}, 
                {'row': 7, 'data': {'URL': 'https://example.com/full-article'}}
            ]"""
        )

    def research_task(self, agent, context):
        # Ensure context is correctly passed and used
        return Task(
            description='Conduct research based on the specifics provided by the Sheets Auditor and prepare the findings for sheet update.',
            agent=agent,
            async_execution=True,
            tools=[self.search_tool],  # Correct tool reference
            context=context,  # This context should be the output from the identify_research_task
            expected_output="""A detailed report containing the researched information, structured for easy insertion into the Google Sheet by the Sheets Auditor. 
            Example Output: 
            [
                {'row': 4, 'findings': ['AI advancements include...', 'Recent controversies in AI ethics...']},
                {'row': 7, 'findings': ['Notable upcoming AI conferences include...', 'Emerging AI startups to watch...']}
            ]"""
        )

    def update_sheet_task(self, agent, context):
        # Correctly use the write tool and ensure context is detailed for updates
        return Task(
            description='Update the Google Sheet with the information provided by the Researcher, ensuring each piece of data is placed in the correct row and column.',
            agent=agent,
            async_execution=True,
            tools=[self.sheet_write_tool],  # Correct tool reference
            context=context,  # This context should be the output from the research_task
            expected_output="""Confirmation that the Google Sheet has been updated with all the necessary information in the correct locations. 
            Example Output: 
            'Updated rows 4 and 7 with the researched information. The sheet now contains the latest AI advancements and ethics controversies, as well as upcoming AI conferences and significant AI startups.'"""
        )
