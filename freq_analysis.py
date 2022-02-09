


import numpy as np

from matplotlib import pyplot as plt




def fromfile():
    file = input('analyse recording: ' or './recording.npy')
    print('load file %s \n ' % file)
    t_signal = np.load(file)

    t = t_signal[0,:]
    signal = t_signal[1,:]

    dt = np.mean(np.diff(t))              # times should be equidistant

    freq = np.fft.rfftfreq(len(signal), d=dt)  # get possible frequencies for signal

    fft_spectrum = np.fft.rfft(signal)         # fast fourier transform, population of frequencies in signal


    plt.subplot(121)
    plt.title('signal')
    plt.plot(t, signal)
    plt.xlabel('time [sec.]')
    plt.ylabel('signal from ADC')

    plt.subplot(122)
    plt.title('FFT')
    plt.plot(freq, fft_spectrum)
    plt.xlabel('freq [Hz]')

    plt.show()

if __name__ == '__main__':
    fromfile()

