# -*- coding: utf-8 -*-
'''
Created on Sat Mar 11 09:24:00 2017
Python 3.6.0
@author: Julio
'''

import numpy as np
import scipy.io.wavfile as wav
import math

np.random.seed(1212)


def audio_stuffing(audio1_path, size_sec, dest_path):
  '''Stuff audio files to make their length known.
	
	Parameters
	----------
  audio1_path: string
    The path of the audio file to be stuffed
  size_sec: float
    The length of the resulting audio file in seconds
  dest_path: string
    The path where the resulting audio file should be exported

	Returns
	-------
  An array containing the mathematical representation of the stuffed audio file
	'''
  [frame_rate, a1_data] = wav.read(audio1_path)
  a1_size = len(a1_data)
  lim_frames = frame_rate * size_sec
  stuffing_size = lim_frames - a1_size
  
  a1_data_start = np.random.randint(0, stuffing_size)
  a1_data_end = a1_data_start + a1_size - 1
  remaining_frames = lim_frames - a1_data_end - 1
  new_audio = np.concatenate((np.zeros(a1_data_start, dtype=np.int16), \
                              a1_data, \
                              np.zeros(remaining_frames, dtype=np.int16)))
  
  wav.write(dest_path + str.split(audio1_path, '/')[-1], frame_rate, new_audio)
  return new_audio


def audio_mixing(audio1_path, audio2_path, size_sec, dest_path):
  '''Mix two audio files together.
	
	Parameters
	----------
  audio1_path: string
    The path of the first audio file to be mixed
  audio2_path: string
    The path of the second audio file to be mixed
  size_sec: float
    The length of the originals and the resulting audio file in seconds
  dest_path: string
    The path where the resulting audio file should be exported

	Returns
	-------
  An array containing the mathematical representation of the mixed audio file
	'''  
  [frame_rate_a1, a1_data] = wav.read(audio1_path)
  a1_size = len(a1_data)
  lim_frames = frame_rate_a1 * size_sec
  stuffing_size = lim_frames - a1_size
  
  [frame_rate_a2, a2_data] = wav.read(audio2_path)
  
  if (len(a2_data) / frame_rate_a2) < size_sec:
    raise AssertionError('Music is too short!')
  
  a1_data_start = np.random.randint(0, stuffing_size)
  a1_data_end = a1_data_start + a1_size - 1
  new_audio = np.concatenate((a2_data[0:a1_data_start], \
                              a1_data, \
                              a2_data[a1_data_end+1:lim_frames]))
  
  
  wav.write(dest_path + audio1_path[-11:], frame_rate_a1, new_audio)
  return new_audio


def audio_smooth_mixing(audio1_path, audio2_path, size_sec, dest_path):
  '''Mix two audio files together with a smoother transition between them.
	
	Parameters
	----------
  audio1_path: string
    The path of the first audio file to be mixed
  audio2_path: string
    The path of the second audio file to be mixed
  size_sec: float
    The length of the originals and the resulting audio file in seconds
  dest_path: string
    The path where the resulting audio file should be exported

	Returns
	-------
  An array containing the mathematical representation of the smoother mixed audio file
	'''
  # Read audio 1
  [frame_rate_a1, a1_data] = wav.read(audio1_path)
  a1_size = len(a1_data)
  lim_frames = frame_rate_a1 * size_sec
  stuffing_size = lim_frames - a1_size
  
  # Read audio 2
  [frame_rate_a2, a2_data] = wav.read(audio2_path)
  
  # Check audio length
  if (len(a2_data) / frame_rate_a2) < size_sec:
    raise AssertionError('Music should have duration equal or greater than size_sec')
  
  # Calculate audio 1 starting and ending points
  a1_data_start = np.random.randint(0, stuffing_size)
  a1_data_end = a1_data_start + a1_size - 1
  
  # Parts of audio track
  part1 = a2_data[0:a1_data_start]
  part2 = a1_data
  part3 = a2_data[a1_data_end+1:lim_frames]
  
  # Fading in and out (Smoothing)
  percentil_20 = math.ceil(len(part2) * 0.2)
  for i in range(percentil_20):
    part2[i] = a1_data[i] + a2_data[a1_data_start+i] * (1 - round(i/percentil_20, 2))
    part2[-i] = a1_data[-i] + a2_data[a1_data_end-i] * (1 - round(i/percentil_20, 2))
  
  # Audio track creation
  new_audio = np.concatenate((part1, part2 , part3))
  wav.write(dest_path + audio1_path[-11:], frame_rate_a1, new_audio)
  
  return new_audio


# Creates audio data
def main():
  for i in range(20):
    file_number = '%02d' % (i+1)
    audio_smooth_mixing('data/speech/vf12-' + file_number + '.wav', 'data/silence.wav', 10, 'output/speech-silence/')
    audio_smooth_mixing('data/speech/vf12-' + file_number + '.wav', 'data/music.wav', 10, 'output/speech-music/')
    audio_smooth_mixing('data/speech/vf12-' + file_number + '.wav', 'data/sinusoidal.wav', 10, 'output/speech-high-frequency/')
    audio_smooth_mixing('data/speech/vf12-' + file_number + '.wav', 'data/whitenoise.wav', 10, 'output/speech-noise/')


if __name__ == '__main__':
  main()