# -*- coding: utf-8 -*-

'''
Created on Sat Mar 25 09:50:32 2017
Python 3.6.0
@author: Julio and Gleyser
'''

import scipy.io.wavfile as wav
import scipy.fftpack as transf
import numpy as np
import math


def windowed_fft(audio_path, w_size, sl_rate):
	'''Calculates FFT of windows.
	
	Parameters
	----------
	audio_path: string
		Path to audio file
	w_size: float
		Window size in seconds
	sl_rate: float
		Sliding rate in seconds

	Returns
	-------
	A bidimensional array of complex numbers
		The FFTs of each window
	'''
	[sample_rate, data] = wav.read(audio_path)
	fftwindows = list(list())    
	for w_start in range(0, len(data) - sample_rate*w_size, int(math.floor(sample_rate*sl_rate))):
		window = data[w_start:w_start+sample_rate*w_size]
		fftwindow = transf.fft(window)
		# We only need the first half of FFT, since the second half is only a mirror if the first one
		fftwindow = fftwindow[:len(window)//2] 
		fftwindows.append(fftwindow)      
	return fftwindows


def experiment(files_windows):
	'''Calculates Windowed FFT for all audio files.

	files_windows is a 3D array. 
	Dimension 1 is a file, Dimension 2 is a window inside this file and 
	dimension 3 stores the result of FFT for each window.
	So, files_windows[0][1][2] gets the 3rd element of the 2nd window of file 1
	files_windows[4][2][0] gets the 1st element of the 3rd window of file 5

	Parameters
	----------
	files_windows: is a 3D array of complex numbers
	'''
	files = {}
	names = {}
	for i in range(20):
		file_number = '%02d' % (i+1)
		file_windows = windowed_fft('output/speech-noise/vf12-' + file_number + '.wav', 2, 0.2)    
		files[i+1] = file_windows
		names[i+1] = 'vf12-' + str(file_number)

	result = {}    
	for i in range(20):
		file_i = files[i+1] 
		count = 0
		secs = 0
		result[i+1] = []

		for window in file_i:
			n_components = len(window)
			# Calculate the magnitude of frequencies inside the window
			mag = np.abs(window)
			# Take the 25 frequencies with the biggest amplitudes
			mag_order = np.argsort(mag)[-25:]
			mag_order = np.add(mag_order, 1.0)
			main_frequencies = np.multiply(np.divide(mag_order, n_components), float(48000) / 2)
			
			# Check if 15 out of the 25 frequencies are inside the voice spectrum (65Hz~285Hz) and classify the window
			voice_frequencies = [x for x in main_frequencies if x >= 65 and x <= 285]
			if len(voice_frequencies) >= 15:
				result[i+1].append(secs)
				result[i+1].append(secs+2)
			count+=1
			secs += 0.2

	for j in range(20):
		if len(result[j+1]) > 1:		
			start = result[j+1][0] + 1
			end = result[j+1][-1] - 1
			print('On file ' + names[j+1] + ' the voice starts at: ' + str(start))
			print('On file ' + names[j+1] + ' the voice ends at: ' + str(end))
			print('----')


def main():
	print('=== Multimedia Signal Processing: Final Project ===')
	print('Voice segmentation on audio using a variation of model-based segmentation')
	print('Enter 1 to run the experiments and 2 to insert a specific file name')
	selected_option = int(input())
	files = {}
	count = 0
	secs = 0

	if selected_option == 1:
		files_windows = list(list())
		experiment(files_windows)
	elif selected_option == 2:
		file_name = input('Enter the filename: ')
		result = {}
		result[file_name] = [] 
		file_windows = windowed_fft('output/entrada/' + file_name, 2, 0.2)    
		files[file_name] = file_windows
		file_i = files[file_name]  
		for window in file_i:
			n_components = len(window)
			# Calculate the magnitude of frequencies inside the window
			mag = np.abs(window)
			# Take the 25 frequencies with the biggest amplitudes
			mag_order = np.argsort(mag)[-25:]
			mag_order = np.add(mag_order, 1.0)
			main_frequencies = np.multiply(np.divide(mag_order, n_components), float(48000) / 2)
				
			# Check if 15 out of the 25 frequencies are inside the voice spectrum (65Hz~285Hz) and classify the window
			voice_frequencies = [x for x in main_frequencies if x >= 65 and x <= 285]
			if len(voice_frequencies) >= 15:
				result[file_name].append(secs)
				result[file_name].append(secs+2)
			count+=1
			secs += 0.2

		start = result[file_name][0] + 1
		end = result[file_name][-1] - 1
		print('On file ' + file_name + ' the voice starts at: ' + str(start))
		print('On file ' + file_name + ' the voice ends at: ' + str(end))
		print('----')


if __name__ == '__main__':
	main()