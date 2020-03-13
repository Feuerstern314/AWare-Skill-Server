#import requirements
import json

lang = None


def generate_answer(intent):
	global lang
	answer = None
	if(lang == "de"):
		if(intent == "parents"):
			answer = "Ich wurde von dem Aware Team erschaffen"

		if(intent == "creationtime"):
			answer = "Ich bin 2020 auf die Welt gekommen"




	if(answer == None):
		if(intent == "parents"):
			answer = "I was created by the Aware Team"

		if(intent == "creationtime"):
			answer = "I saw the world first time in 2020"


	return answer

#beginn function, each skill needs to handle the datas
def beginn(data, intents):
	global lang
	#load users data into json
	datas = json.loads(data)
	#load nlu data into json
	intents = json.loads(intents)
	intention = intents["intent"]["intentName"]
	lang = intents["lang"]
	
	return generate_answer(intention),"https://a-ware.io/wp-content/uploads/2020/02/LOGO.png"
	

	
