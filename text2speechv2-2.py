
import os
import requests
import time
from xml.etree import ElementTree as ET
from sys import argv
import yaml
import azure.cognitiveservices.speech as speechsdk

try:
    input = raw_input
except NameError:
    pass


# Loading YAML key & region

stream = open('credentials.yaml', 'r')
keys = yaml.safe_load(stream)
key = keys['key']
region = keys['region']

import azure.cognitiveservices.speech as speechsdk


# Parsing SSML file to a string



def getvals(argv):
    values = {}
    while argv:
        if argv[0][0] == "-":
            values[argv[0]] = argv[1]
        argv = argv[1:]
    return (values)

myvalues = getvals(argv)

input_ssml = myvalues['-xml']
output = myvalues['-output']

# Parsing SSML file to a string


text = ET.parse(input_ssml)
tree = text.getroot()
text2 = ET.tostring(tree, encoding='unicode')


def speech_to_mp3(txt):
    # Creates an instance of a speech config with specified subscription key and service region.

    #your own subscription key and service region (e.g., "westus").

    speech_key, service_region = key, region

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Creates an audio configuration that points to an audio file.
    # Replace with your own audio filename.
    audio_filename = output 

    audio_output = speechsdk.AudioOutputConfig(filename=audio_filename)

    # Creates a synthesizer with the given settings
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)

    # Synthesizes the text to speech.
    # Replace with your own text.

    result = speech_synthesizer.speak_ssml(text2)

    # Checks result.
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to [{}] for text [{}]".format(audio_filename, text2))

    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        print("Did you update the subscription info?")





if output == 'speaker':
    speech_synthesis_to_speaker()
else:
    speech_to_mp3(text2)
