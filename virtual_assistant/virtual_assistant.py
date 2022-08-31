# Set up the following shells in order:

# 1. In /rasa, run the actions server using 'rasa run actions --port 5055'
# 2. In /rasa, run the rasa server using 'rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml'

# Then run the virtual_assistant.py script (in yet another shell).


import requests
from stt_module.stt_module import STTModule
from tts_module.tts_module import TTSModule

class VirtualAssistant:

	# Conda environment containing rasa installation
	CONDA_ENV = 'raspberry-pi'

	# Virtual assistant hotwords ('Hey google'?)
	hotwords = ['hello diana', 'hey diana']

	# Wait length for listening session
	wait_length = 50

	def __init__(self):
		self.stt_mod = STTModule()
		self.tts_mod = TTSModule()

		# Test if Rasa is running on port 5002
		sender = 'test'
		try:
			r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"sender": sender, "message": 'testing'})
		except:
			raise ConnectionError('Rasa assistant is not running on port 5002. Are you sure Rasa has been configured correctly?')

	def send_message(self, message):
		sender = 'user'

		r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"sender": sender, "message": message})

		output = []
		for i in r.json():
			output.append(i['text'])
		
		return output

	def start(self):
		print('Virtual assistant started! Press CTRL+C to exit.\nSpeak!')

		try:
			while True:
				msg = self.stt_mod.listen_hotword(hotwords=self.hotwords, break_after=True, headless=True)
				print(msg)
				output = self.send_message(msg)
				for sentence in output:
					print(sentence)
					self.tts_mod.speak(sentence)

				self.start_listen_session()
		except KeyboardInterrupt:
			print('\nDone')
		except Exception as e:
			print(e)

	# Start a listening session triggered after a hotword has been spoken (so the hotword doesn't need to be said again)
	def start_listen_session(self):
		msg = '_'
		while True:
			msg = self.stt_mod.listen(wait_length=self.wait_length, break_after=True, headless=True)
			print(msg)

			if msg != '':
				output = self.send_message(msg)
				for sentence in output:
					print(sentence)
					self.tts_mod.speak(sentence)
			else:
				break

if __name__ == '__main__':
	assistant = VirtualAssistant()
	assistant.start()