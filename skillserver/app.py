# coding=UTF-8
#!/usr/bin/env python3
from __future__ import unicode_literals, print_function

from flask import Flask
from flask import Flask, flash, render_template, request
import urllib.parse
import json
import os.path
import os
import requests
import urllib.request
import urllib
import random
import shutil
import string
import re
import uuid
import importlib
from glob import glob
from pathlib import Path
from whatthelang import WhatTheLang
from googletrans import Translator
from fallback import fallbackHandler, google
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN
import linecache
import sys
from searxapi import callAPI


def detect(text):
	wtl = WhatTheLang()
	return wtl.predict_lang(text)



def info(text):
	print("\n")
	print("*"*5)
	print(text)
	print("*"*5)
	print("\n")


def translate(text, target = "en", src = False):
	wtl = WhatTheLang()
	if(wtl.predict_lang(text) != target):
		info("translating...")
		translator = Translator()
		translated = translator.translate(text, dest = target)
		text = translated.text
		if(src):
			return text,translated.src
	return text


def ip2loc(ip):
	r = requests.get(url = "https://freegeoip.app/json/" + str(ip)) 
	answer = r.text
	datas = json.loads(answer)
	answer = datas["city"]
	if(answer != ""):
		return(answer)
	elif(datas["country_name"] != ""):
		answer = datas["country_name"]
		return(answer)
	else:
		r = requests.get(url = "https://freegeoip.app/json/")
		answer = r.text
		datas = json.loads(answer)
		answer = datas["city"]
		if(answer != ""):
			return(answer)
		else:
			answer = datas["country_name"]
			return answer


def PrintException():
	exc_type, exc_obj, tb = sys.exc_info()
	f = tb.tb_frame
	lineno = tb.tb_lineno
	filename = f.f_code.co_filename
	linecache.checkcache(filename)
	line = linecache.getline(filename, lineno, f.f_globals)
	print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

	
# install requirements for each skill if needed
def install_dependencies(path):
	os.system("pip3 install -r " + path)

list = glob("skills/*/requirements.txt")
for x in list:
	install_dependencies(x)
install_dependencies("requirements.txt")


class serverHelpers:
	def __init__(self, data):
		self.data = data
		self.text = data["text"]
		self.translated = None
		self.nlu_parsing = None
		self.probability = 0.6
		self.detect()

	
	def info(self,text):
		print("\n")
		print("*"*5)
		print(text)
		print("*"*5)
		print("\n")


	def detect(self):
		wtl = WhatTheLang()
		self.lang = wtl.predict_lang(self.text)


	def translate(self,text = None, target = "en", src = False):
		if(text == None):
			text = self.text
		wtl = WhatTheLang()
		if(wtl.predict_lang(text) != target):
			self.info("translating...")
			translator = Translator()
			translated = translator.translate(text, dest = target)
			self.translated = translated.text
			if(src):
				self.lang = translated.src
		else:
			self.translated = text


	def parseAnswer(self, text):
		text = str(text)
		text = re.sub("[\(\[].*?[\)\]]", "", text)
		text = text.replace("(","")
		text = text.replace(")","")
		return text



	def callFallback(self):
		self.translate()
		try:
			answer = fallbackHandler(self.translated,json.dumps(self.data, indent=2, ensure_ascii=False))
			self.nlu_parsing["skill_category"] = "fallback"
			if(answer != False and answer != "False"):
				answer = str(answer)
				print(answer)
				self.translate(text = answer,target = self.lang)
				answer = self.translated
				self.nlu_parsing["speak"] = self.parseAnswer(answer)
				if(len(self.nlu_parsing["speak"]) < 1):
					return "An error occured"
				self.nlu_parsing["answer_url"] = callAPI(self.text,self.lang)
				results = json.dumps(self.nlu_parsing, indent=2, ensure_ascii=False)
				self.info("Fallback succesfull")
				return results
			else:
				self.info("Fallback found no answer")
				lang = self.nlu_parsing["lang"]
				self.nlu_parsing["answer_url"] = callAPI(self.text,self.lang)
				
				de = ["Tut mir leid. Das weiß ich noch nicht, aber vielleicht hilft dir diese Website"]
				en = ["Sorry, I dont know this at the moment but maybe this webpage can help you"]

				if(lang == "de"):
					self.nlu_parsing["speak"] = random.choice(de)
				else:
					self.nlu_parsing["speak"] = random.choice(en)
				
				results = json.dumps(self.nlu_parsing, indent=2, ensure_ascii=False)
				return results
				
				
		except Exception as e:
			self.PrintException()
			return "An error occured"



	def PrintException(self):
		exc_type, exc_obj, tb = sys.exc_info()
		f = tb.tb_frame
		lineno = tb.tb_lineno
		filename = f.f_code.co_filename
		linecache.checkcache(filename)
		line = linecache.getline(filename, lineno, f.f_globals)
		print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))




	def nlu(self):
		try:
			nlu_engine = SnipsNLUEngine.from_path(str(self.lang))
			self.nlu_parsing = nlu_engine.parse(self.text)
		except Exception as e:
			print(e)
			self.translate(src = True)

			try:
				nlu_engine = SnipsNLUEngine.from_path(str(self.lang))
				self.nlu_parsing = nlu_engine.parse(self.text)
			except Exception as e:
				print(e)

			nlu_engine = SnipsNLUEngine.from_path("en")
			self.nlu_parsing = nlu_engine.parse(self.translated)

		self.nlu_parsing["lang"] = self.lang

		try:
			slots = self.nlu_parsing["slots"]
			for x in slots:
				self.nlu_parsing[x["slotName"]] = x["value"]["value"]
				

		except Exception as e:
			print(e)


		print(self.nlu_parsing)



	def nlu2(self):
		print("Second nlu")
		nlu_engine = SnipsNLUEngine.from_path("en")
		self.translate()
		self.nlu_parsing = nlu_engine.parse(self.translated)
		self.nlu_parsing["lang"] = self.lang

		try:
			slots = self.nlu_parsing["slots"]
			for x in slots:
				self.nlu_parsing[x["slotName"]] = x["value"]["value"]
				

		except Exception as e:
			print(e)


		print(self.nlu_parsing)





app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
	return "Hello World"


@app.route('/', methods=['POST', 'GET']) 
def foo(data = None):
	"""
	important variables:
	text: contains the text need to be processed
	lang: is the language code from original language
	"""


	nlu_engine = None
	translated = None
	if request.method == 'POST':
		try:
			data = str(request.json).replace("'","\"")
			#print(data)
		except Exception as e:
			print(e)

	if request.method == 'GET':
		data = {}
		
		try:
			import config
			data = config.keys
		except:
			pass

		data.update(request.args)

		try:
			text = data["text"]
		except:
			return "No text given"
		
		
	
	try:
		if(data["text"] == None or len(data["text"]) < 2):
			return "No text given"
		
	except:
		return "No text given"
	


	helper = serverHelpers(data)


	helper.nlu()

	nlu_results = json.loads(json.dumps(helper.nlu_parsing, indent=2))
	skill = nlu_results["intent"]["intentName"]
	probability = float(nlu_results["intent"]["probability"])
	
	if(skill == None or probability <= helper.probability):
		answer,answer_url = google(helper.text,json.dumps(helper.data, indent=2, ensure_ascii=False), language = helper.nlu_parsing["lang"])
		if(answer != False and answer != "False"):
			answer = str(answer)
			print(answer)
			if(answer_url != None):
					helper.nlu_parsing["answer_url"] = answer_url
			helper.nlu_parsing["speak"] = helper.parseAnswer(answer)
			helper.nlu_parsing["skill_category"] = "fallback"
			if(len(helper.nlu_parsing["speak"]) > 1):
				results = json.dumps(helper.nlu_parsing, indent=2, ensure_ascii=False)
				helper.info("Fallback succesfull")
				return results
		
		if(helper.lang != "en"):
			helper.nlu2()

		nlu_results = json.loads(json.dumps(helper.nlu_parsing, indent=2))
		skill = nlu_results["intent"]["intentName"]
		probability = float(nlu_results["intent"]["probability"])
		
		if(skill == None or probability <= helper.probability):
			
			return helper.callFallback()


	
	skill = skill.split("_")
	skill = skill[0]
	category = skill
	helper.nlu_parsing["skill_category"] = category
		
	skill = "skills." + skill + ".skill"
	mod=importlib.import_module(skill)
	results = ""

	try:
		url = None
		speak = mod.beginn(json.dumps(helper.data, indent=2, ensure_ascii=False), json.dumps(helper.nlu_parsing, indent=2).replace(category + "_", ""))

		try:
			if(len(speak) > 1 and isinstance(speak, tuple)):
				url = speak[1]
				speak = speak[0]
		except:
			pass

		info(skill)

		if(speak == False):
			
			answer,answer_url = google(helper.text,json.dumps(helper.data, indent=2, ensure_ascii=False), language = helper.nlu_parsing["lang"])
			if(answer != False and answer != "False"):
				answer = str(answer)
				print(answer)
				if(answer_url != None):
						helper.nlu_parsing["answer_url"] = answer_url
				helper.nlu_parsing["speak"] = helper.parseAnswer(answer)
				helper.nlu_parsing["skill_category"] = "fallback"
				if(len(helper.nlu_parsing["speak"]) > 1):
					results = json.dumps(helper.nlu_parsing, indent=2, ensure_ascii=False)
					helper.info("Fallback succesfull")
					return results
			
			
			try:
				return helper.callFallback()

			except Exception as e:
				print(e)


			results = "An error occured"

		else:

			try:
				helper.translate(text = speak,target = helper.lang)
			except:
				#speak = translate(speak,lang)
				pass
			
			helper.nlu_parsing["speak"] = helper.parseAnswer(helper.translated)

			if(url == None):
				helper.nlu_parsing["answer_url"] = callAPI(helper.text,helper.lang)
			else:
				helper.nlu_parsing["answer_url"] = url

			results = json.dumps(helper.nlu_parsing, indent=2, ensure_ascii=False)


	except Exception as e:
		print(e)
		results = "An error occured"
	return(results)


if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(host='0.0.0.0', port=5000)
