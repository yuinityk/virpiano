#coding: utf-8
import wave
import struct
import numpy as np
from pylab import *

def createTriangleWave (A, f0, fs, length):
    data = []
    # [-1.0, 1.0]の小数値が入った波を作成
    for n in arange(length * fs):  # nはサンプルインデックス
        s = 0.0
        for k in range(0, 10):  # サンプルごとに10個のサイン波を重ね合わせ
            s += (-1)**k * (A / (2*k+1)**2) * np.sin((2*k+1) * 2 * np.pi * f0 * n / fs)
        # 振幅が大きい時はクリッピング
        if s > 1.0:  s = 1.0
        if s < -1.0: s = -1.0
        data.append(s)
    # [-32768, 32767]の整数値に変換
    data = [int(x * 32767.0) for x in data]
#    plot(data[0:100]); show()  # 波を描画
    # バイナリに変換
    data = struct.pack("h" * len(data), *data)  # listに*をつけると引数展開される
    return data

def play (data, fs, bit):
    import pyaudio
    # ストリームを開く
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=int(fs),
                    output= True)
    # チャンク単位でストリームに出力し音声を再生
    chunk = 1024
    sp = 0  # 再生位置ポインタ
    buffer = data[sp:sp+chunk]
    while buffer != '':
        stream.write(buffer)
        sp = sp + chunk
        buffer = data[sp:sp+chunk]
    stream.close()
    p.terminate()

if __name__ == "__main__" :
    freqList = [262, 294, 330, 349, 392, 440, 494, 523]  # ドレミファソラシド
    for f in freqList:
        data = createTriangleWave(0.5, f, 8000.0, 1.0)
        play(data, 8000, 16)
