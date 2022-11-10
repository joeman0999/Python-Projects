from pynput.mouse import Button, Controller
import time
import random
from pynput.keyboard import Listener, KeyCode
from pynput import keyboard
import threading



class AutoClicker(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = False
        self.program_running = True
        self.clickRate = .1
        self.start_stop_char = 's'
        self.edit_speed_char = 'c'
        self.exit_char = 'e'
        
    def exit(self):
        self.stop_clicking()
        self.program_running = False
        
    def start_clicking(self):
        self.running = True
        
    def stop_clicking(self):
        self.running = False
    
    def run(self):
        while self.program_running:
            while self.running:
                mouse.click(Button.left)
                #time.sleep(random.randint(1400,1600)/1000)
                time.sleep(self.clickRate)
            time.sleep(0.1)
            
    def printClickRate(self):
        print("Current time between clicks: " + str(self.clickRate))

    def printStatus(self):
        self.printClickRate()
        print("Press " + self.start_stop_char + " to start clicking")
        print("Press " + self.edit_speed_char + " to change time between clicks")
        print("Press " + self.exit_char + " to quit")
            
mouse = Controller()
click_thread = AutoClicker()
click_thread.printStatus()
click_thread.start()

def on_press(key):
    if key == KeyCode(char=click_thread.start_stop_char):
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
    elif key == KeyCode(char=click_thread.edit_speed_char):
        time.sleep(.01)
        running = False
        if click_thread.running:
            running = True
            click_thread.stop_clicking()
        click_thread.clickRate = int(input("New clickRate: "))
        if running == True:
            click_thread.start_clicking()
        click_thread.printClickRate()
    elif key == KeyCode(char=click_thread.exit_char):
        click_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()

