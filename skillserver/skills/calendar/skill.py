import json
from datetime import datetime
import caldav 
import json
from ics import Calendar
from datetime import timedelta
from app import detect, translate

lang = None

def generate_answer(h,m,name):
	global lang
	h = str(h)
	m = str(m)
	name = str(name)
	answer = None
	if(lang == "de"):
		answer = name + " um " + h + " Uhr " + m + "\n"


	if(answer == None):
		answer = name + " at " + h + " o'clock " + m + "\n"

	return answer


def connectCalendar(url, username, password):
	client = caldav.DAVClient(url, username=username, password=password)
	principal = client.principal()
	return principal.calendars()



def getCalDavEvents(begin = None, end = None, url = None, username = None, password = None):

	calendars = connectCalendar(url = url, username = username,password = password)

	speech_text = "The login to your calendar failed"
	
	if begin==None:
		begin = datetime.today()
	else:
		begin = begin.split(" ")
		begin = begin[0] + " " + begin[1]
		begin = datetime.strptime(begin,"%Y-%m-%d %H:%M:%S")

	if end==None:
		end = begin + timedelta(hours=24)

	if len(calendars) > 0:
		calendar = calendars[0]
		results = calendar.date_search(begin,end)

		for event in results:
			print("Found: " + str(event))

		if len(results)>0:
			flatten = lambda l: [item for sublist in l for item in sublist]
			eventList = flatten([Calendar(event._data).events for event in results])
			sortedEventList = sorted(eventList,key=lambda icsEvent: icsEvent.begin)


			speech_text = ""
			for icsEvent in sortedEventList:
				print(icsEvent.begin)
				beginn = icsEvent.begin
				if("+00" in str(beginn)):
					beginn = icsEvent.begin + (timedelta(hours=1))
					h = beginn.strftime("%H")
					m = beginn.strftime("%M")
				else:
					h = beginn.strftime("%H")
					m = beginn.strftime("%M")

				speech_text += generate_answer(h,m,icsEvent.name)
		else:
			speech_text = "There is nothing on your calendar"

	return speech_text


def setCalDavEvents(begin = None, end = None, url = None, username = None, password = None, event = "Termin"):


	

	speech_text = "Der Termin konnte leider nicht eingetragen werden"

	try:

		if date==None:
			date = datetime.today()

		else:
			begin = begin.split(" ")
			begin = begin[0] + " " + begin[1]
			begin = datetime.strptime(begin,"%Y-%m-%d %H:%M:%S")

		if duration==None:
			duration = timedelta(hours=1)

		d = datetime.combine(date,time) - timedelta(hours=1)

		creationDate = datetime.now().strftime("%Y%m%dT%H%M%SZ")
		startDate = d.strftime("%Y%m%dT%H%M%SZ")
		endDate = (d + duration).strftime("%Y%m%dT%H%M%SZ")

		vcal = "BEGIN:VCALENDAR"+"\n"
		vcal += "VERSION:2.0"+"\n"
		vcal += "PRODID:-//Example Corp.//CalDAV Client//EN"+"\n"
		vcal += "BEGIN:VEVENT"+"\n"
		vcal += "TZ:+01"+"\n"
		vcal += "DTSTAMP:" + creationDate +"\n"
		vcal += "DTSTART:" + startDate +"\n"
		vcal += "DTEND:" + endDate +"\n"
		vcal += "SUMMARY:" + event + "\n"
		vcal += "END:VEVENT"+"\n"
		vcal += "END:VCALENDAR"

		print(vcal)

		calendars = connectCalendar( url = url, username = username,password = password)

		if len(calendars) > 0:
			calendar = calendars[0]
			event = calendar.add_event(vcal)
			speech_text = "Termin wurde eingetragen!"

		return speech_text

	except Exception as e:
		print(e)
		pass


def beginn(data, intents):
	data = json.loads(data)
	intents = json.loads(intents)

	url = data["calendar_url"]
	username = data["calendar_username"]
	password = data["calendar_password"]
	begin = None
	event = None
	intention = intents["intent"]["intentName"]
	if(intention == "getevents"):
		try:
			begin = intents["slots"][0]["value"]["value"]
		except Exception as e:
			print(e)


		return (str(getCalDavEvents(url = url, username = username, password = password, begin = begin)))
	else:
		try:
			if(intents["slots"][0]["slotName"] == "datetime"):
				begin = intents["slots"][0]["value"]["value"]
			else:
				event = intents["slots"][0]["value"]["value"]


				
		except Exception as e:
			print(e)

		try:
			if(intents["slots"][1]["slotName"] == "datetime"):
				begin = intents["slots"][1]["value"]["value"]
			else:
				event = intents["slots"][1]["value"]["value"]


				
		except Exception as e:
			print(e)

		if(begin == None):
			return (False)
		if(event == None):
			return (str(setCalDavEvents(url = url, username = username, password = password, begin = begin)))
		else:
			return (str(setCalDavEvents(url = url, username = username, password = password, begin = begin, event = event)))
		
