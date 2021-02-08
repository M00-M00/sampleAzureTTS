import xml.etree.ElementTree as ET
import json
import os
import requests
import time
from xml.etree import ElementTree as ET
from sys import argv
import yaml
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat, ResultReason, CancellationReason
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import argparse
import prepare_ssmls

try:
    input = raw_input
except NameError:
    pass


# Loading YAML key & region

stream = open('config.yml', 'r')
keys = yaml.safe_load(stream)
key = keys['key']
region = keys['region']
filename = keys["SSMLs"]



# Parsing SSML file to a string


parser = argparse.ArgumentParser()

parser.add_argument('-O', "--output_folder", type=str, default="test\\")
parser.add_argument("-V",  "--voices", type=str, default=[], nargs="+", action='append') 
parser.add_argument("-S",  "--sentences", type=str, default=[] ,nargs="+", action='append') 
parser.add_argument("-P",  "--prepare_ssmls", type=bool, default=True ) 
args = parser.parse_args()

output_folder = args.output_folder
voices = args.voices
sentences = args.sentences
prepare_ssmls = args.prepare_ssmls



#Parsing SSML file to a string


def SSML_to_string(input_ssml):

    text = ET.parse(input_ssml)
    tree = text.getroot()
    text2 = ET.tostring(tree, encoding='unicode')
    return text2 


def generate_bulk():


    with open(filename, 'r') as fp:
        data = json.load(fp)
        SSMLs = data["SSMLs"]
    
    for voice in SSMLs:
        for sentence in SSMLs[voice]:
            output_name = "audio\\" + voice + "_" + sentence + ".mp3"
            speech_to_mp3(output_name, SSMLs[voice][sentence])




def generate_some_audio(voices =[], sentences = []):
    with open(filename, 'r') as fp:
        data = json.load(fp)
        SSMLs = data["SSMLs"]
    for voice in SSMLs if voices == [] else voices[0]:
        for sentence in SSMLs[voice] if sentences == [] else sentences[0]:
            output_name = output_folder  + str(voice) + "_" + str(sentence) + ".mp3"
            speech_to_mp3(output_name, SSMLs[voice][sentence])





def speech_to_mp3(output_filename, ssml):
    # Creates an instance of a speech config with specified subscription key and service region.

    #your own subscription key and service region (e.g., "westus").

    speech_key, service_region = key, region

    speech_config = SpeechConfig(subscription=speech_key, region=service_region)

    # Creates an audio configuration that points to an audio file.
    # Replace with your own audio filename.
    audio_filename = output_filename

    audio_output = AudioOutputConfig(filename=audio_filename)

    # Creates a synthesizer with the given settings
    speech_synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)

    # Synthesizes the text to speech.
    # Replace with your own text.

    result = speech_synthesizer.speak_ssml(ssml)

    # Checks result.
    if result.reason == ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to [{}] for text [{}]".format(audio_filename, ssml))

    elif result.reason == ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        print("Did you update the subscription info?")




def single_file(voice: str, sentence: str):

    with open(filename, 'r') as fp:
        data = json.load(fp)
        SSMLs = data["SSMLs"]
    ssml= SSMLs[voice][sentence]
    filen = "audio\\" + voice + "_" + sentence + ".mp3"
    speech_to_mp3(filen, ssml)






if __name__ == "__main__":
    if prepare_ssmls:
        prepare_ssmls.main()
    generate_some_audio(voices, sentences)
