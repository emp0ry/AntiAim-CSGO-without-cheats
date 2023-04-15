import os
import time
import ctypes

try: import psutil
except: os.system("pip install psutil"); import psutil
try: import winsound
except: os.system("pip install winsound"); import winsound
try: import win32gui
except: os.system("pip install win32gui"); import win32gui
try: import win32process
except: os.system("pip install pywin32"); import win32process
try: from pynput import keyboard as kb
except: os.system("pip install pynput"); from pynput import keyboard as kb
try: import multiprocessing as mp
except:  os.system("pip install multiprocess"); import multiprocessing as mp

BIND1 = kb.Key.f1 # for turn on or turn off script
BIND2 = kb.Key.f2 # for change angle of antiaim

# detect if you in csgo
def in_csgo():
    try:
        hwnd = win32gui.GetForegroundWindow()
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        process = psutil.Process(pid).name()
        return True if process == 'csgo.exe' else False
    except:
        in_csgo()

def on_press(key, event1, event2):
    try:
        global timer
        if in_csgo() and time.time() - timer > 1:
            if key == BIND1:
                if event1.is_set():
                    winsound.Beep(600, 250)
                    print('OFF')
                    event1.clear()
                else:
                    winsound.Beep(800, 250)
                    print('ON')
                    event1.set()
                timer = time.time()
            elif key == BIND2:
                if event2.is_set():
                    winsound.Beep(400, 100)
                    print('left angle')
                    event2.clear()
                else:
                    winsound.Beep(400, 100)
                    print('right angle')
                    event2.set()
                timer = time.time()
    except AttributeError:
        pass

# antiaim
def when_pressed(event1, event2):
    while True:
        if event1.is_set() and in_csgo():
            if event2.is_set(): # right antiaim
                time.sleep(150/1000)
                ctypes.windll.user32.mouse_event(0x0001, 4500, 1500)
                time.sleep(10/1000)
                ctypes.windll.user32.mouse_event(0x0001, -4500, -1500)
            else: # left antiaim
                time.sleep(150/1000)
                ctypes.windll.user32.mouse_event(0x0001, -4500, -1500)
                time.sleep(10/1000)
                ctypes.windll.user32.mouse_event(0x0001, 4500, 1500)

        else:
            time.sleep(0.05)

if __name__ == '__main__':
    timer = 0
    with mp.Manager() as manager:
        event1 = manager.Event()
        event2 = manager.Event()
        process = mp.Process(target=when_pressed, args=(event1, event2))
        with kb.Listener(on_press=lambda key: on_press(key, event1, event2)) as listener:
            process.start()
            listener.join()
            event1.clear()
            event2.clear()
            process.terminate()
