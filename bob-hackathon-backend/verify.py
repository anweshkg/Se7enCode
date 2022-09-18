from traceback import print_tb
import face_final as face
import speak_rek as speech
import sys,json
from pydub import AudioSegment
import os



if len(sys.argv) != 4:
    print("False")
    sys.stdout.flush()
    sys.exit()
print("Arg Pass Complete")
if ('.txt' in sys.argv[1]):
    with open(sys.argv[1],'r',encoding='utf-8') as f:
        fid_list=f.read()
else:
    fid_list=sys.argv[1]
face_data = json.loads(fid_list)
os.system(f"ffmpeg -i files\\{sys.argv[2]} -acodec pcm_s16le -ar 16000 files\\{sys.argv[2].replace('.mp4','.wav').replace('.webm','.wav')}")
speech_list_path = sys.argv[3]
apath = 'files\\'+sys.argv[2].split('.')[0]+'.wav'

s = speech.speak_recog(speech_list_path,apath)
print("Pass Ran Face")
f = face.face_verify_fromDB(face_data,sys.argv[2])  
if (s and f):
    print("True")
else:
    print("False")