from PyQt5 import QtWidgets ,QtCore, QtGui
import numpy as np
import matplotlib.pyplot as plt
from img_class import image
from GUI import Ui_MainWindow
import pyqtgraph as pg
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtWidgets, QtMultimedia
import logging
import os

try:
    os.remove("LogFile.txt")
    logging.basicConfig(filename="LogFile.txt",level=logging.INFO)
except FileNotFoundError:
    logging.basicConfig(filename="LogFile.txt",level=logging.INFO)

class ApplicationWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.comboBoxs=[self.ui.image1_comboBox,self.ui.image2_comboBox,self.ui.comp1_comboBox,self.ui.comp2_comboBox,self.ui.edit1_comboBox,self.ui.mixer_comboBox]
        for comboBox in self.comboBoxs :
            comboBox.setEnabled(False)
        self.ui.actionImage_1.triggered.connect(lambda:self.loaddata(image_number=1,widget=self.ui.image1))
        self.ui.actionImage_2.setDisabled(True)
        self.ui.actionImage_2.triggered.connect(lambda:self.loaddata(image_number=2,widget=self.ui.image2))


        self.ui.image1_comboBox.currentTextChanged.connect(lambda:self.plot_imagecomponent(self.img1,1,self.ui.image1_comp,self.ui.image1_comboBox.currentText())) 
        self.ui.image2_comboBox.currentTextChanged.connect(lambda:self.plot_imagecomponent(self.img2,2,self.ui.image2_comp,self.ui.image2_comboBox.currentText()))
        self.ui.edit1_comboBox.currentIndexChanged.connect(self.update_options)
        changes=[self.ui.comp1_slider.sliderReleased,self.ui.comp2_slider.sliderReleased,self.ui.comp1_slider.valueChanged,self.ui.comp2_slider.valueChanged,self.ui.mixer_comboBox.currentTextChanged,
        self.ui.comp1_comboBox.currentTextChanged,self.ui.comp2_comboBox.currentTextChanged,self.ui.edit2_comboBox.currentTextChanged,self.ui.edit1_comboBox.currentTextChanged]
        self.ui.actionNew_window.triggered.connect(self.new_window)
        for change in changes:
            change.connect(lambda :self.mixer())
        self.parameters_comboBoxs=[self.ui.edit1_comboBox,self.ui.edit2_comboBox]
        self.ui.edit2_comboBox.setDisabled(True)

    def loaddata(self,image_number,widget):
        filename = QtGui.QFileDialog.getOpenFileName(self)
        if filename[0]:
            self.path = filename[0]
            if image_number==1:
                self.img1=image(self.path)
                self.ui.image1.setImage(self.img1.img)
                logging.info("Image 1 is loaded correctly")
                self.ui.actionImage_2.setDisabled(False)
                self.ui.image1_comboBox.setDisabled(False)
            else:
                self.img2=image(self.path)
                if self.img2.shape==self.img1.shape:
                    self.ui.image2.setImage(self.img2.img)
                    for comboBox in self.comboBoxs :
                        comboBox.setEnabled(True)
                    logging.info("Image 2 is loaded correctly")
                else:
                    self.error("the two images are not the same size")
                    logging.error("Image 2 has a differnt size than Image 1")
            
        else:
            logging.warning(f"you didn't choose image {image_number}" )
        

    def plot_imagecomponent(self,image,image_number,widget,image_component):
        widget.clear()
        widget.show()
        widget.setImage(np.asarray((image.__getattribute__(image_component)),dtype=np.uint8))
        logging.info(f"you choose image {image_number} {image_component}_component to be shown ") 

    def update_options(self) : 
        self.ui.edit2_comboBox.setDisabled(False)
        self.ui.edit2_comboBox.setEditable(True)
        for i in range(0,7) :
            self.ui.edit2_comboBox.view().setRowHidden(i,False)
        if self.ui.edit1_comboBox.currentText() == "Magnitude"  :
            for i in range(0,7) :
                if (i==2 or i==6) :self.ui.edit2_comboBox.setCurrentText("Phase")
                else:self.ui.edit2_comboBox.view().setRowHidden(i,True)
        elif self.ui.edit1_comboBox.currentText() == "Phase" :
            for i in range(0,7) :
                if (i==1 or i==5) :self.ui.edit2_comboBox.setCurrentText("Magnitude")
                else:self.ui.edit2_comboBox.view().setRowHidden(i,True)
        elif self.ui.edit1_comboBox.currentText() == "Real" :
            for i in range(0,7) :
                if (i==4) :self.ui.edit2_comboBox.setCurrentText("Imaginary")
                else:self.ui.edit2_comboBox.view().setRowHidden(i,True)   
        elif self.ui.edit1_comboBox.currentText() == "Imaginary" : 
            for i in range(0,7) :
                if (i==3) :self.ui.edit2_comboBox.setCurrentText("Real")
                else:self.ui.edit2_comboBox.view().setRowHidden(i,True)  
        elif self.ui.edit1_comboBox.currentText() == "UniMagnitude" :
            for i in range(0,7) :
                if (i==2 or i==6) :self.ui.edit2_comboBox.setCurrentText("Phase")
                else:self.ui.edit2_comboBox.view().setRowHidden(i,True) 
        elif self.ui.edit1_comboBox.currentText() == "UniPhase" :
            for i in range(0,7) :
                if (i==1 or i==5) :self.ui.edit2_comboBox.setCurrentText("Magnitude")
                else:self.ui.edit2_comboBox.view().setRowHidden(i,True) 
        
    def mixer(self):    
        self.component1=self.ui.comp1_comboBox.currentText()
        self.component2=self.ui.comp2_comboBox.currentText()
        self.comp1_parameter=self.ui.edit1_comboBox.currentText()
        self.comp2_parameter=self.ui.edit2_comboBox.currentText()
        self.comp1_percentage=self.ui.comp1_slider.value()*0.01
        self.comp2_Percentage=self.ui.comp2_slider.value()*0.01 

        mixer_output=self.ui.mixer_comboBox.currentText()
        if(self.component1=="Img1"):
            self.component1=self.img1
        else:
            self.component1=self.img2
        if(self.component2=="Img1"):
            self.component2=self.img1
        else:
            self.component2=self.img2

        if(self.comp1_parameter!="Choose Mixer_component :") and (self.comp2_parameter!="Choose Mixer_component :"):
            
            output=image.Images_mixing(self.component1,self.component2,self.comp1_percentage,self.comp2_Percentage,self.comp1_parameter,self.comp2_parameter) 
            if (mixer_output =="output 1") : 
                self.ui.output1.clear()
                self.ui.output1.setImage(output)   
            else :
                self.ui.output2.clear()
                self.ui.output2.setImage(output)
                
            
    def error(self,message):
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error Message")
            msg.setText(message)  
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.exec_() 
    def new_window (self):
        logging.info("New Window is opened")
        self.newwindow=ApplicationWindow()
        self.newwindow.show()

def main():
	app = QtWidgets.QApplication(sys.argv)
	application = ApplicationWindow()
	application.show()
	app.exec_()

if __name__ == "__main__":
	main()


