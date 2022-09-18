import torchaudio
from speechbrain.pretrained import SpeakerRecognition
import json
import torch
import sys
import logging
verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb",savedir="pretrained_models/spkrec-ecapa-voxceleb")

def enc_aud_id(aud_path,file_path='e.txt'):
    """
    aud_path: path of audio file to be encoded 
    file_path: path of file in which id needs to be appended 
    """
    f = open(file_path,'w')
    signal, fs =torchaudio.load(aud_path)
    signal = signal.tolist()
    f.write(str(signal[0]))
    f.close()


def load_id(file_path='e.txt'):
    f = open(file_path,'r')
    x = f.read() #reads txt file
    x = json.loads(x)   #converts it to list
    x = torch.Tensor(x) #converts list to tensor
    return x

def verify_files(tensorfile, audio_path):
    # waveform_x = self.load_audio(path_x)
    waveform_y = verification.load_audio(audio_path)

    # Fake batches:
    batch_x = tensorfile
    # batch_x = waveform_x.unsqueeze(0)
    batch_y = waveform_y.unsqueeze(0)
    # Verify:
    # print(batch_x.numpy())
    score, decision = verification.verify_batch(batch_x, batch_y)
    # Squeeze:
    return score[0], decision[0]

def speak_rec(path1text,path2audio):
     #load hparams
    print("Pass")
    sys.stdout.flush()
    tensorpath=load_id(path1text)

    score,pred = verify_files(tensorpath,path2audio) #compare files 
    if(score.numpy()[0]>0.65):
        return score
    # else:
        # return False


def speak_recog(txt_path,aud_path):
    print("Pass")
    sys.stdout.flush()
    id_tensor=load_id(txt_path)
    signal, fs =torchaudio.load('files\\anweshaudio2.wav')
    verification = SpeakerRecognition.from_hparams(source="models",savedir="pretrained_models/models") #load hparams
    score,pred = verification.verify_batch(id_tensor,signal)
    print("Pass THis",score.numpy()[0].item())
    if score.numpy()[0].item() > 0.7:
        return True
    else:
        return False



# if __name__=='__main__':
#     speak_recog()

# enc_aud_id('audiofiles/bhavyaudio.wav')


# path11=sys.argv[1]
# path12=load_id(path11)
# apath=sys.argv[2]
# print("Pass Run I Go")
# print(speak_recog(path11,apath))
# sys.stdout.flush()
