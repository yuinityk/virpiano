#coding: utf-8
import wave
import struct
import numpy as np
from pylab import *
import pyaudio

def createCombinedWave (A, freqList, fs, length):
    # freqListの正弦波を合成した波を返す
    data = []
    amp = float(A) / len(freqList)
    # [-1.0, 1.0]の小数値が入った波を作成
    # A（振幅） を1から変えると音の大きさが変わる
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

def createCombinedDampingWave (A, freqList, fs, length):
    # freqListの正弦波を合成した波を返す
    amp = float(A) / len(freqList)
    d = 2.0 # damping factor
    # [-1.0, 1.0]の小数値が入った波を作成
<<<<<<< HEAD
    for n in arange(length * fs):  # nはサンプルインデックス
        s = 0.0
        for f in freqList:
            sk = 0.0
            for k in range(0, 10):  # サンプルごとに10個のサイン波を重ね合わせ
                sk += (-1)**k * (1 / (2*k+1)**2) * np.sin((2*k+1) * 2 * np.pi * f * n / fs)
            s += sk
#        s = s * np.exp(-n / fs) # 減衰
        s = s * 2 * amp / (1 + np.exp(d * n / fs)) # 減衰
        # 振幅が大きい時はクリッピング
        if s > 1.0:  s = 1.0
        if s < -1.0: s = -1.0
        data.append(s)
    # [-32768, 32767]の整数値に変換
    data = [int(x * 32767.0) for x in data]
    # バイナリに変換
=======
    data = np.zeros(int(length * fs))
    d = 2.
    for f in freqList:
        for k in range(0,10):
            th = 2*(2*k+1)*np.pi*f/fs * np.arange(int(length*fs))
            data += (-1)**k * (1/(2*k+1)**2) * np.sin(th)
    data = data*2*amp / np.exp(d/fs *np.arange(int(length*fs)))
    data[np.where(data>1.)[0]] = 1.
    data[np.where(data<-1.)[0]] = -1.
    data *= 32767.
    data = data.astype(int)
>>>>>>> f825409fed9907b944c0c6083f3b4d2a7456c57a
    data = struct.pack("h" * len(data), *data)  # listに*をつけると引数展開される
    return data

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
                 
# 数を2つ入力すると重ね合わせ音を出力                
    while(n<3):
      m1=float(input())
#      m2=float(input())
#      m3=float(input())
      s1=440*(2**((m1-9)/12.0))
#      s2=440*(2**((m2-9)/12.0))
#      s3=440*(2**((m3-9)/12.0))
      chordList = [(s1,)]
#      chordList = [(s1,s2)]
#      chordList = [(s1,s2,s3)]
      for freqList in chordList:
    	  data = createCombinedDampingWave(2, freqList, 8000.0, 5.0)
    	  play(data, 8000, 16)
      n=n+1

#if __name__ == "__main__" :
#    freqList = [262, 294, 330, 349, 392, 440, 494, 523]  # ドレミファソラシド
#    for f in freqList:
#        data = createTriangleWave(0.5, f, 8000.0, 1.0)
#        play(data, 8000, 16)
