#imports here
import os
import colorama
import sounddevice as sd
import datetime
from EASGen import EASGen
from pydub import AudioSegment
import soundfile as sf
import time
import json


def getdev():
    
    device_list_name = []

    for e in range(len(sd.query_devices())):
        if sd.query_devices(device=e) not in device_list_name:
            device_list_name.append(sd.query_devices(device=e))

    for e in range(len(device_list_name)):
        print(str(e) + " - " + device_list_name[e]["name"])

    print("\n\n------------------------------------------------------------\nWhich Device (Number) do you want to use for audio Output?")

    user_input_good = False
    while user_input_good == False:

        user_input = input(">")
        try:
            user_input = int(user_input)
            if user_input < len(device_list_name):
                user_input_good = True
        except:
            user_input_good = False


    output_device = device_list_name[user_input]["name"]
    dev = output_device
    return dev



def getjjj():
    date_val = datetime.datetime.now()
    current_utc = datetime.datetime.utcnow()

    day_of_year = date_val.strftime('%j')
    utc_hour = str(current_utc.strftime('%H'))
    utc_min = str(current_utc.strftime('%M'))
    ZCZC_utc_date = f"{day_of_year}{utc_hour}{utc_min}"
    return ZCZC_utc_date


with open("config.json", "r") as jfile:
    config_file = jfile.read()
    jfile.close()

config_data = json.loads(config_file)

verbose = config_data['verbose']
callsign = config_data['callsign']
fips = config_data['FIPS']

colorama.init()

class clog:
    def error(err):
        print(f" {colorama.Fore.RED} [ ERROR ] {colorama.Fore.WHITE} {err} ")
    def warn(warn):
        print(f" {colorama.Fore.YELLOW} [ WARNING ] {colorama.Fore.WHITE} {warn} ")
    def info(inf):
        print(f" {colorama.Fore.CYAN} [ INFO ] {colorama.Fore.WHITE} {inf} ")
    def verbose(veb):
        print(f" {colorama.Fore.LIGHTYELLOW_EX} [ VERBOSE ] {colorama.Fore.WHITE} {veb} ")
    def custom(nm, inf, typ):
        if typ == "1":
            print(f" {colorama.Fore.RED} [ {nm} ] {colorama.Fore.WHITE} {inf} ")
        if typ == "2":
            print(f" {colorama.Fore.YELLOW} [ {nm} ] {colorama.Fore.WHITE} {inf} ")
        if typ == "3":
            print(f" {colorama.Fore.CYAN} [ {nm} ] {colorama.Fore.WHITE} {inf} ")
        if typ != "1":
            if typ != "2":
                if typ != "3":
                    clog.error("PULLED CLOG WITH INVALID OR NONEXISTANT TYPE.")

os.system("title FMEASTester")


if verbose == "True":
    clog.verbose("EAS Tester Initialized.")
    time.sleep(3)
    clog.verbose("Initializing Librarys and Running Warning Prompts.")

if verbose == "False":
    time.sleep(3)


time.sleep(5)

clog.warn("This Program Issues *** VALID *** EAS Tones, Make Sure your station is OFF THE AIR when using this tool.")
time.sleep(5)
clog.warn("I AM NOT RESPONSIBILE FOR MISUSE!")
time.sleep(3)
input("Press Any Key to Continue.")


time.sleep(2)
print("This will now run tests on your EAS Audio Switch.. Please Select the audio device it is located on.")
input("READY? IF NOT EXIT NOW! ")
device = getdev()


jjj = getjjj()
header = f"ZCZC-EAS-DMO-{fips}+0015-{jjj}-{callsign}-" 
Alert = EASGen.genEAS(header=header, attentionTone=True, endOfMessage=True, SampleRate=48000, mode="DASDEC") 
EASGen.export_wav("audio/Alert.wav", Alert)

file = "audio/play.wav"
data, fs = sf.read(file, dtype='float32')
dur = round(int(sf.info(file).duration))   
sd.default.reset()
sd.default.device = device
if verbose == "True":
    clog.verbose("Playing Tones through Audio Switch")
sd.play(data, fs)
sd.wait()
print("If you heard the tones go through the Audio Switch everything is configured properly! If not you might want to check it out...")
input()
time.sleep(2)
print("This will now run tests on your ENDEC.. Please Select the audio device of one of the monitors it monitors.. ")
input("READY? IF NOT EXIT NOW! ")
device = getdev()


jjj = getjjj()
header = f"ZCZC-EAS-DMO-{fips}+0015-{jjj}-{callsign}-" 
Alert = EASGen.genEAS(header=header, attentionTone=True, endOfMessage=True, SampleRate=48000, mode="DASDEC") 
EASGen.export_wav("audio/Alert.wav", Alert)

file = "audio/play.wav"
data, fs = sf.read(file, dtype='float32')
dur = round(int(sf.info(file).duration))   
sd.default.reset()
sd.default.device = device
if verbose == "True":
    clog.verbose("Playing Tones through Audio Switch")
sd.play(data, fs)
sd.wait()
print("If your Endec relayed it then everything is configured properly! If not you might want to check it out...")
input()