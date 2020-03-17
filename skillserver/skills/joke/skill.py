#import requirements
import json
import random

lang = None


def generate_answer(intent, url):
	global lang
	answer = None
	
	Random = random.randrange(1, 50)	
	
	with open(url, 'r') as json_file:
		reader = json.load(json_file)
		for row in reader:
			if(row['id'] == Random):
				answer = row['body']
				break
			else:
				continue

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
	url = "skills//joke//jokes//"	
	
	if(lang == "de"):
		url += "de//"
		if(intention == "jokes_blonde"):
			url += "blonde_jokes.json"
		else:
			url += "funny_jokes.json"


	else:
		url += "en//"
		if(intention == "jokes_blonde"):
			url += "blonde_jokes.json"
		else:
			url += "funny_jokes.json"	

	
	return generate_answer(intention, url),"https://a-ware.io/wp-content/uploads/2020/02/LOGO.png"
	

	
