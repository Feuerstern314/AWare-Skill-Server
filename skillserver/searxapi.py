import urllib.request, json
import urllib.parse

def callAPI(question,lang = "en"):
  question = urllib.parse.quote(question)
  with urllib.request.urlopen("http://127.0.0.1:8888/search?q=:" + lang + "%20" + question + "&format=json") as url:
    datas = json.loads(url.read().decode())
    return datas["results"][0]["url"]
