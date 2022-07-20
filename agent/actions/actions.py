# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


def interpret_answer(intent: str) -> bool:
    # Helper method to go from intent name to boolean
    if intent == "Affirm":
        return True
    elif intent == "Deny":
        return False
    else:
        # unknown case
        return False


class CollectSymptomsAction(Action):
    # The symptoms are summarized in a binary array.
    # 13 possible symptoms, 6 mild, 7 severe
    # order:
    # 0: annoyance
    # 1: anxious
    # 2: motivation
    # 3: focus
    # 4: sleep
    # 5: physical state
    #
    # 6: feeling like yourself
    # 7: panic attacks
    # 8: depression
    # 9: anger episodes
    # 10: loss of control
    # 11: guilt
    # 12: shame

    def name(self) -> Text:
        return "action_collect_symptoms"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("Running collection")
        # Get the current list of symptoms
        symptoms = tracker.get_slot(key="symptoms")

        intent = tracker.get_intent_of_latest_message()

        # The user just told about a symptom
        if "tell_symptom" in intent:
            print("entering symptom: " + intent)

            # check symptom, then return
            if "annoyance" in intent:
                symptoms[0] = 1
            elif "anxiety" in intent:
                symptoms[1] = 1
            elif "motivation" in intent:
                symptoms[2] = 1
            elif "focus" in intent:
                symptoms[3] = 1
            elif "sleep" in intent:
                symptoms[4] = 1
            else:
                print("Symptom not supported yet: " + intent)
            print(symptoms)
            return [SlotSet(key="symptoms", value=symptoms)]

        question = tracker.latest_action_name

        print("Check question asked")
        # The bot just asked after a specific symptom
        if question == "ask_sleep":
            if interpret_answer(intent):
                # add
                symptoms[4] = 1
            else:
                # remove
                symptoms[4] = 0
        elif question == "ask_focus":
            if interpret_answer(intent):
                # add
                symptoms[3] = 1
            else:
                # remove
                symptoms[3] = 0
        else:
            # no relevant question provided
            print(symptoms)
            return []

        print(symptoms)

        return [SlotSet(key="symptoms", value=symptoms)]


class DetermineSeverityAction(Action):

    def name(self) -> Text:
        return "action_determine_severity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the list of symptoms
        symptoms = tracker.get_slot(key="symptoms")

        mild = sum(symptoms[0:5])
        severe = sum(symptoms[6:])

        # Determine symptom severity so far
        severity = "green"
        if severe > 3:
            severity = "red"
        elif severe > 0:
            severity = "orange"
        elif mild > 1:
            severity = "yellow"

        return [SlotSet(key="severity", value=severity)]
