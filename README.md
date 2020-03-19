# [Documentation A\\Ware Skill Server](https://documentation.a-ware.io/?docs=skill-server)

***This software is still in development and not ready for production environment yet!***

**We are A\\Ware**\
\
A german start up with focus on software development and artificial intelligence.

Data protection is a top priority for us. Our premise is to make life easier, improve and individualize processes through intelligent software solutions. This applies equally to large corporations and private individuals. With an awareness of the value and security of data, we have set ourselves the goal of developing software that supports both commercial customers and their users.

Even before the foundation of our company, our team was able to gain a lot of experience in cooperation with internationally successful companies. Among others, we have gained projects in the fields of artificial intelligence, skill development of smart assistants, software development and IT security.

Our goal is to create tangible added value through virtual products. Thereby we attach great importance to IT security and data protection.

**Our Goal**\
With this project we aim to establish a framework that lives up to highest smart assistance standards.

Similar to Alexa and co. most of the processing is supposed to run on cloud services. This project, however, is fully open source as data security and transparency is our highest value. With an upstream NLU engine we aim to exceed usability that local engines provide while maintaining a high level of transparency and data security.

In order to ensure a certain degree of usability the server has to be equipped with several skills. For this matter we rely on support and advice of the community. Feel free to comment, add and use the service so we are keep enlarging our services to make the tolerance for data abuse obsolete when using voice assistance. Furthermore, this opens the door to use voice assistance in areas with high vulnerable data as in the health sector.

\
**That’s how it works:**

In order to show you how it works and what we bring to the table we want to walk you through the Data process.\
\
We defined a JSON API that allows accessing the server from different devices. However, we rely on Mycroft for our shared values. Therefore we developed a Fallback skill that allows direct access to our cloud. This works as follows:

1. The device passes spoken text + other data (such as login data for music streaming services or other API keys)

```
{ "text":"play music from adele", "YoutubeAPIKey":xxxxxxxxx, "caldavusername":"myUsername", "caldavpassword":"myPassword"}
```

2. A\\Ware Server receives data and retrieves variable labeled as “text”.

3. A\\Ware Server sends “text”-data through NLU engine. This AI serves as a tool to direct requests to the right skill. If detected, the system hands JSON-array as well as results from the NLU engine.

4. Now it is up to the respective skill to handle the data. And give back the answer that is supposed to be given to the user.

### **How to create a Skill:**

```
Attention: put the language code with a dot before each yaml file name
examples: en.intent.yaml or en.entity.yaml                
              de.intent.yaml or de.entity.yaml
```

1. Create a new folder for each skill. Name has to be indicator for the function.

2. This folder contains 2 files:

   1. **intent.yaml**: This file contains all the Information necessary to direct a request to the skill.\
      Put the language code in the name before, example: en.intent.yaml or de.intent.yaml.\
      The information has to be structured by the snips_nlu scheme:

\
<https://snips-nlu.readthedocs.io/en/latest/tutorial.html#training-data> \
\
Please note: Slots are global information! If new entities needed, they have to be added in the file “entity.yaml” in the entity folder.

1. **skill.py**: This file contains the actual skill code. Only Python skills are accepted. \
   \
   This file has to contain the beginn function “**def beginn(data, intents)“.**

```
import json
def beginn(data, intents):
datas = json.loads(data)
text = datas["text"]
return text
```

1. “data” contains the JSON-array from the request with optional data and the text.

2. “intents” contains results of NLU engine in JSON format.

This function also returns the answer that is given to the user.\
each line means a small pause of one second

to count to 10 for example, the output looks like this:

> one
>
> two
>
> three
>
> four
>
> five
>
> six
>
> seven
>
> eight
>
> nine
>
> ten

##### **The answer**

The answer must be a tuple, in the first place python code is returned if necessary and in the second place what the end user should get back.

Both parts have to be returned via the return statement, if one of them is not needed assign the ninth value to it according to the ninth value

The answer the server return to device looks like:

```
{ "speak":"there is no appointment for today"}
```

Please orientate yourself on existing skills to develop new ones

### **3party**

    ●https://github.com/indix/whatthelang Apache
    ●https://github.com/pallets/flask bsd3
    ●https://github.com/ssut/py-googletrans MIT
    ●https://github.com/psf/requests Apache
    ●https://github.com/snipsco/snips-nlu Apache
    ●https://github.com/jaraco/wolframalpha MIT

