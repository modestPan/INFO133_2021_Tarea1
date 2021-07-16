import wave
import contextlib
import random
from base64 import b64encode
import gridfs

def importwav(db):

    #Se crean las variables iniciales del audio
    nombres = random.choice(["car", "catpur", "guau", "meow", "patting", "seacreature", "water"])
    at_formato = ".wav"
    file_url = 'Sonidos/'
    file_url = file_url + nombres + at_formato
    at_duracion = 0
    
    #Se calcula la duracion del audio
    with contextlib.closing(wave.open(file_url,'r')) as f: 
        frames = f.getnframes()
        audio = f
        rate = f.getframerate()
        at_duracion = frames / float(rate)    
    
    #Se guarda audio en la base de datos
    with open(file_url, 'rb') as fd:
        contents = fd.read()
        audio= b64encode(contents)
    filename = nombres
    fs = gridfs.GridFS(db)
    fielid = fs.put(audio, filename = filename)
    aud = {"filename": filename, "fieldif":fielid}

    #Se crea el audio para la base de datos
    json_wav = {
        "duracion": at_duracion,
        "formato": at_formato,
        "direccion": file_url,
        "audio": aud
    }   

    return json_wav