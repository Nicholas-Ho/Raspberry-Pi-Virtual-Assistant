# Instructions for setup (Windows)
# 1. Start WSL.
# 2. Check the version of node.js with 'nvm list'. Use 'nvm use <node version>' to start node.
# 3. Run this python file (or run Rasa action server)

import os, sys

from cryptography.fernet import Fernet

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import chromedriver_binary

from time import sleep

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

# Handling of relative import
if __name__ == "__main__":
    sys.path.append(DIR_PATH)
    from secrets.keys import SPOTIFY_USERNAME, SPOTIFY_PASSWORD, FERNET_KEY
else:
    from .secrets.keys import SPOTIFY_USERNAME, SPOTIFY_PASSWORD, FERNET_KEY

class SpotifyModule:

    def __init__(self):
        self.driver = webdriver.Chrome()
        driver = self.driver
        
        driver.get("http://localhost:3000/auth/login")

        # Decrypt username and password
        decrypter = Fernet(FERNET_KEY)

        # Find and enter the username and password

        user_field = driver.find_element(By.ID, 'login-username')
        if user_field:
            user_field.clear()
            user_field.send_keys(decrypter.decrypt(SPOTIFY_USERNAME.encode('utf-8')).decode('utf-8'))

        pw_field = driver.find_element(By.ID, 'login-password')
        if pw_field:
            pw_field.clear()
            pw_field.send_keys(decrypter.decrypt(SPOTIFY_PASSWORD.encode('utf-8')).decode('utf-8'))
            pw_field.send_keys(Keys.RETURN)

        # Wait for the redirect to complete
        sleep(2)

        # Prepare for test
        print('Connect the account to the Web Playback SDK (using another device), then click the button twice.')
        sleep(10)

    def close_driver(self):
        self.driver.close()

    def toggle_play(self):
        self.driver.execute_script('webPlayer.togglePlay();')

    def play(self):
        self.driver.execute_script('play();')

    def pause(self):
        self.driver.execute_script('pause();')

    def play_song(self, track, artist=None):
        if artist:
            self.driver.execute_script(f'playSong("{track}", "{artist}");')
        else:
            self.driver.execute_script(f'playSong("{track}");')