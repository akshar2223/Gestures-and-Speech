import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
import Gesture_Controller
#import Gesture_Controller_Gloved as Gesture_Controller
import app
from threading import Thread


# -------------Object Initialization---------------
today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init('sapi5')
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# ----------------Variables------------------------
file_exp_status = False
files =[]
path = ''
is_awake = True  #Bot status

# ------------------Functions----------------------
def reply(audio):
    app.ChatBot.addAppMsg(audio)

    print(audio)
    engine.say(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        reply("Good Morning!")
    elif hour>=12 and hour<18:
        reply("Good Afternoon!")   
    else:
        reply("Good Evening!")  
        
    reply("I am proton, how may I help you?")

# Set Microphone parameters
with sr.Microphone() as source:
        r.energy_threshold = 500 
        r.dynamic_energy_threshold = False

# Audio to String
def record_audio():
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        voice_data = ''
        audio = r.listen(source, phrase_time_limit=5)

        try:
            voice_data = r.recognize_google(audio)
        except sr.RequestError:
            reply('Sorry my Service is down. Plz check your Internet connection')
        except sr.UnknownValueError:
            print('cant recognize')
            pass
        return voice_data.lower()


# Executes Commands (input: string)
def respond(voice_data):
    global file_exp_status, files, is_awake, path
    print(voice_data)
    voice_data.replace('proton','')
    app.eel.addUserMsg(voice_data)

    if is_awake==False:
        if 'wake up' in voice_data:
            is_awake = True
            wish()

    # STATIC CONTROLS
    elif 'hello' in voice_data:
        wish()

    elif 'what is your name' in voice_data:
        reply('My name is Proton!')

    elif 'date' in voice_data:
        reply(today.strftime("%B %d, %Y"))

    elif 'time' in voice_data:
        reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])

    elif 'search' in voice_data:
        reply('Searching for ' + voice_data.split('search')[1])
        url = 'https://google.com/search?q=' + voice_data.split('search')[1]
        try:
            webbrowser.get().open(url)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')

    elif 'location' in voice_data:
        reply('Which place are you looking for ?')
        temp_audio = record_audio()
        app.eel.addUserMsg(temp_audio)
        reply('Locating...')
        url = 'https://google.nl/maps/place/' + temp_audio + '/&amp;'
        try:
            webbrowser.get().open(url)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')

    elif ('bye' in voice_data) or ('by' in voice_data):
        reply("Good bye Sir! Have a nice day.")
        is_awake = False

    elif('zoom in' in voice_data) or ('zoomin' in voice_data) or ('Zoom In' in voice_data) or ('ZoomIn' in voice_data):
        pyautogui.hotkey('ctrl','+')
        reply('zoom in successfully')

    elif('zoom out' in voice_data) or ('zoomout' in voice_data) or ('Zoom Out' in voice_data) or ('ZoomOut' in voice_data):
        pyautogui.hotkey('ctrl','-')
        reply('zoom out successfully')

    elif ('minimize tab' in voice_data) or ('minimizetab' in voice_data) or ('minimise tab' in voice_data) or('minimisetab' in voice_data):
        pyautogui.hotkey('winleft','down')
        reply('minimize successfully')

    elif ('maximize tab' in voice_data) or ('maximizetab' in voice_data) or ('maximise tab' in voice_data) or('maximisetab' in voice_data):
        pyautogui.hotkey('winleft','up')
        reply('maximize successfully')

    elif ('volumeup' in voice_data) or ('volume up' in voice_data):
        pyautogui.press('volumeup')
        reply('volume increased!')

    elif ('volumedown' in voice_data) or ('volume down' in voice_data):
        pyautogui.press('volumedown')
        reply('volume decreased!')

    elif ('scrollup' in voice_data) or ('scroll up') in voice_data:
        pyautogui.scroll(100)
        reply('Scrolled Up Successfully')
    
    elif ('scrolldown' in voice_data) or ('scroll down') in voice_data:
        pyautogui.scroll(-100)
        reply('Scrolled Down Successfully')

    elif ('scrollleft' in voice_data) or ('scroll left') in voice_data:
        pyautogui.hscroll(-100)
        reply('Scrolled Left Successfully')

    elif ('scrollright' in voice_data) or ('scroll right') in voice_data:
        pyautogui.hscroll(100)
        reply('Scrolled Right Successfully')

    elif ('screenshot' in voice_data) or ('screen shot' in voice_data):
        pyautogui.hotkey('winleft','prtscr')
        reply('Screenshot Captured!')

    elif ('terminal' in voice_data) or ('Terminal' in voice_data):
        pyautogui.hotkey('winleft','r')
        reply('Terminal Opened Successfully')

    elif ('recent close' in voice_data) or ('recentclose' in voice_data):
        pyautogui.hotkey('ctrl','shift','t')
        reply('Recent Close Tab Opened Successfully')

    elif ('start' in voice_data) or ('Start' in voice_data):
        pyautogui.hotkey('ctrl','esc')
        reply('Start Menu Opened')

    elif ('shutdown' in voice_data) or ('Start' in voice_data):
        pyautogui.hotkey('alt','f4')
        reply('Shutdown')

    elif ('right click' in voice_data) or ('rightclick' in voice_data):
        pyautogui.click(button='right')
        reply('Right Clicked Successfully!')

    elif ('left click' in voice_data) or ('leftclick' in voice_data):
        pyautogui.click(button='left')
        reply('Left Clicked Successfully!')

    elif ('double click' in voice_data) or ('doubleclick' in voice_data):
        pyautogui.doubleClick()
        reply('Double Clicked Successfully!')

    elif ('Right' in voice_data) or ('right' in voice_data):
        pyautogui.press('right')
        reply('Right Arrow Pressed!')

    elif ('left' in voice_data) or ('Left' in voice_data):
        pyautogui.press('left')
        reply('Left Arrow Pressed!')

    elif ('opencamera' in voice_data) or ('open camera' in voice_data):
        if pyautogui.hotkey('winleft','q'):
            pyautogui.typewrite('camera')
            pyautogui.press('enter')
        reply('Camera Open')

    # elif ('turn on bluetooth' in voice_data) or ('turnonbluetooth' in voice_data):
    #     if pyautogui.hotkey('win'):
    #         pyautogui.typewrite('Bluetooth')
    #         pyautogui.press('enter')
    #         pyautogui.click(x=100, y=100) # Replace x, y with the coordinates of the toggle button on your screen
    #     reply('turned on bluetooth')

    elif ('exit' in voice_data) or ('terminate' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
        app.ChatBot.close()
        #sys.exit() always raises SystemExit, Handle it in main loop
        sys.exit()
        
    
    #DYNAMIC CONTROLS
    elif 'launch gesture recognition' in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            reply('Gesture recognition is already active')
        else:
            gc = Gesture_Controller.GestureController()
            t = Thread(target = gc.start)
            t.start()
            reply('Launched Successfully')

    elif ('stop gesture recognition' in voice_data) or ('top gesture recognition' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
            reply('Gesture recognition stopped')
        else:
            reply('Gesture recognition is already inactive')
        
    elif 'copy' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied')
        
    elif 'page' in voice_data or 'pest'  in voice_data or 'paste' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted')  
        
    # File Navigation (Default Folder set to C://)
    elif 'list' in voice_data:
        counter = 0
        path = 'C://'
        files = listdir(path)
        filestr = ""
        for f in files:
            counter+=1
            print(str(counter) + ':  ' + f)
            filestr += str(counter) + ':  ' + f + '<br>'
        file_exp_status = True
        reply('These are the files in your root directory')
        app.ChatBot.addAppMsg(filestr)
        
    elif file_exp_status == True:
        counter = 0   
        if 'open' in voice_data:
            if isfile(join(path,files[int(voice_data.split(' ')[-1])-1])):
                os.startfile(path + files[int(voice_data.split(' ')[-1])-1])
                file_exp_status = False
            else:
                try:
                    path = path + files[int(voice_data.split(' ')[-1])-1] + '//'
                    files = listdir(path)
                    filestr = ""
                    for f in files:
                        counter+=1
                        filestr += str(counter) + ':  ' + f + '<br>'
                        print(str(counter) + ':  ' + f)
                    reply('Opened Successfully')
                    app.ChatBot.addAppMsg(filestr)
                    
                except:
                    reply('You do not have permission to access this folder')
                                    
        if 'back' in voice_data:
            filestr = ""
            if path == 'C://':
                reply('Sorry, this is the root directory')
            else:
                a = path.split('//')[:-2]
                path = '//'.join(a)
                path += '//'
                files = listdir(path)
                for f in files:
                    counter+=1
                    filestr += str(counter) + ':  ' + f + '<br>'
                    print(str(counter) + ':  ' + f)
                reply('ok')
                app.ChatBot.addAppMsg(filestr)

    else: 
        reply('I am not functioned to do this !')

# ------------------Driver Code--------------------

t1 = Thread(target = app.ChatBot.start)
t1.start()

# Lock main thread until Chatbot has started
while not app.ChatBot.started:
    time.sleep(0.5)

wish()
voice_data = None
while True:
    if app.ChatBot.isUserInput():
        #take input from GUI
        voice_data = app.ChatBot.popUserInput()
    else:
        #take input from Voice
        voice_data = record_audio()

    #process voice_data
    if 'proton' in voice_data:
        try:
            #Handle sys.exit()
            respond(voice_data)
        except SystemExit:
            reply("Exit Successfull")
            break
        except:
            #some other exception got raised
            print("EXCEPTION raised while closing.") 
            break



