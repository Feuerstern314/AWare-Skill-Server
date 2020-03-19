#import requirements
import json

lang = None


def generate_answer(intent):
	global lang
	answer = None
	if(lang == "de"):
		if(intent == "thanks"):
			answer = "Gern geschehen"

		if(intent == "shutup"):
			answer = "     "




	if(answer == None):
		if(intent == "thanks"):
			answer = "Please"

		if(intent == "shutup"):
			answer = "     "


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
	

	
