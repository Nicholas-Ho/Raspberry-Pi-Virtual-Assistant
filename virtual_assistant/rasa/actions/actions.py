# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from .modules.weather_module.weather import WeatherModule
from .modules.news_module.news import NewsModule
from .modules.spotify_module.python.spotify import SpotifyModule
# from .modules.utils import convert_iso_2_to_country

# Initialise the Spotify Module
spotify_module = SpotifyModule()

class ActionUtterResidence(Action):

    def name(self) -> Text:
        return "action_utter_residence"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        residence = tracker.get_slot("residence_city")

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
            entity_type="GPE"
        ), None)
        
        if not residence:
            msg = "I didn't get where you lived. Are you sure it's spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
        
        mod = WeatherModule()
        if not mod.check_city(residence):
            msg = f"I didn't recognise {residence}. Are you sure it's a city?"
            dispatcher.utter_message(text=msg)
            return []
        
        residence = residence.title()
        msg = f"Sure thing! I'll remember that you live in {residence}."
        dispatcher.utter_message(text=msg)

        country = mod.get_country_iso_2_from_city(residence)
        # country = convert_iso_2_to_country(country) # Seems like there isn't a need to convert from ISO Alpha-2
        
        return [SlotSet("residence_city", residence), SlotSet("residence_country", country)]

class ActionGetWeather(Action):

    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Check if the user gave a city to check the weather. If not, default to 'residence' slot.
        city = next(tracker.get_latest_entity_values("city"), None)
        if not city: city = tracker.get_slot("residence_city")
        
        if not city:
            msg = "I'm not sure where you want to check the weather for. Maybe you could give me a place?"
            dispatcher.utter_message(text=msg)
            return []
        
        # Checking
        mod = WeatherModule()
        if not mod.check_city(city):
            msg = f"I didn't recognise {city}. Are you sure it's spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
        
        forecast = mod.get_simple_forecast(city=city)
        
        msg = f"The weather in {city} is {forecast['weather'].lower()} today, with a temperature high of {forecast['temp_high']} and a low of {forecast['temp_low']} degrees Celsius."
        dispatcher.utter_message(text=msg)
        
        return []

class ActionGetNews(Action):

    def name(self) -> Text:
        return "action_get_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Check if the user gave a news category. If not, default to 'general'.
        category = next(tracker.get_latest_entity_values("news_category"), None)
        
        # Checking
        mod = NewsModule()
        if category:
            if not category in mod.CATEGORIES:
                msg = f"I didn't recognise {category}. Are you sure it's spelled correctly?"
                dispatcher.utter_message(text=msg)
                return []
            else:
                headlines = mod.get_headline_titles(category=category)
        else:
            headlines = mod.get_headline_titles_by_source(source='bbc-news')
        
        msg = "Here are the headlines for today!"
        dispatcher.utter_message(text=msg)
        for headline in headlines:
            dispatcher.utter_message(headline)
        msg = "That's it with the news for now!"
        dispatcher.utter_message(text=msg)
        
        return []

class ActionPlayMusic(Action):

    def name(self) -> Text:
        return "action_play_music"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        msg = "Playing music!"
        dispatcher.utter_message(text=msg)

        spotify_module.play()
        
        return []

class ActionPauseMusic(Action):

    def name(self) -> Text:
        return "action_pause_music"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        msg = "Pausing music!"
        dispatcher.utter_message(text=msg)

        spotify_module.pause()
        
        return []

class ActionPlaySong(Action):

    def name(self) -> Text:
        return "action_play_song"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get song (and artist if available)
        song = next(tracker.get_latest_entity_values("song"), None)
        artist = next(tracker.get_latest_entity_values("music_artist"), None)

        if song:
            msg = f"Playing {song}"
            if artist: msg += f" by {artist}"

            spotify_module.play_song(song, artist)
        else:
            msg = "No song provided!"
        dispatcher.utter_message(text=msg)
        
        return []