#!/usr/bin/env python
# coding: utf-8

# Reconocimiento de Audio
import speech_recognition as sr


# Manipulación de Audio 
from pydub import AudioSegment
from pydub.silence import split_on_silence 

# Otras librerías
import os

to_audio = os.getcwd() + "/Converted_audio.wav"


""" 
Lee el video de audio. 
"""
def read_audio_file():
    read = sr.AudioFile(to_audio)
    print("Audio ha sido leído...")
    return read
     
"""
Define una función para normalizar un fragmento a una amplitud dada.
"""
def match_target_amplitude(audio_chunk, target_dBFS):
    change_in_dBFS = target_dBFS - audio_chunk.dBFS
    return audio_chunk.apply_gain(change_in_dBFS)

"""
 Divide archivo de audio en fragmentos.
"""
def create_audio_chunks(audio):
    chunks = split_on_silence(audio,
        min_silence_len = 500,
        silence_thresh = -40
    )
    return chunks

"""
Se obtiene la transcripción del audio.
"""
def get_audio_transcription(video_description = ""):
    print("::video_description :", video_description)
    r = sr.Recognizer()
        
    # Se aplica speech recognition
    path = to_audio
        
    # Abre el archivo de audio
    folder_name = path.replace("wav","")
    
    # Crea el archivo de texto.
    fh = open(folder_name + "txt", "w+") 
    audio = AudioSegment.from_wav(path)  
    
    # Divide el audio en fragmentos.
    chunks = create_audio_chunks(audio)
    
    # Crea un directorio para almacenar los fragmentos de audio
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""

    # Procesa cada fragmento.
    for i, audio_chunk in enumerate(chunks, start=0):
        silence_chunk = AudioSegment.silent(duration=500)
            
        # Agrega un padding al inicio y al final de todo el fragmento.
        audio_chunk = silence_chunk + audio_chunk + silence_chunk
            
        # Exporta fragmento de audio y se guarda en el directorio. 
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            
        # Normaliza el fragmento completo.
        normalized_chunk = match_target_amplitude(audio_chunk, -20.0)
            
        normalized_chunk.export(chunk_filename, bitrate = "192k", format="wav")
            
        # Se preprocesa el fragmento.
        with sr.AudioFile(chunk_filename) as source:
            r.energy_threshold = 400
            r.adjust_for_ambient_noise(source, duration=0.5)
                
            audio_file = r.record(source)
            
            try:  
                text = r.recognize_google(audio_file, language='es-MX') 
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text} "
                whole_text += text
                    
    # Si existe una descripción, se agregará en el archivo de texto.
    video_description = "\nDescripción del Video: \n" + str(video_description)
    whole_text += video_description
        
    #word = "ingredientes" # TODO cambiar palabras 
    #if not word in whole_text:
    #    print("No es video-receta!")
     #    return
        
    # Guarda el texto completo del video.
    fh.write(whole_text + "\n") 
    fh.close() 
    return whole_text
    

#videourl = "https://www.youtube.com/watch?v=eQpAi5CogiQ"  #"https://www.youtube.com/watch?v=TzbvfPaGHl4" #(rajas) # "https://www.youtube.com/watch?v=eQpAi5CogiQ" (chiles) #https://www.youtube.com/watch?v=TzbvfPaGHl4 (con ingredientes)"  #"https://www.youtube.com/watch?v=qi3V_ArpDp4" 
#to_text = SoundToText(videourl)





