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

parser.add_argument('-O', "--output_folder", type=str, default="audio\\")
parser.add_argument("-V",  "--voices", type=str, nargs="+", action='append') 
parser.add_argument("-S",  "--sentences", type=str ,nargs="+", action='append') 
args = parser.parse_args()

output_folder = args.output_folder
voices = args.voices
sentences = args.sentences


print( sentences[0])

