#import requirements
import json
from fallback import wolfram_Alpha
from app import detect, translate
import urllib.request, json
import urllib.parse

lang = None

def getSlotbyName(slotname, datas):
	try:
		slots = datas["slots"]
		for x in slots:
			if x["slotName"] == slotname:
				return x["value"]["value"]

		return None

			
	except Exception as e:
		print(e)
		return None



def generate_answer(appnames):
	global lang
	answer = None
	if(lang == "de"):
		answer = "Ich versuche " + appnames + " für dich zu öffnen"


	if(answer == None):
		answer = "I try to open " + appnames + " for you"

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
	
	song = ""

	appnames = getSlotbyName("appnames",intents)

	if(appnames == None):
		return False

	return generate_answer(appnames)
