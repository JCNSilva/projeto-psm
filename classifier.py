# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 09:50:32 2017
Python 3.6.0
@author: Julio and Gleyser
"""

import scipy.io.wavfile as wav
import scipy.fftpack as transf
import numpy as np
import math

# Calculates FFT of windows
# w_size: Window size
# sl_rate: Sliding rate
def windowed_fft(audio_path, w_size, sl_rate):
    [sample_rate, data] = wav.read(audio_path)
    fftwindows = list(list())    
    for w_start in range(0, len(data) - sample_rate*w_size, int(math.floor(sample_rate*sl_rate))):
        window = data[w_start:w_start+sample_rate*w_size]
        # precisamos apenas da metade direita dos valores da FFT, 
        # a outra metade é apenas o espelho da primeira
        fftwindow = transf.fft(window)
        fftwindow = fftwindow[:len(window)//2] 
        fftwindows.append(fftwindow)      
    return fftwindows

# Calculates Windowed FFT for all audio files
# files_windows is a 3D array. 
# Dimension 1 is a file, Dimension 2 is a window inside this file and 
# dimension 3 stores the result of FFT for each window
# So, files_windows[0][1][2] gets the 3rd element of the 2nd window of file 1
# files_windows[4][2][0] gets the 1st element of the 3rd window of file 5
files_windows = list(list())

# cada elemento do dicionario tem a FFT de todas as janelas do arquivo passado como chave para o dicionario
arquivos = {}
nomes = {}
for i in range(20):
    file_number = '%02d' % (i+1)
    file_windows = windowed_fft('output/speech-silence/vf12-' + file_number + '.wav', 2, 0.2)    
    arquivos[i+1] = file_windows
    nomes[i+1] = 'vf12-' + str(file_number)
    print(i+1)
    #files_windows.append(file_windows)

result = {}    
for i in range(20):
    # element eh um array que tem a FFT de todas as janelas do arquivo
    arquivo = arquivos[i+1] 
    # os valores da FFT das janelas
    count = 0
    segs = 0
    result[i+1] = []
    for window in arquivo:
        #window = element[0]
        n_components = len(window)
        # calculamos a magnitude dos valores da janela
        mag = np.abs(window)
        # pega o indice das 25 frequencias de maior amplitude
        mag_order = np.argsort(mag)[-25:]
        # descobre quais foram as 25 frequencias de maior amplitude
        # (index / num_components) * (fs/2)
        mag_order = np.add(mag_order, 1.0)
        main_frequencies = np.multiply(np.divide(mag_order, n_components), float(48000) / 2)
        
        #TODO: Melhorar isso aqui
        #Verifica se 15 dessas 25 frequencias estão no espectro da voz
        frequencias_voz = [x for x in main_frequencies if x >= 65 and x <= 285]
        #Classifica a janela
        if len(frequencias_voz) >= 15:
            print('Voz! Na janela', count, 'do arquivo', i+1, '. Segundos:', segs , '-', segs+2)
            result[i+1].append(segs)
            result[i+1].append(segs+2)
        count+=1
        segs += 0.2

for j in range(20):
	
	if len(result[j+1]) > 1:		
		inicio = result[j+1][0] + 1
		fim = result[j+1][-1] - 1
		print "arquivo " + nomes[j+1] + " inicio da voz: " + str(inicio)
		print "arquivo " + nomes[j+1] + " final da voz: " + str(fim)
		#print "----"
     
	
