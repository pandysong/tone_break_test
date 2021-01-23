# Tone continuity tester

In audio product testing, often we need to test if the device has defect:
sometimes the voice/audio will break from time to time due to some reasons: it
is possible that software has bugs, or the system clocks are not synchronized
and jitter could happen.

This little script could be used to detect if the tone is continuously
detected.

# How to use

```
python3 tone_break_test.py
```

Press "q" or "Q" or simply "enter" to terminate.

# How it is designed

This little project reads the data from sound card, and detect tone continuity
by using FFT. The percentage wise of energy of 1K signal is estimated, if it is
above a threshold, it is assumed the tone exists.

The threshold is hard coded in:

```
        tone_on = energy > 0.84
```

If the tone is on to off or vice verse, a line will be printed to indicate the
time and current state (on or off).


