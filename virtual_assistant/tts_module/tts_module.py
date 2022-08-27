# Taken and edited from Coqui_AI TTS source code (TTS/bin/synthesizer.py)

import os
import string
from typing import List
# pylint: disable=redefined-outer-name, unused-argument
from pathlib import Path
import numpy as np

import TTS
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

import sounddevice as sd

# Extending the Synthesizer to allow it to play audio without saving first (using sounddevice)
class SynthesizerPlay(Synthesizer):

    # Increases the sample rate. Note: Increases both speed and pitch!
    sample_rate_factor = 1.1

    def play_audio(self, wav: List[int]):
        wav = np.array(wav)

        if self.tts_model.ap.do_rms_norm:
            wav_norm = self.tts_model.ap.rms_volume_norm(wav, self.db_level) * 32767
        else:
            wav_norm = wav * (32767 / max(0.01, np.max(np.abs(wav))))

        sample_rate = self.tts_model.ap.sample_rate * self.sample_rate_factor
        sd.play(wav_norm.astype(np.int16), sample_rate)
        sd.wait()

class TTSModule:
    # Models:
    # tts_models/en/ljspeech/fast_pitch
    # tts_models/en/ljspeech/glow-tts
    # tts_models/en/ljspeech/tacotron2-DDC

    model_name = 'tts_models/en/ljspeech/fast_pitch'
    vocoder_name = None

    # For multi-speakers
    speaker_name = '' # eg. 'VCTK_p244'

    use_cuda = False

    model_path = None
    config_path = None
    vocoder_path = None
    vocoder_config_path = None

    def __init__(self):
        # load model manager
        path = Path(TTS.__file__).parent / ".models.json"
        manager = ModelManager(path)

        if self.model_name is not None:
            self.model_path, self.config_path, _ = manager.download_model(self.model_name)

        if self.vocoder_name is not None:
            self.vocoder_path, self.vocoder_config_path = manager.download_model(self.vocoder_name)

        self.synthesizer = SynthesizerPlay(
            self.model_path,
            self.config_path,
            self.vocoder_path,
            self.vocoder_config_path,
            self.use_cuda)

    def speak(self, text):
        # RUN THE SYNTHESIS

        print(" > Text: {}".format(text))

        # kick it
        wav = self.synthesizer.tts(text, self.speaker_name)

        # play the audio
        self.synthesizer.play_audio(wav)


    def save_audio(self, text):
        # RUN THE SYNTHESIS

        print(" > Text: {}".format(text))

        # kick it
        wav = self.synthesizer.tts(text, self.speaker_name)

        # save the results
        file_name = text.replace(" ", "_")[0:20]
        out_path = '.'
        file_name = file_name.translate(
            str.maketrans('', '', string.punctuation.replace('_', ''))) + '.wav'
        out_path = os.path.join(out_path, file_name)
        print(" > Saving output to {}".format(out_path))
        self.synthesizer.save_wav(wav, out_path)


# Testing

# if __name__ == "__main__":
#     tts = TTSModule()
#     text = 'Hello Nicholas. Hope you have a nice day!'
#     tts.speak(text)