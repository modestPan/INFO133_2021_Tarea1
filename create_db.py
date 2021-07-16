from typing import Collection
from pymongo import MongoClient
from datetime import date
import random
import add_wavfile
import os

def create_users():
    #Generar usuario
    id_rut = random.randint(18000000,21000000)
    at_nombre = random.choice(["antonio", "ivania", "hector", "maria", "david", "jacqueline", "gustavo", "antonia", "mauro", "camila"])
    at_apellido = random.choice(["Gonzales", "Muñoz", "Rojas", "Diaz", "Perez", "Soto", "Contretas", "Silva", "Torres", "Rubio"])
    #Crear usuario
    json_usuario = {
        "_rut":id_rut,
        "nombre":at_nombre,
        "apellido":at_apellido,
    }
    return json_usuario

def subir_audio(db):
    #Generar datos del audio
    at_exterior = random.choice(["exterior", "interior"])
    at_fecha_grabacion = random.choice(["12/10/2020","13/12/2019","2/3/2021","7/4/2021",])
    at_ciudad = "valdivia"

    '''
    >Coordenadas valdivia
     -73.24733754416314  S
      -73.21025868964128   N
     -39.80345745699139   E
     -39.828246046467164  O
    '''

    at_latitud = random.uniform(-73.21025868964128, -73.24733754416314 )
    at_longitud = random.uniform(-39.80345745699139, -39.828246046467164)
    
    #Generar usuario
    at_usuario = create_users()
    
    #importar audio
    up_audio = add_wavfile.importwav(db)
    at_duracion = up_audio["duracion"]
    at_formato = up_audio["formato"]
    at_url = up_audio["direccion"]
    at_audio = up_audio["audio"]

    #Segmentar audio
    at_segmentos = []
    for i in range(random.randint(0,5)):
        at_segmentos.append(segmentar_audio(up_audio))
    
    #Crear audio
    json_audio = {
        "fecha_grabacion": at_fecha_grabacion,
        "ciudad": at_ciudad,
        "duracion": at_duracion,
        "formato": at_formato,
        "latitud": at_latitud,
        "longitud": at_longitud,
        "exterior": at_exterior,
        "usuario": at_usuario,  
        "url_audio": at_url,
        "audio": at_audio,
        "segmentos": at_segmentos  
    }
    return json_audio

def segmentar_audio(audio):
    '''
        crear distintos segmentos de audio en base al audio importado
    '''
    
    #Generar etiqueta
    at_nombre_fuente = random.choice(["Humanos", "Musica", "Animales", "Climaticos y Medio ambientales", "Mecanicos"])
    at_descripcion = "Descripcion del segmento..."
    at_id_analizador = random.randint(1,10000000)

    #Crear etiqueta
    etiqueta = {
        "nombre_fuente": at_nombre_fuente,
        "descripcion": at_descripcion,
        "id_analizador": at_id_analizador
    }

    at_formato = audio["formato"]
    at_duracion = random.uniform(0, 30)

    if(audio["duracion"] > at_duracion):
        at_duracion = random.uniform(0,audio["duracion"])
    
    at_inicio = audio["duracion"]  - at_duracion
    at_fin = at_duracion + at_inicio
    segmento = {
        "formato": at_formato,
        "duracion": at_duracion,
        "inicio": at_inicio,
        "fin": at_fin,
        "etiquetas": etiqueta
    }
    return segmento

def main():
    MONGO_URI = 'mongodb://localhost'
    client = MongoClient(MONGO_URI)
    # crea la base de datos 
    db = client['KevinMedina_FUSA']  # <-- almacena la base de datos}
    colAudios = db["Audios"]
    for i in range(15):
        colAudios.insert_one(subir_audio(db))
main()

