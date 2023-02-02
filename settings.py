# Define constant variables
import yaml

# Open the config file
with open("config.yml", "r") as file:
    # Load the YAML contents into a Python dictionary
    config = yaml.safe_load(file)


APP_NAME = config['app_name']
APP_SHORTCUT_LINK = config['app_shortcut_link']
WAIT_VALUE = config['wait_value']
QUICK_SEARCH_BUTTON = config['quick_search_button']
TIME_INTERVAL_BUTTON = config['time_interval_button']
KEYS_FOR_QUICK_SEARCH =  config['keys_for_quick_search']
KEYS_FOR_TIME_INTERVAL = config['keys_for_time_interval']

NUMPAD_KEYS_SCANCODE = config['numpad_keys_scancode']
SIZE_OF_SQUARE = config['size_of_square']
KEYS_THAT_ALREADY_HAVE_HOTKEYS: dict = config['keys_that_already_have_hotkeys']

# Special cases Key
OPEN_TRADINGVIEW_KEY = config['open_tradingview_key']
SQUARE_HOTKEY = config['square_hotkey']


# Mappings of keys to their respective functions
HOT_KEYS_MAPPING = {
    '1': 'Cross',                  
    '2': '1D',                      # 1 Day Chart
    '3': '5',                       # 5 Minute Chart
    '4': '1',                       # 1 Minute Chart
    '5': '15',                      # 15 Minute Chart  
    '6': '30',                      # 30 Minute Chart
    '7': '1H',                      # 1 Hour Chart
    '8': '4H',                      # 4 Hour Chart
    '9': '1W',                      # 1 Week Chart
    '0': 'Trend',                   # Trend line, has alternative hotkey 
    'enter': 'Open',                # Open up the TradingView App
    '+': 'Hide',                    # Delete Drawings
    '-': 'Rectangle',               # Hide all drawings, has alternative hotkey
    '*': 'Fib R',                   # Fib, has alternative hotkey
    '.': 'Horiz',                   # Draw Horizontal Line, has alternative hotkey
    '/': 'Auto (Fit',
    'backspace': 'Remove Drawings'
}

HOT_KEYS_MAPPING_METHOD2 = config['hotkeys_mapping_method2']

BACKSPACE_REMOVE_DRAWING_KEY = config['backspace_remove_drawing_key']
AUTOFIT_KEY = '/'
