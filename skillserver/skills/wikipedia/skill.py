#import requirements
import json
from fallback import wolfram_Alpha
from app import detect, translate
import wikipediaapi
import wikipedia

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
	results = None
	#load users data into json
	datas = json.loads(data)
	#load nlu data into json
	intents = json.loads(intents)
	name = getSlotbyName("name",intents)
	if(name == None):
		return False
	lang = intents["lang"]
	
	wiki_wiki = wikipediaapi.Wikipedia(lang)
	wikipedia.set_lang(lang)
	
	page_py = wiki_wiki.page(name)

	try:
		return wikipedia.summary(name, sentences=4).split("\n\n")[0]
	except:
		pass

	if(page_py.exists()):
		sentences = page_py.summary[0:-1].split(". ")
		answer = ""
		for x in range(3):
			try:
				answer += sentences[x] + ". "
			except:
				pass
		return(answer.split("\n\n")[0])

	try:
		wikipedia.set_lang("en")
		return wikipedia.summary(name, sentences=4).split("\n\n")[0]
	except:
		pass


	if(page_py.exists()):
		wiki_wiki = wikipediaapi.Wikipedia('en')
		page_py = wiki_wiki.page(name)
		sentences = page_py.summary[0:-1].split(". ")
		answer = ""
		for x in range(3):
			try:
				answer += sentences[x] + ". "
			except:
				pass

		return(answer.split("\n\n")[0])

	else:
		return False


	return False
