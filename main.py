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

BIND = kb.Key.f1 # f1

# detect if you in csgo
def in_csgo():
    try:
        hwnd = win32gui.GetForegroundWindow()
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        process = psutil.Process(pid).name()
        return True if process == 'csgo.exe' else False
    except:
        in_csgo()

def on_press(key, event):
    try:
        global timer
        if in_csgo() and key == BIND and time.time() - timer > 1.5:
            if event.is_set():
                winsound.Beep(600, 250)
                event.clear()
            else:
                winsound.Beep(800, 250)
                event.set()
            timer = time.time()
    except AttributeError:
        pass

# antiaim
def when_pressed(event):
    while True:
        if event.is_set() and in_csgo():
            time.sleep(150/1000)
            ctypes.windll.user32.mouse_event(0x0001, 4500, 1500)
            time.sleep(10/1000)
            ctypes.windll.user32.mouse_event(0x0001, -4500, -1500)
        else:
            time.sleep(0.05)

if __name__ == '__main__':
    timer = 0
    with mp.Manager() as manager:
        event = manager.Event()
        process = mp.Process(target=when_pressed, args=(event,))
        with kb.Listener(on_press=lambda key: on_press(key, event)) as listener:
            process.start()
            listener.join()
            event.clear()  # Stop the loop
            process.terminate()