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

from .modules.weather_module.weather import WeatherModule


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

        residence = next(tracker.get_latest_entity_values(
            entity_type="place",
            entity_role="residence"
        ), None)
        
        if not residence:
            msg = "I didn't get where you lived. Are you sure it's spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
        
        mod = WeatherModule()
        if not mod.check_city(residence):
            msg = f"I didn't recognise {residence}. Are you sure it's spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
        
        residence = residence.title()
        msg = f"Sure thing! I'll remember that you live in {residence}."
        dispatcher.utter_message(text=msg)
        
        return [SlotSet("residence", residence)]

class ActionGetWeather(Action):

    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Check if the user gave a place to check the weather. If not, default to 'residence' slot.
        place = next(tracker.get_latest_entity_values("place"), None)
        if not place: place = tracker.get_slot("residence")
        
        if not place:
            msg = "I'm not sure where you want to check the weather for. Maybe you could give me a place?"
            dispatcher.utter_message(text=msg)
            return []
        
        # Checking
        mod = WeatherModule()
        if not mod.check_city(place):
            msg = f"I didn't recognise {place}. Are you sure it's spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
        
        forecast = mod.get_simple_forecast(city=place)
        if forecast['weather'] == 'Rain':
            forecast['weather'] = 'Rainy'
        elif forecast['weather'] == 'Snow':
            forecast['weather'] = 'Snowy'
        
        msg = f"The weather in {place} is {forecast['weather'].lower()} today, with a temperature high of {forecast['temp_high']} and a low of {forecast['temp_low']} degrees Celsius."
        dispatcher.utter_message(text=msg)
        
        return []