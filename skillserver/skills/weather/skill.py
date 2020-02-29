#import requirements
import urllib.request, json
from datetime import datetime
import urllib.parse


lang = None

def generate_answer(weather,temp):
	global lang
	weather = str(weather)
	temp = str(int(temp))
	answer = None
	if(lang == "de"):
		answer = weather + " mit etwa " + temp + " Grad"


	if(answer == None):
		answer = weather + " with circa " + temp + " degrees"

	return answer





#beginn function, each skill needs to handle the datas
def beginn(data, intents):
	global lang
	location = None
	time = None
	datas = None
	answer = ""
	#load users data into json
	data = json.loads(data)
	#load nlu data into json
	intents = json.loads(intents)
	#get intention name
	intention = intents["intent"]["intentName"]
	slots = intents["slots"]
	lang = intents["lang"]
	apikey = data["owmapi"]



	try:
		for x in slots:
			if x["slotName"] == "city":
				location = x["value"]["value"]

			if x["slotName"] == "datetime":
				time = x["value"]["value"]
				time = time.split(" ")[0]
			
			
	except Exception as e:
		print(e)
		# return false, so the server can try to use fallback skills to generate an answer
		return False

	if(location == None):
		return False


	location = urllib.parse.quote(location)


	try:	

		if(time == None):
			with urllib.request.urlopen("https://api.openweathermap.org/data/2.5/weather?q=" + location + "&appid=" + apikey + "&units=metric&lang=" + lang) as url:
				datas = json.loads(url.read().decode())


			answer = generate_answer(datas["weather"][0]["description"],datas["main"]["temp"])

			return answer


		else:
			with urllib.request.urlopen("https://api.openweathermap.org/data/2.5/forecast?q=" + location + "&appid=" + apikey + "&units=metric&lang=" + lang) as url:
				datas = json.loads(url.read().decode())


			for x in datas["list"]:
				if(x["dt_txt"].split(" ")[0] == time and x["dt_txt"].split(" ")[1] == "15:00:00"):
					answer = generate_answer(x["weather"][0]["description"],str(int(x["main"]["temp_min"])))
					return answer

		return False


	except Exception as e:
		print(e)
		return False


	#at least one return (no in, if or try) statement has to be not indented
	#this statement is not executed. Necessary for python interpreter tho.
	return str(intents)
