# coding=UTF-8
#!/usr/bin/env python3

import urllib.parse
import urllib.request
import json
import wolframalpha
import requests as req
from pandas import DataFrame
import pandas as pd
import os.path
from fallbacks.GoogleAnswers import ask as askGoogle


def duckduckgo(text):
	print("asked duckduckgo")
	text = urllib.parse.quote(text)
	response = urllib.request.urlopen("https://api.duckduckgo.com/?q=" + text + "&format=json&pretty=1")
	try:
		datas = json.loads(response.read())
		answer = datas["AbstractText"]
		if(answer == ""):
			answer = False
		return answer
	except Exception as e:
		print(e)
		return False
	


def google(text,data, language = "en"):
	
	gl = language
	text = text.replace("?","")
	if(language == "en"):
		gl = "us"
		
	first_question = None

	df = None
	df2 = None
	answer = None
	answer_url = None
	

	datas = json.loads(data)

	params = {
	'api_key': datas["serpstack_api"],
	'q': text,
	'hl': language,
	'gl': gl
	}

	
	answer = str(askGoogle(text,language))

	if(answer != "Error"):
		print("Answered by google")
		from searxapi import callAPI
		answer_url = callAPI(text,language)
		return answer,answer_url
	
	answer = None

	api_result = req.get('https://api.scaleserp.com/search', params)
	
	print("asked google")
	
	api_response = api_result.json()


	try:
		answer = api_response["knowledge_graph"]["description"]
		answer_url = api_response["organic_results"][0]["link"]
	except:
		pass

	try:
		answer = api_response["answer_box"]["answers"][0]["answer"]
		answer_url = api_response["organic_results"][0]["link"]
	except:
		pass


	if(answer != None):
		return answer,answer_url
	else:
		return False,answer_url


def wolfram_Alpha(text,data):

	df = None
	df2 = None
	answer = None



	print("asked wolfram alpha")
	datas = json.loads(data)
	
	appId = str(datas["wolframalpha_api"])
	client = wolframalpha.Client(appId)


	res = client.query(text)
	#print(res)

	# Wolfram cannot resolve the question
	if res['@success'] == 'false':
		return False
	# Wolfram was able to resolve question
	else:
		result = None
		for entry in res['pod']:
			if(result == None):
				try:
					if(entry["@title"] == "Result"):
						result = entry["subpod"]["plaintext"]


					if(entry["@title"] == "Wikipedia summary"):
						result = entry["subpod"]["plaintext"]


					if(entry["@id"] == "WeatherSummary:WeatherData"):
						result = entry["subpod"]["plaintext"]


				except Exception as e:
					print(e)

		if(result == None):
			return False
		else:
			return(result)



def fallbackHandler(text,data):

	answer,answer_url = google(text,data)
	if(answer != False):
		return answer
	
	answer = wolfram_Alpha(text,data)
	if(answer != False):
		return answer

	#answer = duckduckgo(text)
	#if(answer != False):
	#	return answer



	return False
		
	
