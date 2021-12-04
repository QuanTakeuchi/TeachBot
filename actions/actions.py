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
                return []
            else:
                dispatcher.utter_message(text="Hello " + name + "! The deadlines are as follows: \n" + deadlines.to_string())
                return []
        else:
            subset_df = deadlines[deadlines['Assessment'].str.contains("assignmentNum") == True]
            dispatcher.utter_message(text="Hello " + name + "! The deadlines are as follows: \n" + subset_df.to_string())
                          
        dispatcher.utter_message(text="Hello " + name + "! The assignment details are incorrect \n" )   

        return []

class GetNotes(Action):

    def name(self) -> Text:
        return "action_get_notes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")
        chapterName = tracker.get_slot("chapterName")
        print(chapterName)

        # read csv file
        notes = pd.read_csv('data/Notes.csv')
        notes.columns = ['Week', 'Chapter', 'Url']
        print(notes.columns)
        # check if assignmentNum is a number
        for i in range(len(notes)):
            # check if notes['Chapter'] contains the string "chapterName" and filter out the rows
            if chapterName.lower() in notes['Chapter'][i].lower():
                dispatcher.utter_message(text="Hello " + name + "! The notes for topic " + chapterName + " could be found here: \n" + notes['Url'][i])
                return []
        dispatcher.utter_message(text="Hello " + name + "! There are no notes for the topic " + chapterName + ".")

        return []

class GetMiniTalk(Action):

    def name(self) -> Text:
        return "action_mini_talk"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")
        lastName = tracker.get_slot("last_name")
        minitalkCategory = tracker.get_slot("minitalkCategory")
        fullName = lastName+","+name
        print(fullName)
        print(minitalkCategory)

        # read csv file
        minitalk = pd.read_csv('data/minitalk.csv')
        minitalk.columns = ['Week', 'Presenter', 'Questioner 1', 'Questioner 2']
        print(minitalk.columns)

        # empty data frame
        minitalk_df = pd.DataFrame(columns=['Week', 'Presenter', 'Questioner 1', 'Questioner 2'])

        # check if assignmentNum is a number
        for i in range(len(minitalk)):
            if minitalkCategory == "Presenter":
                if fullName.lower() in minitalk['Presenter'][i].lower():
                    minitalk_df = minitalk_df.append(minitalk.iloc[[i]], ignore_index=True)
            elif minitalkCategory == "Questioner":
                if fullName.lower() in minitalk['Questioner 1'][i].lower() or fullName.lower() in minitalk['Questioner 2'][i].lower():
                    minitalk_df = minitalk_df.append(minitalk.iloc[[i]], ignore_index=True)
            else:
                if fullName.lower() in minitalk['Presenter'][i].lower() or fullName.lower() in minitalk['Questioner 1'][i].lower() or fullName.lower() in minitalk['Questioner 2'][i].lower():
                    minitalk_df = minitalk_df.append(minitalk.iloc[[i]], ignore_index=True)
        dispatcher.utter_message(text="Hello " + name + "! The minitalk details are as follows: \n" + minitalk_df.to_string())
        return []