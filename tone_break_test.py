import argparse
from scipy.fft import fft, fftfreq, fftshift
import sounddevice as sd
import numpy as np
import pickle
import datetime

parser = argparse.ArgumentParser(add_help=False)


class ToneDetector:
    def __init__(self):

        # max frequency resolution is 48K
        # for N sampling points, the freq resolution is 48K/N
        # for N= 512, the freq resolution is 48000/512=93.75Hz
        # for 1KHz signal, the max amplitued is on 1000/93.75 = 10.6

        sample_rate = 48000
        signal_freq = 1000
        sample_len = 512

        freq_resolu = sample_rate / float(sample_len)

        # the offset of desired signal frequency
        offset = int(signal_freq / freq_resolu)

        # used in tone det
        self.hamming = np.hamming(sample_len)
        self.min_offset = offset - 2
        self.max_offset = offset + 2 + 1
        self.full_energy_len = int(sample_len/2)

    def tone_det(self, indata):

        data = np.multiply(self.hamming, indata)
        sp = np.absolute(fft(data))

        energy_on_signal = sum(sp[self.min_offset: self.max_offset])
        energy = energy_on_signal/float(sum(sp[:self.full_energy_len]))
        return energy


det = ToneDetector()


class ContinuousTest:
    def __init__(self):
        self.tone_on = False
        self.first_time = True
        self.start_time = datetime.datetime.now()

    def print_statue(self, energy):
        tone_on = energy > 0.84
        if tone_on != self.tone_on or self.first_time:
            self.first_time = False
            time_diff = datetime.datetime.now() - self.start_time

            print("{}, {}, {}, energy: {:1.4f}".format(
                {False: "Off", True: "On "}[tone_on],
                time_diff,
                datetime.datetime.now(), energy))
            self.tone_on = tone_on


ct = ContinuousTest()


def callback(indata, frames, time, status):
    if status:
        print(status)
    energy = det.tone_det(indata[:, 0])
    ct.print_statue(energy)


try:
    with sd.InputStream(channels=2, callback=callback):
        #sd.sleep(int(duration * 1000))
        while True:
            response = input()
            if response in ('', 'q', 'Q'):
                break
except KeyboardInterrupt:
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
