import wave
import matplotlib.pyplot as plt
import numpy as np
import os

 
f = wave.open("output.wav",'rb')
params = f.getparams()
print(f.getframerate())
nchannels, sampwidth, framerate, nframes = params[:4]

print(nchannels, sampwidth, framerate, nframes)
strData = f.readframes(nframes)#读取音频，字符串格式
waveData = np.fromstring(strData,dtype=np.int16)#将字符串转化为int
waveData.shape = -1,2
waveData = waveData.T
print(waveData)
# plot the wave
print((1.0 / framerate))
print(np.arange(0,nframes))

time = np.arange(0,nframes)*(1.0 / framerate)
print(time)
plt.plot(time,waveData)
plt.xlabel("Time(s)")
plt.ylabel("Amplitude")
plt.title("Single channel wavedata")
plt.grid('on')#标尺，on：有，off:无。
plt.show()