# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 09:50:32 2017
Python 3.6.0
@author: Julio and Gleyser
"""

import scipy.io.wavfile as wav
import scipy.fftpack as transf
import math

# Calculates FFT of windows
def windowed_fft(audio_path, w_size, sl_rate):
    [frame_rate, data] = wav.read(audio_path)
    fftwindows = list(list())
    
    for w_start in range(0, len(data) - frame_rate*w_size, int(math.floor(frame_rate*sl_rate))):
		window = data[w_start:w_start+frame_rate*w_size]
		fftwindows.append(transf.fft(window))
        
    return fftwindows

# Calculates Windowed FFT for all audio files
# files_windows is a 3D array. 
# Dimension 1 is a file, Dimension 2 is a window inside this file and 
# dimension 3 stores the result of FFT for each window
# So, files_windows[0][1][2] gets the 3rd element of the 2nd window of file 1
# files_windows[4][2][0] gets the 1st element of the 3rd window of file 5
files_windows = list(list())
for i in range(20):
    file_number = '%02d' % (i+1)
    file_windows = windowed_fft('output/speech-noise/vf12-' + file_number + '.wav', 2, 0.2)    
    files_windows.append(file_windows)
    print(i+1)
    
