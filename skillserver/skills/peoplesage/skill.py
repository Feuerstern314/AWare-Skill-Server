#import requirements
import json
from fallback import wolfram_Alpha
from app import detect, translate


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



#beginn function, each skill needs to handle the datas
def beginn(data, intents):
	global lang
	#load users data into json
	datas = json.loads(data)
	#load nlu data into json
	intents = json.loads(intents)
	name = getSlotbyName("name",intents)
	if(name == None):
		return False,False
	lang = intents["lang"]
	
	question = "how old is " + name

	answer = wolfram_Alpha(question,data)


	if(answer == False):
		return False
	else:
		return answer
