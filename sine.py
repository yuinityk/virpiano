# -*- coding:utf-8 -*-
"""
http://ism1000ch.hatenablog.com/entry/2013/11/15/182442
"""
#coding:utf-8
import math
import numpy
import pyaudio

#指定周波数でサイン波を生成する
def sine(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return numpy.sin(numpy.arange(length) * factor)

#オーディオ鳴らす
def play_tone(stream, frequency=440, length=1, rate=44100):
    chunks = []
    chunks.append(sine(frequency, length, rate))
    chunk = numpy.concatenate(chunks) * 0.25
    stream.write(chunk.astype(numpy.float32).tostring())

#main
if __name__ == '__main__':
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1, rate=44100, output=1)
    for i in range(1,20):
        play_tone(stream,frequency=440,length=0.05)
    stream.close()
    p.terminate()
