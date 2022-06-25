#!/usr/bin/env python3

import queue
import sounddevice as sd
import vosk
import sys

class STTModule():

    samplerate = None
    device = None

    q = queue.Queue()

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def listen(self):
        try:
            if self.samplerate is None:
                device_info = sd.query_devices(self.device, 'input')
                # soundfile expects an int, sounddevice provides a float:
                self.samplerate = int(device_info['default_samplerate'])

            model = vosk.Model(lang="en-us")

            with sd.RawInputStream(samplerate=self.samplerate, blocksize = 8000, device=self.device, dtype='int16',
                                    channels=1, callback=self.callback):
                    print('#' * 80)
                    print('Press Ctrl+C to stop the recording')
                    print('#' * 80)

                    rec = vosk.KaldiRecognizer(model, self.samplerate)

                    # Recognises a hotword and waits for user to finish speaking
                    listen = False
                    listen_buffer_max = 5 # 10 cycles of buffer after stop speaking
                    listen_buffer = 0
                    hotword = 'hello diana'
                    
                    while True:
                        data = self.q.get()
                        if rec.AcceptWaveform(data):
                            # rec.Result() returns {/n   "text" : "<result>"\n}
                            # String slice to return only <result>
                            result = rec.Result()[14:-3]
                        
                        else:
                            # rec.PartialResult() returns {/n   "partial" : "<result>"/n}
                            # String slice to return only <result>
                            result = rec.PartialResult()[17:-3]
                            
                        if hotword in result:
                            listen = True
                            listen_buffer = listen_buffer_max

                        if listen:
                            if result != '' : print(result)
                        
                        if result == '' and listen_buffer > 0:
                            listen_buffer -= 1

                        if listen_buffer <= 0: listen = False

        except KeyboardInterrupt:
            print('\nDone')

if __name__ == '__main__':
    stt = STTModule()
    stt.listen()