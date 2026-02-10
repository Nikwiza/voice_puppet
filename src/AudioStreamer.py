import wave
import sys
import numpy as np
from threading import Lock
from ctypes import *
import logging

import pyaudio

class LiveAudioStremer:
    def __init__(self, sample_rate=44100, channels=2, chunk_size=512,
                format=pyaudio.paInt16, input_device_index=None, gain=20.0, logger=None):

        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.format = format
        self.input_device_index = input_device_index

        if gain < 0:
            self.logger.warning(f"Gain value {gain} is less than 0. Setting gain to 0.")
            gain = 0.0

        self.gain = gain

        # Stream state
        self.is_recording = False
        self.stream = None

        # Initialize PyAudio
        self.pyaudio_instance = pyaudio.PyAudio()

        # Data buffer for volume calculations
        self.latest_audio_data = None
        self.data_lock = Lock()

        # Format info for numpy conversion
        self.dtype_map = {
            pyaudio.paInt16: np.int16,
            pyaudio.paInt32: np.int32,
            pyaudio.paFloat32: np.float32,
        }

        self.max_amplitude_map = {
            pyaudio.paInt16: 32768.0, # pow(2,15)
            pyaudio.paInt32: 2147483648.0, #pow(2,31)
            pyaudio.paFloat32: 1.0,
        }
        
        