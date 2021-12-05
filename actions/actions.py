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

class GetBooks(Action):

    def name(self) -> Text:
        return "action_get_books"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")
        # print current path
        print(os.getcwd())

        # read json file into pandas dataframe
        df = pd.read_csv('data/books.csv')

        # convert pandaas dataframe to formatted string

        dispatcher.utter_message(text="Hello ! Your schedule is: \n" + df.to_string())

        return []


class GetJurasky(Action):

    def name(self) -> Text:
        return "action_get_jurafsky"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # read json file into pandas dataframe
        df = pd.read_csv('data/Jurafsky.csv')

        # convert pandaas dataframe to formatted string

        dispatcher.utter_message(text="Here are the notes \n" + df.to_string())

        return []

class GetBird(Action):

    def name(self) -> Text:
        return "action_get_bird"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # read json file into pandas dataframe
        df = pd.read_csv('data/Bird.csv')

        # convert pandaas dataframe to formatted string

        dispatcher.utter_message(text="Here are the notes \n" + df.to_string())

        return []

class GetGrading(Action):

    def name(self) -> Text:
        return "action_get_grading"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # print current path
        print(os.getcwd())

        # read text file into an array
        with open('data/Grades.txt', 'r') as myfile:
            data = myfile.readlines()

        # convert pandaas dataframe to formatted string


        dispatcher.utter_message(text="Hello ! Your Grading is: \n" + "".join(data))

        return []

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
            subset_df = deadlines[deadlines['Assessment'].str.contains(assignmentNum) == True]
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
        jurafsky = pd.read_csv('data/Jurafsky.csv')
        bird = pd.read_csv('data/Bird.csv')
        notes.columns = ['Week', 'Chapter', 'Url']
        jurafsky.columns = ['Week', 'Chapter', 'Url']
        bird.columns = ['Week', 'Chapter', 'Url']

        print(notes.columns)
        # check if assignmentNum is a number

        subset_df = pd.DataFrame(columns=['Week', 'Chapter', 'Url'])
        
        for i in range(len(notes)):
            # check if notes['Chapter'] contains the string "chapterName" and filter out the rows
            if chapterName.lower() in notes['Chapter'][i].lower():
                # subset current row into a dataframe
                subset_df = subset_df.append(notes.iloc[i])
                # dispatcher.utter_message(text="Hello " + name + "! The notes for topic " + chapterName + " could be found here: \n" + subset_df.to_string())
            if chapterName.lower() in jurafsky['Chapter'][i].lower():
                # subset current row into a dataframe
                subset_df = subset_df.append(jurafsky.iloc[i])    
            if chapterName.lower() in bird['Chapter'][i].lower():
                subset_df = subset_df.append(bird.iloc[i])
        if len(subset_df) == 0:
            dispatcher.utter_message(text="Hello " + name + "! The notes for topic " + chapterName + " could not be found \n")
            dispatcher.utter_message(text="Showing results for all the notes \n" + subset_df.to_string())
        else:
            dispatcher.utter_message(text="Hello " + name + "! The notes for the given topics are as follows:  \n" + subset_df.to_string())

        return []


class GetNotesTopic(Action):

    def name(self) -> Text:
        return "action_show_note_topics"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # read csv file
        print("reading notes")
        notes = pd.read_csv('data/Notes.csv')
        print("reading jurafsky")
        jurafsky = pd.read_csv('data/Jurafsky.csv')
        print("reading bird")
        bird = pd.read_csv('data/Bird.csv')
        notes.columns = ['Week', 'Chapter', 'Url']
        jurafsky.columns = ['Week', 'Chapter', 'Url']
        bird.columns = ['Week', 'Chapter', 'Url']

        print(notes.columns)
        # check if assignmentNum is a number

        # Extract only chapter column from the dataframe
        notes_chapters = notes['Chapter']
        jurafsky_chapters = jurafsky['Chapter']
        bird_chapters = bird['Chapter']

        dispatcher.utter_message(text="Hello! The following topics are available from class notes: \n" + notes_chapters.to_string())
        dispatcher.utter_message(text="Hello! The following topics are available from jurafsky: \n" + jurafsky_chapters.to_string())
        dispatcher.utter_message(text="Hello! The following topics are available from bird: \n" + bird_chapters.to_string())
        
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