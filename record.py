""" record adio signal with 4466 Microphone from AZdelivery. 
Playback of audio with Python.display.Audio() or frequency analyis with
numpy FFT rutines. Works surprinsingly well \n"""



import time
from ADCDevice import *

from matplotlib import pyplot as plt
import numpy as np
adc = ADCDevice() # Define an ADCDevice class object

def setup():
    global adc
    if(adc.detectI2C(0x48)): # Detect the pcf8591.
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)): # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        "Program Exit. \n");
        exit(-1)
        
def rec(length):
    """ record some audio of given length. And save raw signal as a 
    darray where signal[0,:] are the times and signal[1,:] are the 
    channels returned by the ADC converter. Play audio with 
    IPython.display.Audio(signal, rate=len(signal)/length) and be surprised
    how easy it is. Also you can create a wav file with by saving audio 
    data f.write(audio.data) and view it in software like audacity
    Also this function does some frequency analysis 
    and plots spectrum at the end when audio was recorded. 

    :param length: length of recording in seconds
    :return signal: raw signal returned from ADC converter"""
    threshold = 230
    
    start = time.time()
    t = []
    values = []
    print('start recording')
    while True:
        value = adc.analogRead(0)    # read the ADC value of channel 0
        if value > threshold:
            print('peak noise')
        t.append(time.time())
        values.append(value)
        if time.time() - start > length:
            print('stop recording')
            break
    t = np.array(t) - start
    values = np.array(values)
    print('\n save recording')
    np.save('./recording', np.vstack((t,values)))

    plt.plot(t, values)
    plt.show()

def freqanal():
    """ detect frequency. test with samples from https://www.szynalski.com/tone-generator/
    """
    sampsize = 1000      # freq analyis finite number of vals
    bcknoise = 135       # average ADC channel of back ground noise
    print('start detection')
    while True:
        
        t = []
        signal = []
        for i in range(sampsize):
            value = adc.analogRead(0)    # read the ADC value of channel 0
            t.append(time.time())
            signal.append(value)
        
        if np.max(np.abs(signal)) > bcknoise:
            dt = (t[-1] - t[0])/sampsize     # times should be equidistant

            freq = np.fft.rfftfreq(sampsize, d=dt)   # get possible frequencies for signal
            fft_spectrum = np.fft.rfft(signal)       # fast fourier transform, population of frequencies in signal
        
            fft_spectrum = fft_spectrum[freq > 0] 
            freq = freq[freq > 0]
            print('(peak signal %.1f) main freq %.2f Hz \r' % (np.max(np.abs(signal)), freq[np.argmax(np.abs(fft_spectrum))]), end='')


def destroy():
    adc.close()

    
if __name__ == '__main__':   # Program entrance
    print ('Program is starting ... ')
    try:
        setup()
        length = float(input('record length: '))
        rec(length)
        #freqanal()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()
        
    
