#!/usr/bin/env python3

import queue
import sounddevice as sd
import vosk
import sys

class STTModule:

    model = vosk.Model(lang="en-us")

    samplerate = None
    device = None

    q = queue.Queue()

    def __init__(self):
        if self.samplerate is None:
            device_info = sd.query_devices(self.device, 'input')
            # soundfile expects an int, sounddevice provides a float:
            self.samplerate = int(device_info['default_samplerate'])

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print("Sounddevice Status: ", status, file=sys.stderr)
        self.q.put(bytes(indata))

    def stt(self, rec, data):
        if rec.AcceptWaveform(data):
            # rec.Result() returns {/n   "text" : "<result>"\n}
            # String slice to return only <result>
            return rec.Result()[14:-3]
        
        else:
            # rec.PartialResult() returns {/n   "partial" : "<result>"/n}
            # String slice to return only <result>
            return rec.PartialResult()[17:-3]


    def listen(self, wait_length=None, break_after=True, headless=True):
        '''
        Listens for a set duration (number of loop cycles), then prints the output when activated.

        wait_length: duration (in cycles) that the program waits for an input. If None, waits indefinitely.
        break_after: whether the loop breaks after the user has finished speaking
        '''
        try:
            with sd.RawInputStream(samplerate=self.samplerate, blocksize = 8000, device=self.device, dtype='int16',
                                    channels=1, callback=self.callback):
                    if not headless:
                        print('#' * 80)
                        print('Press Ctrl+C to stop the recording')
                        print('#' * 80)

                    rec = vosk.KaldiRecognizer(self.model, self.samplerate)

                    # If wait_length != None, waits for a few cycles until the user speaks
                    # If wait_length == None, wait indefinitely
                    # Prints result afterwards
                    listen = False

                    result = ''
                    
                    while True:
                        prev_result = result

                        # Convert speech into text
                        data = self.q.get()
                        result = self.stt(rec, data)    
                        
                        # Note: 'listen' is a bit of a misnomer
                        if result == '':
                            if not listen:
                                # If the user has not started speaking
                                if wait_length != None : wait_length -= 1
                            else:
                                # If the user has finished speaking
                                listen = False
                                if break_after : break
                        else:
                            listen = True

                        if wait_length != None:
                            if wait_length <= 0 and break_after: break

                    if not headless: print(prev_result)
                    return prev_result

        except KeyboardInterrupt:
            if headless:
                raise
            else:
                print('\nDone')
        except Exception as e:
            print(e)


    def listen_hotword(self, hotwords=['hello'], break_after=True, headless=True):
        '''
        Listens indefinitely for a set of hotwords, then prints the output when activated.

        hotwords: the list of words (or phrases) to listen for
        break_after: whether the loop breaks after the user has finished speaking
        '''
        try:
            with sd.RawInputStream(samplerate=self.samplerate, blocksize = 8000, device=self.device, dtype='int16',
                                    channels=1, callback=self.callback):
                    if not headless:
                        print('#' * 80)
                        print('Press Ctrl+C to stop the recording')
                        print('#' * 80)

                    rec = vosk.KaldiRecognizer(self.model, self.samplerate)

                    # Recognises a hotword and waits for user to finish speaking
                    # Prints result afterwards
                    listen = False

                    result = ''
                    
                    while True:
                        prev_result = result

                        # Convert speech into text
                        data = self.q.get()
                        result = self.stt(rec, data)
                            
                        # If hotword is heard, prepare to speak
                        # Note: 'listen' is a bit of a misnomer
                        for hotword in hotwords:
                            if hotword in result:
                                listen = True
                        
                        if result == '' and listen:
                            listen = False
                            if break_after : break

                    if not headless: print(prev_result)
                    return prev_result

        except KeyboardInterrupt:
            if headless:
                raise
            else:
                print('\nDone')
        except Exception as e:
            print(e)


# Testing
if __name__ == '__main__':
    stt = STTModule()
    # stt.listen_hotword(['hello diana', 'hey diana'], True, False)
    stt.listen(10, True, False)