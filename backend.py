#!python3
import pyautogui
import win32gui
import win32process
import psutil
import queue
import keyboard
import threading
import time
from win32api import GetSystemMetrics
from settings import *
import os
import ctypes
import sys

# GLOBAL VALUES
last_slashes_used_at = 0
last_enters_used_at = 0
last_backspace_used_at = 0
slashes_count = 0
enters_count = 0
backspaces_count = 0
keys_pressed_till_now = []
terminate = False

# Create a queue to transport data from one thread to another
q = queue.Queue()


class TradingViewHotKeys:
    """
    TradingViewHotKeys class is responsible for handling incoming keystrokes and
    executing the necessary actions based on the hotkey pressed.
    """
    def handle_incoming_keys(self, key) -> None:
        """
        This method handles incoming keystrokes and checks whether it is a valid key,
        then calls appropriate methods for further processing.

        Parameters:
            key: keyboard.KeyEvent object that contains the name and scan code of the pressed key.
       
        Returns: None
        """
        try:
            # Get key name
            key_char = key.name
            keys_pressed_till_now.append(key_char)

            # Internal representation of decimal is '.'
            if key_char == 'decimal':
                key_char = '.'

            # Key was pressed from the default keyboard
            # Key needs to be pressed from external numpad only
            if key.scan_code not in NUMPAD_KEYS_SCANCODE:
                #! Might need to remove this line of code
                return

            # Ignore any key pressed if it is not in the mapping 
            # or if the key was pressed using python (pyautogui etc.)
            if (key_char not in HOT_KEYS_MAPPING.keys()) or (key.scan_code < 0):
                return

            selected_app_name = self.get_selected_application_name()
            # Create a variable is_selected that tells whether the TradingView app is selected or not
            is_selected = APP_NAME in selected_app_name.lower()

            if key_char == OPEN_TRADINGVIEW_KEY:
                # Open Trading View App Or
                # Pull up Trading View app (if It is already running)
                self.open_tradingview_app()
            else:
                if is_selected:
                    # Use queue to outsource the handle hotkey job to other thread
                    q.put(key)

        except AttributeError:
            print(f'Special key {key} pressed')

    def open_tradingview_app(self):
        """
        Opens the TradingView application on the computer.
        """
        global last_enters_used_at, enters_count
        now = time.time()
        if enters_count == 0:
            last_enters_used_at = now
            
        if (now - last_enters_used_at) < 1:
            enters_count += 1
        else:
            enters_count = 0

        if enters_count == 3:
            # # Reset enters_count for next use
            enters_count = 0

            # if not self.is_process_running(APP_NAME):
            os.startfile(APP_SHORTCUT_LINK)
            # self.bring_to_front(APP_NAME)


    def remove_drawings(self, key_char):
        global last_backspace_used_at, backspaces_count
        now = time.time()
        if backspaces_count == 0:
            last_backspace_used_at = now
            
        if (now - last_backspace_used_at) < 1:
            backspaces_count += 1
        else:
            backspaces_count = 0

        if backspaces_count == 2:
            # # Reset backspaces_count for next use
            backspaces_count = 0

            search_query = HOT_KEYS_MAPPING[key_char]
            self.do_a_search_on_quick_search(search_query)



    def open_tradingview_app_from_start_menu(self):
        # Press windows button to popup Start Menu
        pyautogui.press('win')
        # Search for tradingview app in windows search
        keyboard.write(APP_NAME)
        # Click on the TradingView app 
        time.sleep(WAIT_VALUE)
        pyautogui.press('enter')
        

    def is_process_running(self, process_name):
        """
        This method checks whether the given process/software is currently running or not.

        Parameters:
            process_name (str): The name of the process to check.
        
        Returns:
            A boolean value indicating whether the process is running or not.
        """
        # Iterates through all the processes
        for proc in psutil.process_iter():
            try:
                # The given process name is present in the process name list, return True
                if process_name.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        # If process not found, return false
        return False


    def get_selected_application_name(self):
        """
        This method returns the name of the application which is currently active.
                
        Returns:
            A string containing the name of the active application.
        """
        # Get the handle of currently selected window
        handle = win32gui.GetForegroundWindow()
        try:
            # Give the handle to this function to get process Id of current window
            _, pid = win32process.GetWindowThreadProcessId(handle)
            # Using psutil module, get the name of process
            proc = psutil.Process(pid)
            # Return process/application name
            return proc.name()
        except:
            return 'Error'

    def handle_hotkey(self, key) -> None:
        """
        Handles hotkey presses.
        This method checks for hotkeys in the KEYS_FOR_QUICK_SEARCH and KEYS_FOR_TIME_INTERVAL 
        and calls the appropriate methods based on the key pressed.

        Parameters:
            key_char (str): The character corresponding to the hotkey pressed.
        """
        key_char = key.name
        # Internal representation of decimal is '.'
        if key_char == 'decimal':
            key_char = '.'

        search_query = HOT_KEYS_MAPPING[key_char]

        if key_char == SQUARE_HOTKEY:
            # To draw squre, we'll handle it differently
            self.draw_square(search_query)
        elif key_char in KEYS_THAT_ALREADY_HAVE_HOTKEYS.values():
            # Corresponding functionlity of the key already have a hotkey associated with in the app
            self.press_hotkey_in_app(key_char)
        elif key_char in KEYS_FOR_QUICK_SEARCH:
            # Search the functionality in Search tool 
            self.do_a_search_on_quick_search(search_query)
        elif key_char in KEYS_FOR_TIME_INTERVAL:
            # Key corresponds to changing Time Interval, Use ',' key to achieve this task
            self.select_time_interval(key_char)
        elif key_char in KEYS_FOR_PIXEL_LOCATION:
            self.locate_pixels_on_screen(key_char)

        elif key_char == BACKSPACE_REMOVE_DRAWING_KEY:
            self.remove_drawings(key_char)

        elif key_char == AUTOFIT_KEY:
            self.auto_fit(key_char)



    def auto_fit(self, key_char):
        global last_slashes_used_at, slashes_count
        now = time.time()
        if slashes_count == 0:
            last_slashes_used_at = now
            
        if (now - last_slashes_used_at) < 1:
            slashes_count += 1
        else:
            slashes_count = 0

        if slashes_count == 2:
            # # Reset slashes_count for next use
            slashes_count = 0

            search_query = HOT_KEYS_MAPPING[key_char]
            self.do_a_search_on_quick_search(search_query)



    def draw_square(self, search_query):
        now = time.time()

        # Search rectangle in quick-search
        self.do_a_search_on_quick_search(search_query)
        time.sleep(WAIT_VALUE)
        
        keyboard.press('shift')
        pyautogui.drag(SIZE_OF_SQUARE, SIZE_OF_SQUARE)
        pyautogui.click()
        keyboard.release('shift')

            
    def do_a_search_on_quick_search(self, search_query):
        """
        Performs a search using the quick search feature.
        This method opens the quick search feature, types the search term corresponding 
        to the hotkey pressed and selects the first search result.

        Parameters:
            search_query (str): The query which will be searched in quick search option.
        """
        # Press escape to close Symbol Search or any other popup
        keyboard.press_and_release('esc')
        pyautogui.keyDown('ctrl')
        pyautogui.press('k')
        pyautogui.keyUp('ctrl')
            
        time.sleep(WAIT_VALUE)
        pyautogui.write(search_query)

        pyautogui.keyDown('down')
        pyautogui.keyUp('down')

        time.sleep(WAIT_VALUE)
        pyautogui.keyDown('enter')
        pyautogui.keyUp('enter')


    def select_time_interval(self, key_char):
        """Selects a time interval using the hotkey pressed.

        This method types the search term corresponding to the hotkey pressed and selects the search result by pressing enter.

        Parameters:
            key_char (str): The character corresponding to the hotkey pressed.
        """
        keyboard.press_and_release('escape')
        keyboard.press_and_release(',')
        keyboard.write(HOT_KEYS_MAPPING[key_char])
        pyautogui.press('enter')

    def press_hotkey_in_app(self, key_char):
        pyautogui.press('escape')            
        hotkey = HOT_KEYS_MAPPING_METHOD2[key_char]
        keyboard.press_and_release(hotkey)

    def find_window_for_pid(self, pid):
        result = None
        def callback(hwnd, _):
            nonlocal result
            ctid, cpid = win32process.GetWindowThreadProcessId(hwnd)
            if cpid == pid:
                result = hwnd
                return False
            return True
        try:
            win32gui.EnumWindows(callback, None)
        except:
            return None
        return result
        
    def bring_to_front(self, process_name):
        for proc in psutil.process_iter():
            if process_name in proc.name().lower():
                print(proc.pid)
                hwnd = self.find_window_for_pid(proc.pid)
                if hwnd:
                    ctypes.windll.user32.SetForegroundWindow(hwnd)
                break
            
    def locate_center_of_screen(self):
        """Locate the center of the screen"""
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        center_of_width = width / 2
        center_of_height = height / 2
        return center_of_width, center_of_height


    def locate_pixels_on_screen(self, key_char):

        image = r'images/screenshots/remove-all-drawings.png'
        image2 = r'images/screenshots/remove-all-drawings2.png'

        # Escape the symbol search
        pyautogui.press('escape')
        # Escape the selection of drawing
        pyautogui.press('escape')
        
        box = pyautogui.locateOnScreen(
            image, grayscale=True
        ) or pyautogui.locateOnScreen(
            image2, grayscale=True
        )

        if box:
            x, y = (box.left + box.width//2), (box.top + box.height//2)

            pyautogui.click(x, y)
            pyautogui.click(x+50, y)


    def run(self):
        """
        Start the keyboard event listener that handles incoming keys
        when a key is pressed. Outsource the task to other thread using queue
        """
        print("RUN")
        keyboard.on_release(self.handle_incoming_keys)

        # Do other stuff here
        while True:
            if not q.empty():
                key = q.get()
                self.handle_hotkey(key)
                
            if terminate == True:
                print("Exiting")
                break      


class TradingViewHotKeysBackgroundProcess(threading.Thread):
    """
    A class representing the background process that runs the TradingView hotkeys program.
    """

    def run(self):
        # function to run in another thread
        global terminate
        terminate = False
        print("Running in another thread")
        self._stop_event = threading.Event()
        try:
            app = TradingViewHotKeys()
            app.run()
        except Exception as e:
            print(e)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def terminate(self):
        global terminate
        terminate = True


def main():        
    app = TradingViewHotKeys()
    app.run()


if __name__ == '__main__':
    main()
