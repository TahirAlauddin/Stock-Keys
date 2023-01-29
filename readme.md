## Introduction

This is a GUI Application made with PyQt5, that allows users to set custom hotkeys for certain actions in TradingView Desktop application. In order to use the application, a valid license key is required. 

## Getting Started

### Prerequisites

-   A working computer with Windows 10/11 installed on it.
-   A valid license key (can be purchased on our Shopify store)
-   TradingView Desktop application installed on your computer

### Installation

 - ***For Developers***
      
      1.  Clone the repository on your local machine using `git clone https://github.com/<your-username>/<your-repo-name>.git`
      2.  Navigate to the project's root directory
      3.  Run `pipenv install` to install the required dependencies
      4.  Run `pipenv shell` to activate the virtual environment
      5.  Run `python main.py` to start the application
      
 - ***For Users:***
 
      1.  Download the installer from [here](https://google.com).
      2.  Run the installer once downloaded successfully.
      3. Go through the instructions of the installer.
      4.  Once the application is installed, make sure to configure the settings based on your requirements. For example the path to the shortcut of TradingView App.
      
      

## Usage

1.  Open the installed application
2.  Enter the license key that you received via email after purchasing the product from our Shopify store
3.  The application will run in the background and listen to keys pressed on an numpad
4.  Press the defined key (as per your configuration) to perform a specific action in TradingView

### Setting up the license key

1.  Once the application is launched, a dialog box will prompt you to enter the license key.
2.  If you have recently purchased a license key, you will receive an email with the key.
3.  If you haven't received an email or the key is invalid, please contact us for assistance.

### Setting up the hotkeys

1.  Once the license key is accepted, the application's main window will appear.
2.  In the "Settings" tab, you can define the hotkeys for different actions.
3.  Click "Save" to apply the changes and start listening for the hotkeys.

### Using the hotkeys

1.  Make sure that the TradingView Desktop application is running.
2.  Press the defined hotkey(s) on your numpad. The application will perform the corresponding action.

*Note*: You cannot use the same License key in multiple computers.

## Technical details

The license keys are generated automatically in AWS Lambda Function using webhooks from Shopify API. The application runs as a background process and listens to keys pressed on the numpad. The interface is built with `PyQt5` which is an open-source library for desktop app development. The key presses are intercepted using the `keyboard` library.

## Support

If you encounter any issues or have any questions, please contact us for assistance.

## Contributions

If you would like to contribute to the development of the application, please feel free to submit pull requests or contact us with your ideas at tahiralauddin7@gmail.com.

## License

This project is licensed under the MIT License.
