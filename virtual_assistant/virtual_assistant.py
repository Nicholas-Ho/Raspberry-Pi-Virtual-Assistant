# Set up the following shells in order:

# 1. Run the actions server using 'rasa run actions --port 5055'
# 2. Run the rasa server using 'rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml'

# Then run the virtual_assistant.py script (in yet another shell).


import requests

sender = input("What's your name?\n")

bot_message = ""
while bot_message != "Goodbye!":
	message = input("What's your message?\n")

	print("Sending message now...")

	r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"sender": sender, "message": message})

	print("Bot says, ")
	for i in r.json():
		bot_message = i['text']
		print(f"{i['text']}")