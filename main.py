from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from modules.interface import Ui_MainWindow
from modules.ui_functions import UIFunctions
from backend import TradingViewHotKeysBackgroundProcess
from dotenv import load_dotenv
import boto3
import yaml
import wmi 
import os
import requests
import ctypes


myappid = 'tahiralauddin.tradingviewhotkeysapp.1.6' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

load_dotenv()

VALIDATED_LICENSE_KEY_MESSAGE = "You're license Key is validated! You can use this software."

class MainWindow(QMainWindow):
    """
    MainWindow class for the TradingView HotKeys Desktop App.
    This class creates the main window for the app, connects UI elements to functions, 
    and sets up the app's functionality.
    """
    def __init__(self):
        """Initializes the MainWindow class and sets up the UI elements and their functions."""
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.keys_bg_process = None

        # APP NAME
        title = "Stock Keys"
        description = "An App that listens to hotkeys and does corresponding task in TradingView App."
        # APPLY TEXTS
        self.setWindowTitle(title)
        self.ui_functions = UIFunctions(self.ui, self)
        # EXTRA RIGHT BOX
        def openCloseRightBox():
            self.ui_functions.toggleRightBox(True)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            self.ui_functions.toggleLeftBox(True)

        self.ui.sizeOfSquareSpinBox.setRange(1, 1000)
        self.ui.waitValueSpinBox.setRange(1, 20)

        # Mouse Click events
        self.ui.settingsButton.clicked.connect(openCloseRightBox)
        self.ui.helpButton.clicked.connect(openCloseLeftBox)
        self.ui.loginButton.clicked.connect(self.login)
        self.ui.stopButton.clicked.connect(self.stop)
        self.ui.hideGUIButton.clicked.connect(self.hide_gui)
        self.ui.updateButton.clicked.connect(self.update_settings)
        self.ui.resetButton.clicked.connect(self.reset_settings)

        if self.get_license_key_from_config():
            self.ui.licenseInput.setEnabled(False)
            self.ui.statusLabel.setText(VALIDATED_LICENSE_KEY_MESSAGE)

        # Call other functions for initialization
        self.populate_settings_input_boxes()
        self.initialize_dynamodb()
        self.show()

    def is_internet_connected(self):
        """
        Checks if the computer is connected with internet
        Returns True if it is connected, otherwise returns False
        """
        try:
            requests.get('https://google.com')
            return True
        except requests.exceptions.ConnectionError:
            return False

    def get_license_key_from_config(self) -> bool:
        """If the license key is already validated for this machine, return True"""
        with open('config.yml') as config_file:
            config = yaml.safe_load(config_file)

        if config['license_key']:
            return True

    def set_license_key_in_config(self, license_key):
        """Set the license key in config.yml file for future use"""
        with open('config.yml') as config_file:
            config = yaml.safe_load(config_file)

        config['license_key'] = license_key

        with open('config.yml', 'w') as config_file:
            yaml.dump(config, config_file)


    def hide_gui(self):
        """Hide the Interface of the application. App runs in background completely"""
        self.hide()


    def stop(self):
        """Stop the hotkeys listener process from the background"""
        if self.keys_bg_process:
            self.keys_bg_process.terminate()
            self.ui.statusLabel.setText("The background process stopped!")


    def login(self):
        """
        Check if the provided license key is valid. If it is, 
        start a background process for the TradingViewHotKeysBackgroundProcess.
        If the license key is not valid, display an error message on the UI.
        """
        valid_license = False
        if self.get_license_key_from_config():
            valid_license = True
        else:
            license_key = self.ui.licenseInput.text()
            # Make sure internet is connected, otherwise cannot work with AWS Dynamodb
            if not self.is_internet_connected():
                QMessageBox.information(self, "Important Note", 
                                        "Internet is not connected. Cannot lookup for the license key online!")
                return 

            try:
                valid_license = self.license_key_is_valid(license_key)
                self.set_license_key_in_config(license_key)
            except Exception as e:
                # Generate Logs for erros
                QMessageBox.critical(self, "Critical Error", str(e))

        if valid_license:
            # Use a different thread, background 
            self.keys_bg_process = TradingViewHotKeysBackgroundProcess()
            self.keys_bg_process.daemon = True
            self.keys_bg_process.start()
            self.ui.statusLabel.setText("Program has started running in background!")
        else:
            self.ui.statusLabel.setText("Invalid License Key!")


    def get_machine_id(self):
        """
        This function retrieves the unique machine identifier of the computer where the code is executed.
        If the function is unable to retrieve the identifying number, it raises an exception with the message 
        "Couldn't get the Unique ID of this Machine!".
        """
        c = wmi.WMI()
        for item in c.Win32_ComputerSystemProduct():
            return item.IdentifyingNumber
        
        raise Exception("Couldn't get the Unique ID of this Machine!")


    def initialize_dynamodb(self):
        """
        Initializes a DynamoDB resource using the AWS credentials and region specified in the environment variables.
        It also sets the table name to "LicenseKeys" and assigns it to the class variable 'table'."""
        SECRET_KEY = os.environ.get('SECRET_KEY')
        ACCESS_KEY = os.environ.get('ACCESS_KEY')
        REGION_NAME = os.environ.get('REGION_NAME')

        # Create a session with the AWS credentials
        session = boto3.Session(
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            region_name=REGION_NAME
        )
        # Create a resource for DynamoDB
        dynamodb = session.resource('dynamodb')
        # Specify the table name
        table_name = "LicenseKeys"
        # Get the table
        self.table = dynamodb.Table(table_name)

        
    def create_new_license_key(self, license_key) -> bool:
        """
        Create a new license key and save it to the DynamoDB table. 
        Returns True if the creation is successful, False otherwise.
        """
        try:
            self.write_new_license_key(license_key, '')
            return True
        except:
            return False

        
    def write_new_license_key(self, license_key, machine_id) -> bool:
        """
        Writes a new license key to the DynamoDB table. 
        Returns True if the write is successful, False otherwise.
        """
        try:
            # Put the license key into the table
            self.table.put_item(
                Item={
                    'LicenseKey': license_key,
                    'MachineID': machine_id
                }
            )
            return True
        except:
            return False

    def license_key_is_valid(self, license_key) -> bool:
        """
        Checks if the provided license key is present in the DynamoDB table. 
        It also makes sure that the same license key is not being used in multiple computers.
        Returns True if it is present, False otherwise."""
        machine_id = self.get_machine_id()
        license_keys = self.list_license_keys()
        if license_key in license_keys.keys():
            machine_id_on_cloud = license_keys[license_key]
            if machine_id_on_cloud:
                if machine_id_on_cloud == machine_id:
                    # Valid License Key, being properly used
                    return True
                # Cannot use same license key in multiple computers
                raise Exception("Cannot use same license key in multiple computers!")

            # New License key created but not used yet
            # Update machine_id for license_key
            print("Adding machine to license key")
            self.write_new_license_key(license_key, machine_id)
            return True

        # Invalid License Key
        return False


    def list_license_keys(self) -> dict:
        """
        Returns a list of all license keys present in the DynamoDB table.
        """
        # Use the scan method to get all items in the table
        response = self.table.scan()
        
        # Extract the license keys from the response
        license_keys = {item['LicenseKey']: item.get('MachineID') for item in response['Items']}
        
        return license_keys

        
    def delete_license_key(self, key_to_delete) -> bool:
        """
        Deletes a specific license key from the DynamoDB table.
        Returns True if the delete is successful, False otherwise.
        """
        # Use the delete_item method to delete the item with the specified key
        response = self.table.delete_item(Key={'LicenseKey': key_to_delete})
        
        # Check the response to see if the item was successfully deleted
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print(f'Successfully deleted license key {key_to_delete}')
            return True
        else:
            print(f'Failed to delete license key {key_to_delete}')
            return False
    

    def populate_settings_input_boxes(self):
        """
        This function sets the text of the input boxes in the settings Frame 
        to their corresponding values in the Settings module which further gets
        its value from config.yml.
        """
        from settings import (APP_NAME, HOT_KEYS_MAPPING_METHOD2,
                              APP_SHORTCUT_LINK, WAIT_VALUE, SIZE_OF_SQUARE)

        self.ui.appNameInput.setText(APP_NAME)
        self.ui.fibHotKeyInput.setText(HOT_KEYS_MAPPING_METHOD2['*'])
        self.ui.trendLineHotKeyInput.setText(HOT_KEYS_MAPPING_METHOD2['0'])
        self.ui.hideDrawingsHotKeyInput.setText(HOT_KEYS_MAPPING_METHOD2['-'])
        self.ui.horizontalLineHotKeyInput.setText(HOT_KEYS_MAPPING_METHOD2['.'])
        self.ui.appShortcutLink.setText(APP_SHORTCUT_LINK)

        self.ui.waitValueSpinBox.setValue(int(WAIT_VALUE * 10))
        self.ui.sizeOfSquareSpinBox.setValue(SIZE_OF_SQUARE)


    def update_settings(self):
        """
        Update the settings in the config.yml file based on the user input in the UI.
        """
        try:
            with open('config.yml') as config_file:
                config = yaml.safe_load(config_file)

            square_size = self.ui.sizeOfSquareSpinBox.value()
            wait_value = self.ui.waitValueSpinBox.value()
            app_name = self.ui.appNameInput.text()
            app_shortcut_link_path = self.ui.appShortcutLink.text()
            trend_line_hotkey = self.ui.trendLineHotKeyInput.text()
            horizontal_line_hotkey = self.ui.horizontalLineHotKeyInput.text()
            hide_drawings_hotkey = self.ui.hideDrawingsHotKeyInput.text()
            fib_hotkey = self.ui.fibHotKeyInput.text()
            
            # Updating Configurations settings
            config['size_of_square'] = int(square_size)        
            config['app_name'] = app_name
            config['wait_value'] = wait_value / 10
            config['app_shortcut_link'] = app_shortcut_link_path        
            config['hotkeys_mapping_method2']['0'] = trend_line_hotkey
            config['hotkeys_mapping_method2']['.'] = horizontal_line_hotkey
            config['hotkeys_mapping_method2']['-'] = hide_drawings_hotkey
            config['hotkeys_mapping_method2']['*'] = fib_hotkey

            #? Can keep adding more settings

            # Finally write the settings to config.yml
            with open('config.yml', 'w') as config_file:
                yaml.dump(config, config_file)
        except Exception as e:
            with open('error.log', 'w') as file:
                file.write(e)

    
    def reset_settings(self):
        """
        Reset the settings in the config.yml file to the values in config-backup.yml.
        If the user makes a mistake in the settins, he can easily revert back the original settings.
        """
        with open('config-backup.yml') as backup_settings_file, \
             open('config.yml', 'w') as settings_file:
            # Overwrite the settings of config fille
            backup_config = backup_settings_file.read()
            settings_file.write(backup_config)

        self.populate_settings_input_boxes()


# To add a loading window with animation to a PyInstaller-converted executable, you need to make changes to your original Python code before converting it to an executable. Here's a basic outline of the steps involved:
# Create a new Python script that will act as the loading window. This script should have a GUI created using a library such as tkinter, PyQt, or wxPython.
# In the loading window script, add the desired animation or any other information that you want to show while the main application is loading.
# In your main application script, add code that will launch the loading window as soon as the script is executed. You can use the subprocess module in Python to run the loading window script as a separate process.
# After the loading window is launched, the main application can continue to load and do its work in the background. When the main application is ready, you can close the loading window.
# Finally, convert the main application and the loading window script to an executable using PyInstaller.
# Note: The exact details of how to implement the loading window may vary depending on the GUI library you choose and the specifics of your application. But this outline should give you an idea of the steps involved in adding a loading window to a PyInstaller-converted executable.


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
