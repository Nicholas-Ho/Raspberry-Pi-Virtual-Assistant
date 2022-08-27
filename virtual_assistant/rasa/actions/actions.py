# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from .modules.weather_module.weather import get_simple_forecast


class ActionUtterResidence(Action):

    def name(self) -> Text:
        return "action_utter_residence"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        residence = tracker.get_slot("residence")

        if not residence:
            dispatcher.utter_message(text="I don't know where you live. Maybe you could tell me?")
            return []
        else:
            msg = "You live in " + residence + "!"
            dispatcher.utter_message(text=msg)
            return []

class ActionRememberResidence(Action):

    def name(self) -> Text:
        return "action_remember_residence"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        residence = next(tracker.get_latest_entity_values("residence"), None)
        
        if not residence:
            msg = "I didn't get where you lived. Are you sure it's spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
        
        residence = residence.title()
        msg = f"Sure thing! I'll remember that you live in {residence}."
        dispatcher.utter_message(text=msg)
        
        return [SlotSet("residence", residence)]