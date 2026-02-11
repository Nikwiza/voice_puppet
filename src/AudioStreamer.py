import wave
import sys
import os
import numpy as np
from threading import Lock
# from ctypes import CFUNCTYPE, c_char_p, c_int, cdll
import logging
from typing import Optional


# Suppress ALSA error messages - must be done before importing pyaudio - uncomment if you want to suppress ALSA errors, but be aware it may hide important error messages as well
# _ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
# _c_error_handler = _ERROR_HANDLER_FUNC(lambda *args: None)

# try:
#     _asound = cdll.LoadLibrary('libasound.so.2')
#     _asound.snd_lib_error_set_handler(_c_error_handler)
# except OSError:
#     pass

# Suppress stderr during pyaudio import to catch any remaining ALSA noise
# _devnull = os.open(os.devnull, os.O_WRONLY)
# _old_stderr = os.dup(2)
# os.dup2(_devnull, 2)

import pyaudio

# os.dup2(_old_stderr, 2)
# os.close(_devnull)
# os.close(_old_stderr)


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

        # Initialize PyAudio (suppress stderr to hide ALSA device probe errors - optional)
        # devnull = os.open(os.devnull, os.O_WRONLY)
        # old_stderr = os.dup(2)
        # os.dup2(devnull, 2)
        self.pyaudio_instance = pyaudio.PyAudio()
        # os.dup2(old_stderr, 2)
        # os.close(devnull)
        # os.close(old_stderr)

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

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    live_test = LiveAudioStremer()
    live_test.logger.info("Testing the info")