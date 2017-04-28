#coding: utf-8
import wave
import struct
import numpy as np
from pylab import *

def createCombinedWave (A, freqList, fs, length):
    """freqListの正弦波を合成した波を返す"""
    data = []
    amp = float(A) / len(freqList)
    # [-1.0, 1.0]の小数値が入った波を作成
    for n in arange(length * fs):  # nはサンプルインデックス
        s = 0.0
        for f in freqList:
            s += amp * np.sin(2 * np.pi * f * n / fs)
        # 振幅が大きい時はクリッピング
        if s > 1.0:  s = 1.0
        if s < -1.0: s = -1.0
        data.append(s)
    # [-32768, 32767]の整数値に変換
    data = [int(x * 32767.0) for x in data]
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
    n=0
    
	#(262*(2.0**(m/12.0))]
    			 #(262, 330, 392, 494),  # C（ドミソ）
                 #(294, 370, 440),  # D（レファ#ラ）
                 #(330, 415, 494),  # E（ミソ#シ）
                 #(349, 440, 523),  # F（ファラド）
                 #(392, 494, 587),  # G（ソシレ）
                 #(440, 554, 659),  # A（ラド#ミ）
                 #(494, 622, 740)  # B（シレ#ファ#）
    while(n<11):
    	m1=float(input())
    	m2=float(input())
    	s1=262*(2**(m1/12.0))
    	s2=262*(2**(m2/12.0))
    	chordList = [(s1,s2)]
    	for freqList in chordList:
    		data = createCombinedWave(1.0, freqList, 8000.0, 1.0)
    		play(data, 8000, 16)
       	n=n+1 
