#import requirements
import json
from fallback import wolfram_Alpha
from app import detect, translate

lang = None

def generate_answer(answered):
	global lang
	answered = str(answered)
	answer = None
	if(lang == "de"):
		answer = "Die Antwort lautet: " + answered


	if(answer == None):
		answer = "The answer is: " + answered

	return answer

#beginn function, each skill needs to handle the datas
def beginn(data, intents):
	global lang
	#load users data into json
	datas = json.loads(data)
	#load nlu data into json
	intents = json.loads(intents)
	question = intents["input"]
	lang = intents["lang"]
	if(detect(question) != "en"):
		question = translate(question)


	answer = wolfram_Alpha(question,data)


	if(answer == False):
		return False
	else:
		return generate_answer(answer)
