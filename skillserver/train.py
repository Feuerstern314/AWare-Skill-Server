import os.path
import os
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN, CONFIG_DE, CONFIG_ES, CONFIG_FR, CONFIG_IT, CONFIG_JA, CONFIG_KO
from glob import glob
from pathlib import Path
import json
import shutil


langs = []

list = glob("*.yaml")
for x in list:
	try:
		os.remove(x)
	except Exception as e:
		print(e)


#build train files for nlu engine from skills
def check(category):
	myfile = open(category,"r+")
	category = category.split("/")
	name = category[-1]
	name = name.split(".")
	name = name[0]
	if(name not in langs):
		langs.append(name)
	category = category[1]
	mydef = open(name + ".definition.yaml","a+")
	yamlDatas = myfile.read()
	myfile.close()
	replacing = "type: intent\nname: "
	replacer = "type: intent\nname:"
	for xyz in range(2):
		yamlDatas = yamlDatas.replace(replacing,replacer)
	yamlDatas = yamlDatas.replace(replacer, replacing + category + "_")
	mydef.write("\n")
	mydef.write(yamlDatas.lower())
	mydef.write("\n")


def add_entity(name):
	mydef = open(name + ".definition.yaml","a+")
	myfile = open("entitys/" + name + ".entity.yaml","r+")
	mydef.write(myfile.read().lower())
	myfile.close()
	myfile = open("entitys/global.yaml","r+")
	mydef.write(myfile.read().lower())
	myfile.close()
	mydef.write("\n")
	mydef.close()



list = glob("skills/*/*.yaml")
for x in list:
	print(x)
	check(x)


#generate trained engines
for lang in langs:

	config = CONFIG_EN

	if(lang == "en"):
		config = CONFIG_EN

	if(lang == "de"):
		config = CONFIG_DE

	if(lang == "es"):
		config = CONFIG_ES

	if(lang == "fr"):
		config = CONFIG_FR

	if(lang == "it"):
		config = CONFIG_IT

	if(lang == "ja"):
		config = CONFIG_JA

	if(lang == "ko"):
		config = CONFIG_KO




	add_entity(lang)
	os.system("python3 -m snips_nlu download " + lang)
	os.system("python3 -m snips_nlu generate-dataset " + lang + " " + lang + ".definition.yaml > definition.json")

	try:
		shutil.rmtree(lang)
	except Exception as e:
		print(e)

	DATASET_PATH = Path(__file__).parent / "definition.json"
	with DATASET_PATH.open(encoding="utf8") as f:
	    sample_dataset = json.load(f)

	nlu_engine = SnipsNLUEngine(config=config)
	nlu_engine.fit(sample_dataset)
	nlu_engine.persist(lang)
