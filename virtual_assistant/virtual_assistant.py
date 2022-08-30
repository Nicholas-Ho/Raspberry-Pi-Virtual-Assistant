# Set up the following shells in order:

# 1. Run the actions server using 'rasa run actions --port 5055'
# 2. Run the rasa server using 'rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml'

# Then run the virtual_assistant.py script (in yet another shell).


import requests
from stt_module.stt_module import STTModule
#from tts_module.tts_module import TTSModule

class VirtualAssistant():

	# Conda environment containing rasa installation
	CONDA_ENV = 'raspberry-pi'

	# Virtual assistant hotwords ('Hey google'?)
	hotwords = ['hello diana', 'hey diana']

	def __init__(self):
		self.stt_mod = STTModule()
		#self.tts_mod = TTSModule()

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
				output = self.send_message(msg)
				print(output)
		except KeyboardInterrupt:
			print('\nDone')
		except Exception as e:
			print(e)

if __name__ == '__main__':
	assistant = VirtualAssistant()
	assistant.start()