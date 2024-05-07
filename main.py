from SheetsCrew import SheetsCrew
import datetime


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'current_date': datetime.datetime.now().strftime("%Y-%m-%d"),
        'Instagram_description': input('Enter the page description here: '),
        'topic_of_the_week': input('Enter the topic of the week here: '),
    }
    SheetsCrew().crew().kickoff(inputs=inputs)