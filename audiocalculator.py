import IPython
import http.client, urllib.parse, json
from xml.etree import ElementTree
import sys
from sys import getsizeof
import speech_recognition as sr
import os
import pyaudio

def process(myOperation):
    # remove any dot from string and put it in lower case
    myOperation = myOperation.replace(".", "")
    myOperation = myOperation.replace("+", " plus ")
    myOperation = myOperation.replace("-", " minus ")
    myOperation = myOperation.lower()
    if DEBUG:
        print("Trying to process string '%s'" %myOperation)
    # Split in words
    words = myOperation.split()
    if len(words) != 3:
        return None
    if words[0]=="eins": words[0]="1"
    if words[2]=="eins": words[2]="1"
    try:
        if words[1] == "plus":
            return str(int(words[0]) + int(words[2]))
        elif words[1] == "minus":
            return str(int(words[0]) - int (words[2]))
        elif words[1] == "mal":
            return str(int(words[0]) * int (words[2]))
        else:
            return None
    except:
        return None

def getSpeechToken():
    params = ""
    headers = {"Ocp-Apim-Subscription-Key": SPEECHKEY}
    accessTokenHost = "api.cognitive.microsoft.com"
    path = "/sts/v1.0/issueToken"
    conn = http.client.HTTPSConnection(accessTokenHost)
    conn.request("POST", path, params, headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data.decode("UTF-8")

def speech(myText, myToken):
    # Constructing body with ElementTree
    body = ElementTree.Element("speak", version="1.0")
    body.set("{http://www.w3.org/XML/1998/namespace}lang", "de-de")
    voice = ElementTree.SubElement(body, "voice")
    voice.set("{http://www.w3.org/XML/1998/namespace}lang", "de-DE")
    voice.set("{http://www.w3.org/XML/1998/namespace}gender", "Male")
    voice.set("name", "Microsoft Server Speech Text to Speech Voice (de-DE, JessaRUS)")
    voice.text = myText
    # Simpler alternative to XML
    textBody = "<speak version='1.0' xml:lang='de-DE'><voice xml:lang='de-DE' xml:gender='Female' name='Microsoft Server Speech Text to Speech Voice (de-DE, HeddaRUS)'>"
    textBody += myText
    textBody += "</voice></speak>"
    if DEBUG:
        print("INFO: Sending data...")
        print(textBody)
    # Headers are pretty important
    headers = {"Content-type": "application/ssml+xml",
               "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
               "Authorization": "Bearer " + myToken,
               "User-Agent": "TTSForPython",
               "Host": "speech.platform.bing.com"}
    conn = http.client.HTTPSConnection("speech.platform.bing.com")
    #conn.request("POST", "/synthesize", ElementTree.tostring(body), headers)
    conn.request("POST", "/synthesize", textBody, headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    if DEBUG:
        print("INFO: Status code received from Speech API %s: %s " % (response.status, response.reason))
        print("INFO: Data received from Speech API (%s bytes)" % getsizeof(data))
    p = pyaudio.PyAudio()
    stream = p.open(format = 8, channels = 1, rate = 16000, output = True)
    stream.write(data)


# If you prefer you can hard code your API Key and comment the raw_input line
# SPEEECHKEY = 'Your_Speech_API_Key'
SPEECHKEY = input(u'Please input your Speech API key: ')

VOICE=True
DEBUG=True

# Get a token for the speech API, if we are using voice interaction
if VOICE:
    speechToken = getSpeechToken()
    if DEBUG:
        print("INFO: Speech API token obtained:")
        print(speechToken)
        print("*************************")

# Loop to ask for commands
while True:
    # If in voice mode ask for the command
    if VOICE:
        TEXT = None
        # loop until we understand something
        while (TEXT == None):
            r = sr.Recognizer()
            with sr.Microphone() as source:
                speech("Was soll ich tun?", speechToken)
                #print("Say something")
                audio = r.listen(source)
            # transcribe speech using the Bing Speech API
            try:
                TEXT = r.recognize_bing(audio, key=SPEECHKEY, language="de-DE")
                if DEBUG: print("Here is what I understood: '" + TEXT + "'")
            except sr.UnknownValueError:
                if DEBUG: print("Didnt get it, sorry")
            except sr.RequestError as e:
                print("Something went wrong:; {0}").format(e)
    # If not in voice mode, read the command from stdin
    else:
        TEXT = input('> ')
    # If we have a command, send it to LUIS
    if len(TEXT) > 0:
        result = process(TEXT)
        if DEBUG:
            print("INFO: Result '%s'" %result)
        if result != None:
            speech("Das Ergebnis ist", speechToken)
            speech(result, speechToken)
        else:
            speech("Ich verstehe das nicht, es tut mir Leid", speechToken)
        
