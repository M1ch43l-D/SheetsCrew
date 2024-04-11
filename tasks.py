from datetime import datetime
from crewai import Task


class SheetsTasks():
    def audit_sheet(self, agent):
        return Task(
            description=f'Identify Missing data from the spreadsheet and delegate the correct agent or agents to find the relevant info. The current time is {datetime.now()}.',
            agent=agent,
            async_execution=True,
            expected_output="""A list (or a structured report) indicating the locations (row, column and header) of missing information, along with a timestamp and the recommended the best agent to find the relevant information. 
                Example Output: 
                Missing information at Row: 2, Column: 14, Column Header: 'Persons Twitter', Timestamp: 2024-04-10 18:04:46
                Missing information at Row: 2, Column: 15, Column Header: 'Persons LinkedIn Post 1', Timestamp: 2024-04-10 18:04:46
                Missing information at Row: 2, Column: 16, Column Header: 'Persons LinkedIn Post 2', Timestamp: 2024-04-10 18:04:46
                Missing information at Row: 3, Column: 7, Column Header: 'Departments', Timestamp: 2024-04-10 18:04:46"""
        )

    def research_company_task(self, agent, domain):
        return Task(
            description=f"""Given this website domain: "{domain}".
            Identify the company associated with the domain and provide the company's name 
            along with a 2-3 sentence description of the company.
      """),
      expected_output=dedent(f"""
       The identified company name and a 2-3 sentence description of the company in JSON forma:
       {{
         "company_name": "Company Name",
         "company_description": "Company Description"
       }}

       For example, if you are given airbnb.com, you should return:
       {{
         "company_name": "Airbnb",
         "company_description": "Airbnb is an online platform that allows people to rent out their properties or spare rooms to travelers. It provides a convenient and often more affordable alternative to traditional hotels, offering a wide variety of unique accommodations worldwide. Hosts can list their spaces and set their own prices, while guests can search for and book accommodations based on their preferences and budget."
       }}
      """),
      agent=agent,
    )

  def company_linkedin_task(self, agent, domain, context_tasks):
    return Task(
      description=dedent(f"""Given the company name identified by the Company Researcher 
        and the company's associated domain: "{domain}", find the company's LinkedIn profile URL. 
        
        Execute a web search by passing the following string as the "query" parameter 
        in the Google search tool:
        
        "site:linkedin.com/company/ company_name"
        
        Where company_name is the company name identified by the Company Researcher.

        Then, with the results:
        1. Identify the URL strings with "linkedin.com" as the base URL
        2. Find the URL that is associated to the company being researched.
        3. Return the URL as a string.
        
        If no reliable LinkedIn profile is found, return an empty string "" as the result.
        """),
      expected_output=dedent("""A string wiith the URL of the LinkedIn company profile
        OR an empty string "" if no reliable LinkedIn profile is found. 
        
        Here some examples: 
          - Input: "Airbnb", Output: "https://www.linkedin.com/company/airbnb/"
          - Input: "Citadel", Output: "https://www.linkedin.com/company/citadel-llc/"
          - Input: "CrewAI", Output: "https://www.linkedin.com/company/crewai-inc/"
          
        Keep in mind that you can receive various other companies and domains.

        It is your job to ensure that the returned URL is a valid LinkedIn profile URL 
        and that it is associated to the company being researched.
      """),
        agent=agent,
        context=context_tasks,
        async_execution=True,
    )

  def company_employee_task(self, agent, domain, context_tasks):
    return Task(
      description=dedent(f"""Given the company name identified by the researcher
        and the company's associated domain: "{domain}", find the company's estimated employee range. 
        
        Execute a web search by passing the following string as the "query" parameter 
        in the Google search tool:
        
        "site:linkedin.com/company/ company_name"
        
        Where company_name is the company name identified by the Company Researcher. 

        Then, with the results:
        
        1. Based on the result contents, ensure to look at the data associated to the company being researched.
        2. Look for the string "Company size" and extract the range next to it.
        3. Finally, return the string of the closest range for which the range falls into:
        "1-10"
        "11-50"
        "51-250"
        "251-1K"
        "1K-5K"
        "10K-50K"
        "50K-100K"
        "100K+"
        
        If no reliable result is found, return "1-10" as the estimated employee range.
      """),
      expected_output=dedent("""One of the following strings for the estimated
        number of employees:
          "1-10"
          "11-50"
          "51-250"
          "251-1K"
          "1K-5K"
          "10K-50K"
          "50K-100K"
          "100K+"
      """),
      agent=agent,
      context=context_tasks,
      async_execution=True,
    )

  def company_industry_task(self, agent, domain, context_tasks):
    return Task(
      description=dedent(f"""Given the company name identified by the researcher 
        and the company's associated domain: "{domain}", find the company's estimated employee range. 
        
        Execute a web search by passing the following string as the "query" parameter 
        in the Google search tool:
        
        "site:linkedin.com/company/ company_name"
        
        Where company_name is the company name identified by the Company Researcher. 

        Then, with the results:
        1. Based on the result contents, ensure to look at the data associated to the company being researched.
        2. Look for the string "Industry" and extract the strings next to it.
        3. Finally, return the string of the industry
        
        If no reliable result is found, return "" as the result.
      """),
      expected_output="A string with the related industry of the identified company",
      agent=agent,
      context=context_tasks,
      async_execution=True,
    )

  def revenue_research_task(self, agent, domain, context_tasks):
    return Task(
      description=dedent(f"""Given the company name identified by the researcher
        and the company's associated domain: "{domain}", find the company's estimated employee range. 
        
        Execute a web search by passing the following string as the "query" parameter 
        in the Google search tool:
        
        "company_name annual revenue"
        
        Where company_name is the company name identified by the Company Researcher.

        Then, with the results:
        1. Based on the result contents, ensure to look at the data associated to the company being researched.
        2. Look for the most reliable and recent number associated to the company's annual revenue.
        3. Finally, return the string of the closest range for which the revenue number falls into:
          "$0-$1M"
          "$1M-$10M"
          "$10M-$50M"
          "$50M-$100M"
          "$100M-$250M"
          "$250M-$500M"
          "$500M-$1B"
          "$1B-$10B"
          "$10B+"
        
        If no reliable result is found, return "$0-$1M" as the estimated annual revenue range.
      """),
      expected_output=dedent("""One of the following strings for the estimated annual revenue:
        "$0-$1M"
        "$1M-$10M"
        "$10M-$50M"
        "$50M-$100M"
        "$100M-$250M"
        "$250M-$500M"
        "$500M-$1B"
        "$1B-$10B"
        "$10B+"
      """),
      agent=agent,
      async_execution=True,
      context=context_tasks
    )

    