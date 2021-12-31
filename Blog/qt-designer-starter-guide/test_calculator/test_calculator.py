"""
#############################################################################
filename    test_calculator.py
author      Sunny Sun
email       sunnysun.solar.mail@gmail.com
Description:
    Template made for 'https://www.sunnysun.solar/blog/qt-designer-starter-guide'
    also see test_calculator.ui
#############################################################################
"""

import os

from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtUiTools

from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

OV_PREVIOUS_PATH = "EXPORTER_PREVIOUS_PATH"

def get_maya_window():

    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

def get_script_dir():

    script_file = os.path.abspath(__file__)
    return os.path.dirname(script_file)

# Main window
class TestCalculatorUI(QtWidgets.QMainWindow):
    
    def __init__(self, parent=get_maya_window()):
        # Run the initialization on the inherited QDialog class
        super(TestCalculatorUI, self).__init__(parent)
        
        # Set the window title
        self.setWindowTitle('Test Calculator')
        
        # Assemble the file path for the ui file
        ui_file_path = os.path.join(get_script_dir(), 'test_calculator.ui')
        
        # Creat a QFile object form the file path
        qfile_object = QtCore.QFile(ui_file_path)
        
        # Open the QFile object
        qfile_object.open(QtCore.QFile.ReadOnly)
        
        # Create a QUI Loader
        loader = QtUiTools.QUiLoader()
        
        # Load the file as save it to a property
        self.ui = loader.load(qfile_object, parentWidget=self)

        ###### Here is where you would connect your functions with your buttons!

        '''
        Example:

        To connect a butotn called calBtn to the function calculate

        self.ui.calBtn.clicked.connect(self.calculate)
        
        '''

        ###### Here is where you would connect your functions with your buttons!

        # Close the file handle
        qfile_object.close()
        
        # Show the UI
        self.show()


##### Here is where you would write your functions!

'''
Example:
To make a function called calculate:

def calculate():
    a = self.num1LnEd.text()
    b = self.num2LnEd.text()

    if self.plusRadBtn.isChecked():
        answer = a + b
    elif self.minusRadBtn.isChecked():
        answer = a - b
    elif self.timesRadBtn.isChecked():
        answer = a * b
    elif self.divideRadBtn.isChecked():
        answer = a / b
    else:
        return "Invilad operator"
    
    self.resultNumLbl.setText(result)

'''

##### Here is where you would write your functions!

# Function for running the UI and the script
def run():
    for ui_item in QtWidgets.QApplication.allWidgets():
        if type(ui_item).__name__ == 'TestCalculatorUI':
            ui_item.close()
    TestCalculatorUI()