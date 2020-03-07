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



#beginn function, each skill needs to handle the datas
def beginn(data, intents):
	global lang
	#load users data into json
	datas = json.loads(data)
	#load nlu data into json
	intents = json.loads(intents)
	question = intents["input"]
	lang = intents["lang"]
	
	answer = ""

	appnames = getSlotbyName("appnames",intents)
	quantity = getSlotbyName("quantity",intents)

	if(appnames == None):
		return False

	try:
		with urllib.request.urlopen("https://financialmodelingprep.com/api/v3/search?query=" + urllib.parse.quote(appnames) + "&limit=5=") as url:
					datas = json.loads(url.read().decode())
					for x in datas:
						#print(x["symbol"])
						with urllib.request.urlopen("https://financialmodelingprep.com/api/v3/quote/" + x["symbol"]) as url2:
							datas2 = json.loads(url2.read().decode())
							prices = datas2[0]["price"]
							if(quantity != None):
								prices = prices * float(quantity)
							prices = str(prices)
							price1 = prices.split(".")[0]
							price2 = prices.split(".")[1]
							price2 = price2[0] + price2[1]
							prices = price1 + "." + price2
							answer += x["name"] + ": " + prices + " $\n\n"

	except Exception as e:
		print(e)
		return False

	if(answer != ""):
		return answer
	else:
		return False
