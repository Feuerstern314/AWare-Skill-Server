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



def generate_answer():
	global lang
	answer = None
	if(lang == "de"):
		answer = "Hier sind Bilder "


	if(answer == None):
		answer = "Here are images "

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

	things = getSlotbyName("things",intents)

	if(things == None):
		return generate_answer()

	return generate_answer(),"https://searx.info/?q=" + urllib.parse.quote(things) + "&categories=images"
