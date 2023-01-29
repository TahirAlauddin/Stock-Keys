# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from modules.app_settings import Settings

# GLOBALS
GLOBAL_STATE = False
GLOBAL_TITLE_BAR = True


class UIFunctions:

    def __init__(self, ui, mainwindow) -> None:
        self.ui = ui
        self.mainwindow = mainwindow


    def toggleLeftBox(self, enable):
        if enable:
            # GET WIDTH
            width = self.ui.extraLeftBox.width()
            widthRightBox = self.ui.extraRightBox.width()
            maxExtend = Settings.LEFT_BOX_WIDTH
            color = Settings.BTN_LEFT_BOX_COLOR
            standard = 0

            # GET BTN STYLE
            style = self.ui.helpButton.styleSheet()

            # SET MAX WIDTH
            if width == 0:
                widthExtended = maxExtend
                # SELECT BTN
                self.ui.helpButton.setStyleSheet(style + color)
                if widthRightBox != 0:
                    style = self.ui.settingsButton.styleSheet()
                    self.ui.settingsButton.setStyleSheet(style.replace(Settings.BTN_RIGHT_BOX_COLOR, ''))
                self.ui.gridLayout_2.setHorizontalSpacing(2)
                
            else:
                widthExtended = standard
                # RESET BTN
                self.ui.helpButton.setStyleSheet(style.replace(color, ''))
                self.ui.gridLayout_2.setHorizontalSpacing(0)
                
        UIFunctions.start_box_animation(self, width, widthRightBox, "left")


    # TOGGLE RIGHT BOX
    def toggleRightBox(self, enable):
        if enable:
            # GET WIDTH
            width = self.ui.extraRightBox.width()
            widthLeftBox = self.ui.extraLeftBox.width()
            maxExtend = Settings.RIGHT_BOX_WIDTH
            color = Settings.BTN_RIGHT_BOX_COLOR
            standard = 0

            # GET BTN STYLE
            style = self.ui.settingsButton.styleSheet()

            # SET MAX WIDTH
            if width == 0:
                widthExtended = maxExtend
                # SELECT BTN
                self.ui.settingsButton.setStyleSheet(style + color)
                if widthLeftBox != 0:
                    style = self.ui.helpButton.styleSheet()
                    self.ui.helpButton.setStyleSheet(style.replace(Settings.BTN_LEFT_BOX_COLOR, ''))

                self.ui.gridLayout_2.setHorizontalSpacing(2)
                
            else:
                widthExtended = standard
                # RESET BTN
                self.ui.settingsButton.setStyleSheet(style.replace(color, ''))
                self.ui.gridLayout_2.setHorizontalSpacing(0)

            UIFunctions.start_box_animation(self, widthLeftBox, width, "right")



    def start_box_animation(self, left_box_width, right_box_width, direction):
        right_width = 0
        left_width = 0 

        # Check values
        if left_box_width == 0 and direction == "left":
            left_width = Settings.LEFT_BOX_WIDTH
            left_width = self.mainwindow.width() * 0.5 # 50% of the width
        else:
            left_width = 0
        # Check values
        if right_box_width == 0 and direction == "right":
            right_width = Settings.RIGHT_BOX_WIDTH
            right_width = self.mainwindow.width() * 0.5 # 50% of the width
        else:
            right_width = 0       

        # ANIMATION LEFT BOX        
        self.left_box = QPropertyAnimation(self.ui.extraLeftBox, b"maximumWidth")
        self.left_box.setDuration(Settings.TIME_ANIMATION)
        self.left_box.setStartValue(left_box_width)
        self.left_box.setEndValue(left_width)
        self.left_box.setEasingCurve(QEasingCurve.InOutQuart)

        # ANIMATION RIGHT BOX        
        self.right_box = QPropertyAnimation(self.ui.extraRightBox, b"maximumWidth")
        self.right_box.setDuration(Settings.TIME_ANIMATION)
        self.right_box.setStartValue(right_box_width)
        self.right_box.setEndValue(right_width)
        self.right_box.setEasingCurve(QEasingCurve.InOutQuart)

        # GROUP ANIMATION
        self.group = QParallelAnimationGroup()
        self.group.addAnimation(self.left_box)
        self.group.addAnimation(self.right_box)
        self.group.start()


