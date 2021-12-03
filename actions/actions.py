# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd

import os

class GetSchedule(Action):

    def name(self) -> Text:
        return "action_get_schedule"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")
        # print current path
        print(os.getcwd())

        # read csv file
        schedule = pd.read_csv('data/schedule.csv')

        # convert pandaas dataframe to formatted string


        dispatcher.utter_message(text="Hello " + name + "! Your schedule is: \n" + schedule.to_string())

        return []

class GetHolidays(Action):

    def name(self) -> Text:
        return "action_get_holidays"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")
        # print current path
        print(os.getcwd())

        # read csv file
        schedule = pd.read_csv('data/schedule.csv')

        # change header names
        schedule.columns = ['Week', 'Date', 'Content']
        # convert pandaas dataframe to formatted string

        # check if schedule['Content'] contains the string "no class" and filter out the rows
        holiday_df = schedule[schedule['Content'].str.contains("No Class") == True]


        dispatcher.utter_message(text="Hello " + name + "! There is no Class on: \n" + holiday_df.to_string())

        return []

class GetDeadlines(Action):

    def name(self) -> Text:
        return "action_get_deadlines"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")
        assignmentNum = tracker.get_slot("assignmentNum")
        print(assignmentNum)
        # print current path
        print(os.getcwd())

        # read csv file
        deadlines = pd.read_csv('data/deadlines.csv')
        deadlines.columns = ['No', 'Assessment', 'Due Date (11:59 PM EST of the day)']
        print(deadlines.columns)
        # check if assignmentNum is a number
        if assignmentNum.isdigit():
            if int(assignmentNum) > 0:
                subset_df = deadlines[deadlines['Assessment'].str.contains("Assignment "+assignmentNum) == True]
                dispatcher.utter_message(text="Hello " + name + "! The deadline for Assignment " + assignmentNum + " is: \n" + subset_df.to_string())
            else:
                dispatcher.utter_message(text="Hello " + name + "! The deadlines are as follows: \n" + deadlines.to_string())
        else:
            dispatcher.utter_message(text="Hello " + name + "! The deadlines are as follows: \n" + deadlines.to_string())

        return []
