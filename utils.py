import winreg

path = r"C:\Users\LENOVO\OneDrive\Desktop\Projects\TradingViewHotkeysApp\main.exe"

def add_to_registry():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "StockKeys", 0, winreg.REG_SZ, )
    winreg.CloseKey(key)

# add_to_registry()

def remove_startup_registry():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)
        winreg.DeleteValue(key, "StockKeys")
        winreg.CloseKey(key)
    except WindowsError:
        print("The registry key was not found.")

# remove_startup_registry()
