'''
A simple example of using pyroomacoustics to simulate
sound propagation in a shoebox room and record the result
to a wav file.
'''
from __future__ import print_function
import numpy as np
import pyroomacoustics as pra
from scipy.io import wavfile
import os
import copy

def roomSim(sourcePath, outputPath, roomDim, sourcePos, micPos):
    
    fs, audio_anechoic = wavfile.read(sourcePath)

    shoebox = pra.ShoeBox(
        roomDim,
        absorption=0.2,
        fs=fs,
        max_order=15,
        )

    shoebox.add_source(sourcePos, signal=audio_anechoic)
    shoebox.add_microphone_array(
            pra.MicrophoneArray(
                micPos, 
                shoebox.fs)
            )

    shoebox.simulate()

    audio_reverb = shoebox.mic_array.to_wav(outputPath, norm=True, bitdepth=np.int16)
    return audio_reverb

def random_roomDim(roomDimArray):
    for i in range(roomDimArray.shape[0]):
        for j in range(roomDimArray.shape[1]):
            roomDimArray[i][j] = np.random.randint(3.,8.)
    return roomDimArray

def random_sourcePos(sourcePosNormaliziedArray):
    for i in range(sourcePosNormaliziedArray.shape[0]):
        for j in range(sourcePosNormaliziedArray.shape[1]):
            sourcePosNormaliziedArray[i][j] = round(np.random.uniform(0.01,0.99),2)
    return sourcePosNormaliziedArray
            
def random_micPos(micPosNormaliziedArray):
    for i in range(micPosNormaliziedArray.shape[0]):
        for j in range(micPosNormaliziedArray.shape[1]):
            micPosNormaliziedArray[i][j][0] = round(np.random.uniform(0.01,0.99),2)
    return micPosNormaliziedArray


def save_txt(audioFilePath,acousticPath,  roomDim, sourcePos, micPos):
    audioFilePath = os.getcwd() +'\\audio\\'
    if not os.path.exists(audioFilePath):
        os.makedirs(audioFilePath)
    file_txt = open(audioFilePath + acousticPath + str(roomDim) + str(sourcePos) + str(micPos[:,0]) +str(micPos[:,1]) + '.txt','wt')
    file_txt.write('room information\n\n')
    file_txt.write('roomDim(m):\n')
    np.savetxt(file_txt,roomDim,fmt='%.2f')
    file_txt.write('sourcePos(m):\n')
    np.savetxt(file_txt,sourcePos,fmt='%.2f')
    file_txt.write('micPos(m):\n')
    np.savetxt(file_txt,micPos,fmt='%.2f')
    file_txt.close()
        
if __name__ == "__main__":
    
    n_room = int(input('please input the number of the room:'))
    n_sp = int(input('please input the number of the sourcePosition:'))
    n_mp = int(input('please input the number of the micPosition:'))
    roomDimArray = np.zeros([n_room,3])  #initialize
    sourcePosNormaliziedArray = np.zeros([n_sp,3])
    micPosNormaliziedArray = np.zeros([n_mp,3,2])
    random_roomDim(roomDimArray)         #Randomly generate room information
    random_sourcePos(sourcePosNormaliziedArray)
    random_micPos(micPosNormaliziedArray)
    acousticFilePath = os.getcwd()+'\\acoustic\\'  #get all paths of acoutiscs
    acousticPathList = os.listdir(acousticFilePath)

    for roomDim in roomDimArray:
        for sourcePosNormalizied in sourcePosNormaliziedArray:
            sourcePos = copy.copy(sourcePosNormalizied)
            sourcePos = sourcePos*roomDim
            for acousticPath in acousticPathList:
                sourcePath = copy.copy(acousticPath)
                sourcePath = os.path.join('%s%s' % (acousticFilePath, sourcePath))
                for mic in micPosNormaliziedArray:
                    micPos = copy.copy(mic)
                    for j in range(micPosNormaliziedArray.shape[2]):
                        for i in range(micPosNormaliziedArray.shape[1]):
                            if j==0:
                                micPos[i,:] = micPos[i,:]*roomDim[i]
                            if (j==1)&(i==0):
                                micPos[:,j] = micPos[:,(j-1)] + [0.1,0,0]
                    audioFilePath = os.getcwd() +'\\audio\\'
                    if not os.path.exists(audioFilePath):
                        os.makedirs(audioFilePath)
                    outputPath = audioFilePath + acousticPath + str(roomDim) + str(sourcePos) + str(micPos[:,0]) +str(micPos[:,1]) + '.wav'
                    save_txt(audioFilePath,acousticPath,  roomDim, sourcePos, micPos)
                    roomSim(sourcePath, outputPath, roomDim, sourcePos, micPos)
