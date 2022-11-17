# Kris: A Virtual Assistant
A virtual assistant in the vein of Google Home or Amazon Alexa, designed to be uploaded to a Raspberry Pi and do various useful things.

Simply say hello to Kris ('Hello, Kris!') and tell her what you would like to her to help you with ('What's the weather forecast for today?'). Kris will (hopefully) answer with the information you need, or perform the action requested ('Hi Kris, turn on the lights.'). Kris will continue listening to you until you say thanks ('Thank you!') or stop speaking for a while.

This is a personal project and not intended for mass distribution. The virtual assistant is tailored to my requirements and technologies (for instance, a Philips Wiz lightbulb). However, it can easily be adapted to another's needs.

## Tech Stack
The following libraries form the foundation of the virtual assistant:
- Rasa NLP
- Coqui_AI TTS
- Vosk API STT

The virtual assistant is built around Rasa, an NLP chatbot framework for Python (but that works predominantly in YAML files).
- Chatbot behaviour data can be found in the folder `virtual_assistant/rasa/data`. `nlu.yml` stores the training data for the NLP model to recognise user intent. `rules.yml` and `stories.yml` store specific and general rules about the behaviour of the chatbot after user intent has been identified.
- The trained models are stored in `virtual_assistant/rasa/models`.
- `virtual_assistant/rasa/actions/modules` contains the python modules for the functionality of the virtual assistant. See the section *Features* below for a full description of the modules available.

The Rasa assistant (being a text-based chatbot) was wrapped with the Vosk speech-to-text model for input and the Coqui_AI text-to-speech model for output to make the assistant fully audio.
- The Vosk speech-to-text model can be found in `virtual_assistant/stt_module`
- The Coqui_AI text-to-speech model can be found in `virtual_assistant/tts_module`

## Features
The virtual assistant has the following capabilites:
- Provide the headlines for today using News_API (`news_module`)
- Tell the weather forecast for the day using OpenWeatherMap API (`weather_module`)
- Stream music from Spotify using the Spotify Web Playback SDK and Selenium (`spotify_module`)
- Turn on and off a set of Philips Wiz lightbulb (`wizlight_module`)
- Use face recognition to confirm identity (`face_recognition_module`, *to be implemented*)

## Installation
The included `requirements.txt` should contain all the Python libraries required, including Rasa.

However, because of the heavy reliance on APIs, the following API keys must be obtained:
- News_API API key (https://newsapi.org/). A free Developer tier key should be sufficient. Store the key in a file `virtual_assistant/rasa/actions/news_module/secrets/keys.py` as the constant *NEWS_API_KEY*.
- OpenWeatherMap API key (https://openweathermap.org/). A free tier key should be sufficient. Store the key in a file `virtual_assistant/rasa/actions/weather_module/secrets/keys.py` as the constant *OPENWEATHERAPI_KEY*.

One should also have and successfully set-up one or more Philips Wiz lightbulbs (preferably Full Colour). The list *wizlight_ips* in `virtual_assistant/rasa/actions/actions.py` should be updated to include the IP addressses of the lighbulb(s).

### Spotify
A Spotify Premium account and SDK app credentials (https://developer.spotify.com/dashboard/) are required. Follow the steps below:
- Set up a Spotify developer app as shown in the *Set Up Your Account* section at https://developer.spotify.com/documentation/web-playback-sdk/guide/. Store the credentials in a file ``virtual_assistant/rasa/actions/spotify_module/node_web_player/.env` as the constants *SPOTIFY_CLIENT_ID* and *SPOTIFY_CLIENT_SECRET*.
- Encode your Spotify Premium account username and password using the simple Python script below. Store the credentials in a file `virtual_assistant/rasa/actions/spotify_module/python/secrets/keys.py` as the constants *SPOTIFY_USERNAME* and *SPOTIFY_PASSWORD*. In the same file, also store the Fernet key provided by the script as *FERNET_KEY*. (Note: **This is very insecure**, and is only designed to ensure that the credentials cannot be read at a glance. Restrict access to the keys and code, or edit the code to enter the credentials manually on setup)

This is the suggested script for the encoding of the Spotify username and password:
```
from cryptography.fernet import Fernet

key = Fernet.generate_key()
encrypter = Fernet(key)
print('Key: ' + key.decode('utf-8'))

# DELETE WHEN ENCODED
username = ''
password = ''

print('Username: ' + encrypter.encrypt(username.encode('utf-8')).decode('utf-8'))
print('Password: ' + encrypter.encrypt(password.encode('utf-8')).decode('utf-8'))
```

## Setup
Set up the following shells in order:

1. In `/rasa/actions/modules/spotify_module/node_web_player`, enter WSL (if on Windows), activate node.js via nvm then run 'node .' (see `spotify.py` for details)
2. In `/rasa`, run the actions server using 'rasa run actions --port 5055'
3. In `/rasa`, run the rasa server using 'rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml'

Then run the virtual_assistant.py script (in yet another shell).

## Kris...?
The name 'Kris' was chosen because it is easily detected by the speech-to-text model and the text-to-speech model is female (and because it is a nice name). However, should a name change be required (or desired), change the list of *hotwords* in `virtual_assistant/virtual_assistant.py`. To change the voice, edit `virtual_assistant/tts_module/tts_module.py`. A new model might need to be installed. To do so, reference https://github.com/coqui-ai/TTS.

## Additional Notes
Rasa requires numpy<1.20.0 but TTS requires numpy==1.21.6. numpy version 1.21.6 has been installed, and there haven't been any problems with Rasa...yet.

## License
This project is licensed by the GNU Lesser General Public License v2.1.

GNU © Nicholas Ho