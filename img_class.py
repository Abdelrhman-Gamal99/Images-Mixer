from PIL import Image
import PIL
import numpy as np
import matplotlib.pyplot as plt
import pyqtgraph as pg 

class image:
    def __init__(self,path):
            self.data=Image.open(path)
            self.data=self.data.transpose(PIL.Image.FLIP_LEFT_RIGHT)
            self.data=self.data.transpose(PIL.Image.ROTATE_90)
            self.img=np.array(self.data)
            self.fourier = np.fft.fft2(self.img)
            self.Phase = np.angle(self.fourier)
            self.Real= np.real(self.fourier)
            self.Imaginary= np.imag(self.fourier)
            self.Magnitude = np.abs(self.fourier)
            self.UniMagnitude=np.where(self.Magnitude, 1, self.Magnitude)
            self.UniPhase= np.where(self.Phase, 0, self.Phase)
            self.shape= self.img.shape[0:2]
            self.fourier_shifted=np.fft.fftshift(self.fourier)
            self.Magnitude_=20*np.log(np.abs(self.fourier_shifted))
           
    def Images_mixing (comp1,comp2,comp1_percentage,comp2_percentage,comp1_parameter,comp2_parameter):
        
        component1= comp1_percentage * comp1.__getattribute__(comp1_parameter)  +(1-comp1_percentage)* comp2.__getattribute__(comp1_parameter)
        component2= comp2_percentage * comp2.__getattribute__(comp2_parameter) +(1-comp2_percentage)*comp1.__getattribute__(comp2_parameter)
       
        if(comp1_parameter=="Magnitude") or (comp1_parameter=="UniMagnitude")  :
            multiplying=np.multiply(component1,np.exp(1j*component2))
            output=np.real(np.fft.ifft2(multiplying))
        elif (comp1_parameter=="Phase") or (comp1_parameter=="UniPhase") :
            multiplying=np.multiply(component2,np.exp(1j*component1))
            output=np.real(np.fft.ifft2(multiplying))
        elif(comp1_parameter=="Real"):
            output=np.real(np.fft.ifft2(np.add(component1,1j*component2)))
        elif(comp1_parameter=="Imaginary"):
            output=np.real(np.fft.ifft2(np.add(component2,1j*component1)))
           
        return output 

    
            
        