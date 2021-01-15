import speech_recognition as sr
import pyttsx3
##import pywhatkit
import datetime
import wikipedia
import pyjokes

###################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from pyvirtualdisplay import Display
#########################################

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

#############################
from google_trans_new import google_translator  
translator = google_translator()
################################

listener = sr.Recognizer()
listener.pause_threshold = 0.55
listener.energy_threshold = 325
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():

    try:
        command = ""
        with sr.Microphone() as source:
            print('listening...')
            #voice = listener.listen(source)
            voice = listener.listen(source, timeout = 3)
            print("processing voice...")
           # command = listener.recognize_google(voice)
            command = listener.recognize_google(voice, language= "te")
            command = command.lower()
            print("YOU SAID: " + command)
            if 'Jarvis' in command:
                command = command.replace('Jarvis', '')
            if 'jarvis' in command:
                command = command.replace('jarvis', '')
            
    except:
        pass
    
    return command



def playback(command_box, play_button, say_this):
    print('[!] TextBOX found')
    command_box.clear()
    command_box.send_keys(say_this)
    print('[!] PLAYBUTTON found')
    play_button.click()
    print('[!] COMMAND DONE')
    sleep(5)
    

def run_alexa(command_box, play_button, my_bot):
    
    AI_response = ""
    command = ""
    while command == "":
        command = take_command()        
    print('still searching...')
    print('[!]INPUT COMMAND CMD: ', command)
    command = translator.translate(command,lang_tgt='en') ## TEL -> ENG
    print('[!]ENGLISH COMMAND CMD: ', command)
    
    if 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        to_say = 'Current time is ' + time        
        playback(command_box, play_button, to_say)
    elif 'hi' in command:
        command = command.replace('say hi to', '')
        playback(command_box, play_button, "Hello" + command + ". My name is Jarvis. It is a pleasure to meet you.")
    elif 'status' in command:         
        playback(command_box, play_button, "Don't worry sir, all virtual systems are fully operational")
    elif command != "":
        AI_response = my_bot.get_response(str(command))        
        AI_response = str(AI_response)
        AI_response = AI_response + ""
        print("AI RESPONSE:" + AI_response)
        playback(command_box, play_button, AI_response)
        print("Playback successful:")


# selenium initial SETUP (only happen once)
options = webdriver.ChromeOptions()
options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
chrome_driver_binary = "C:\chromedriver.exe"
driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)


print('Driver successfully imported...Starting Program')
driver.get('https://www.naturalreaders.com/online/')
sleep(1.25)

print('[!] Navigated to website')
sleep(2)
choose_voice =  driver.find_element_by_id('chooseVoice')
choose_voice.click()

sleep(2)
talker = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div/app-voice-list/div/mat-tab-group/div/mat-tab-body[2]/div/app-prem-voices/div/div/div/ul/li[11]/div[2]')
talker.click()

command_box =  driver.find_element_by_id('inputDiv')
play_button =  driver.find_element_by_id('playBtn')

playback(command_box, play_button, "Importing preferences and artificial intelligence interface")

my_bot = ChatBot(name='Kiara', read_only=True, logic_adapters=[
    'chatterbot.logic.MathematicalEvaluation',
    'chatterbot.logic.BestMatch'
])
co_trainer = ChatterBotCorpusTrainer(my_bot)
co_trainer.train('chatterbot.corpus.english')



# This is an infinite loop
playback(command_box, play_button, "I have been successfully uploaded. We are online an ready!")
while True: 
    run_alexa(command_box, play_button, my_bot)






