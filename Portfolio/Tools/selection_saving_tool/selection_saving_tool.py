"""
#############################################################################
filename    selection_saving_tool.py
author      Sunny Sun
email       sunnysun.solar.mail@gmail.com
Description:
    Tool for saving and editing selections using pm.sets(). Works for
    objects, lights, controllers(NURBS), verts, etc. or any combinations
    of those.
Instruction:
    1. Place both "selection_saving_tool.py" and "selection_saving_tool.py"
    under your Maya scripts folder.
    2. Open Maya. In the script editor, enter:
    
import selection_saving_tool
import importlib

importlib.reload(selection_saving_tool)

selection_saving_tool.run()

    3. Run.
#############################################################################
"""

import pymel.core as pm
import os

from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtUiTools

from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

import webbrowser
import json


OV_PREVIOUS_PATH = "EXPORTER_PREVIOUS_PATH"

master_set = []

def get_maya_window():

    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

def get_script_dir():

    script_file = os.path.abspath(__file__)
    return os.path.dirname(script_file)

# Main window
class SeleSaverUI(QtWidgets.QMainWindow):
    
    def __init__(self, parent=get_maya_window()):
        # Run the initialization on the inherited QDialog class
        super(SeleSaverUI, self).__init__(parent)
        
        # Set the window title
        self.setWindowTitle('Selection Saving Tool')
        
        # Assemble the file path for the ui file
        ui_file_path = os.path.join(get_script_dir(), 'selection_saving_tool.ui')
        
        # Creat a QFile object form the file path
        qfile_object = QtCore.QFile(ui_file_path)
        
        # Open the QFile object
        qfile_object.open(QtCore.QFile.ReadOnly)
        
        # Create a QUI Loader
        loader = QtUiTools.QUiLoader()
        
        # Load the file as save it to a property
        self.ui = loader.load(qfile_object, parentWidget=self)

        # For connecting the save button to a function
        self.ui.btnSaveSel.clicked.connect(self.saveSel)

        # For connecting the select button to a function
        self.ui.btnSelect.clicked.connect(self.select)

        # For connecting the delete button to a function
        self.ui.btnDelete.clicked.connect(self.delete)

        # For connecting the rename button to a function
        self.ui.btnRename.clicked.connect(self.rename)

        # For connecting the clear button to a function
        self.ui.btnClear.clicked.connect(self.clearAll)

        # For connecting the move up button to a function
        self.ui.btnUp.clicked.connect(self.up)

        # For connecting the move down button to a function
        self.ui.btnDown.clicked.connect(self.down)

        # For connecting the move to top button to a function
        self.ui.btnTop.clicked.connect(self.top)

        # For connecting the move to bottom button to a function
        self.ui.btnBottom.clicked.connect(self.bottom)

        # For connecting the add to group button to a function
        self.ui.btnAdd.clicked.connect(self.add)

        # For connecting the remove from group button to a function
        self.ui.btnRemove.clicked.connect(self.remove)

        # For connecting the save from group button to a function
        self.ui.btnLoadGrp.clicked.connect(self.loadGrp)

        # Close the file handle
        qfile_object.close()
        
        # Show the UI
        self.show()

    def select(self):
        # get the name of the current selected item
        this_item = self.ui.list.currentItem()
        # get the row of the selected item
        row = self.ui.list.row(this_item)

        print(row)
        

        # select the set's children
        pm.select(master_set[row])
        

    def saveSel(self):
        # get the name from the line edit
        name = self.ui.lnedName.text()
        new_name = ""
        for i in name:
            if i == ' ':
                new_name = new_name + '_'
            else:
                new_name = new_name + i

        # check if the name is already there
        for i in master_set:
            if new_name == i:
                #print("ERR: Name already exist. Please choose a different name.")
                response = pm.confirmDialog(title='Error', message='Name already exist. Please choose a different name.', button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK')

                return

        # add an item to the list with the name
        self.ui.list.addItem(name)

        # add the selected object to a set with that name
        new_set = pm.sets(n=name)

        # add that to the master list
        master_set.append(new_set)

        # clear the line edit
        self.ui.lnedName.clear()

    def delete(self):
        # get the name of the current selected item
        this_item = self.ui.list.currentItem()
        # get the row of the selected item
        row = self.ui.list.row(this_item)
        # remove the item from the list
        self.ui.list.takeItem(row)

        # deleting the set from the outliner
        pm.select(master_set[row],noExpand = True)
        pm.delete()
        # remove the item from the master set
        master_set.pop(row)

    def rename(self):

        # get the new name
        new_name = self.ui.lnedName.text()

        new_new_name = ""
        for i in name:
            if i == ' ':
                new_new_name = new_new_name + '_'
            else:
                new_new_name = new_new_name + i

        # check if the name is already there
        for i in master_set:
            if new_new_name == i:
                print("ERR: Name already exist. Please choose a different name.")
                response = pm.confirmDialog(title='Error', message='Name already exist. Please choose a different name.', button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK')

                return

        # get current selected item
        this_item = self.ui.list.currentItem()
        
        # get the row of the item
        row = self.ui.list.row(this_item)

        # rename selected item
        this_item.setText(new_name)
        #print(this_item.text())

        # making a new set with new name
        pm.select(master_set[row])
        renamed_set = pm.sets(n=new_name)
        # deleting the old set in the outliner
        pm.select(master_set[row],noExpand=True)
        pm.delete()
        # changing the item in master set to the renamed set
        master_set[row] = renamed_set

        # select the new name item
        self.ui.list.setCurrentRow(row)

        # select the modified set
        pm.select(master_set[row])

        # clear line edit
        self.ui.lnedName.clear()
        
    def clearAll(self):
        # clear the list
        self.ui.list.clear()
        # clear the set
        for i in master_set:
            pm.delete(i)
        # empty master_set
        master_set.clear()

    def up(self):
        # get current selected item
        this_item = self.ui.list.currentItem()
        # get the row of the item
        row = self.ui.list.row(this_item)
        if row != 0:
            # move the item up one
            self.ui.list.takeItem(row)
            self.ui.list.insertItem((row-1),this_item)
            # move the item up one in the master set
            master_set[(row-1)],master_set[row] = master_set[row],master_set[(row-1)]
            # select the new name item
            self.ui.list.setCurrentRow((row-1))
        else:
            print("ERR: Item already at top.")

    def down(self):
        # get current selected item
        this_item = self.ui.list.currentItem()
        # get the row of the item
        row = self.ui.list.row(this_item)
        if row != (len(master_set)-1):
            # move the item up one
            self.ui.list.takeItem(row)
            self.ui.list.insertItem((row+1),this_item)
            # move the item up one in the master set
            master_set[(row+1)],master_set[row] = master_set[row],master_set[(row+1)]
            # select the new name item
            self.ui.list.setCurrentRow((row+1))
        else:
            print("ERR: Item already at bottom.")

    def top(self):
        # get current selected item
        this_item = self.ui.list.currentItem()
        # get the row of the item
        row = self.ui.list.row(this_item)
        this_set = master_set[row]
        if row != 0:
            # move the item to top in list
            self.ui.list.takeItem(row)
            self.ui.list.insertItem(0,this_item)

            # removing the item from the master set
            master_set.pop(row)
            # adding the item to the end
            master_set.append(this_set)
            # getting the length of the master set
            array_size = len(master_set)
            # brining the item to the top
            i = 0
            while i < array_size:
                master_set[-i],master_set[-i-1] = master_set[-i-1],master_set[-i]
                i+=1
            master_set[0],master_set[1] = master_set[1],master_set[0]

            # select the new name item
            self.ui.list.setCurrentRow(0)
        else:
            print("ERR: Item already at top.")

    def bottom(self):
        # get current selected item
        this_item = self.ui.list.currentItem()
        # get the row of the item
        row = self.ui.list.row(this_item)
        end = len(master_set)-1
        this_set = master_set[row]
        if row != end:
            # move the item up one
            self.ui.list.takeItem(row)
            self.ui.list.insertItem(end,this_item)
            
            # removing the item from the master set
            master_set.pop(row)
            # adding the item to the end
            master_set.append(this_set)

            # select the new name item
            self.ui.list.setCurrentRow(end)
        else:
            print("ERR: Item already at bottom.")

    def add(self):
        # get current selected item
        this_item = self.ui.list.currentItem()
        # get the row of the item
        row = self.ui.list.row(this_item)
        pm.sets(master_set[row],forceElement=pm.selected())
        # select the modified set
        pm.select(master_set[row])

    def remove(self):
        # get current selected item
        this_item = self.ui.list.currentItem()
        # get the row of the item
        row = self.ui.list.row(this_item)
        pm.sets(master_set[row],remove=pm.selected())
        # select the modified set
        pm.select(master_set[row])

    def loadGrp(self):
        # clear the list
        self.ui.list.clear()
        # clear the set
        master_set.clear()

        for i in pm.ls(et='objectSet'):
            if str(i) != 'defaultLightSet' and i != 'defaultObjectSet':

                # add an item to the list with the name
                self.ui.list.addItem(str(i))

                # add that to the master list
                master_set.append(i)


def deleteAll():
    for i in master_set:
        pm.delete(i)

def maybeSave():
    return "Check"

# Function for running the UI and the script
def run():
    for ui_item in QtWidgets.QApplication.allWidgets():
        if type(ui_item).__name__ == 'SeleSaverUI':
            ui_item.close()
    SeleSaverUI()