#!/usr/bin/env python
# coding: utf-8

# In[1]:


#python -m pip install SpeechRecognition moviepy  pafy pattern3  pydub --upgrade youtube_dl
# python -m pip install pytube


# In[2]:


#pip install SpeechRecognition moviepy
#pip install pafy
#pip install --upgrade youtube_dl

# Reconocimiento de Audio
import speech_recognition as sr
import moviepy.editor as mp

# Manipulación de Audio 
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pytube import YouTube 

# Otras librerías
import os, shutil
import json


# In[3]:


class SoundToText(object):
    """
    Define un archivo con formato de video.
    """
    def __init__(self, video_file):
        self.video_file = video_file
        self.current_directory = os.getcwd()
        self.video_description = ""
        self.current_folder = self.current_directory + "/Converted_results"
        self.converted_audio = self.current_folder + "/"+ "Converted_audio.wav"
    
    """
    Convierto un video a audio. 
    """
    def convert_video_to_audio(self):
        if "youtube" in self.video_file: #optimizar en frontend
            self.download_from_youtube()
            self.convert_to_audio()
            self.read_audio_file()
            self.get_audio_transcription()
        else:
            self.read_audio_file()
            self.get_audio_transcription()
        #self.remove_filed() #TODO error => no elimina mp4
        
    """
    Descarga un video de YouTube.
    """
    def download_from_youtube(self):
        yt_file = YouTube(self.video_file)
        self.video_description = yt_file.description
        
        yt_file = yt_file.streams.get_highest_resolution()
        if not os.path.exists(self.current_folder):
            os.makedirs(self.current_folder)
        yt_file.download(self.current_folder)
      #  yt_file.close()
     
    """
    Convierte un video a audio.
    """
    def convert_to_audio(self):
        for file in os.listdir(self.current_folder):
            file = self.current_folder + "/" + file
            if file.endswith(".mp4"):
                raw_string = r"{}".format(file)
                raw_audio = r"{}".format( self.converted_audio)
                
                clip = mp.VideoFileClip(raw_string)
                clip.audio.write_audiofile(raw_audio)
                print("Conversión a audio ha sido finalizada...")
                   
    """ 
    Lee el video de audio. 
    """
    def read_audio_file(self):
        audio = sr.AudioFile(self.converted_audio)
        print("Audio ha sido leído...")
     
    """
    Define una función para normalizar un fragmento a una amplitud dada.
    """
    def match_target_amplitude(self, audio_chunk, target_dBFS):
        change_in_dBFS = target_dBFS - audio_chunk.dBFS
        return audio_chunk.apply_gain(change_in_dBFS)

    """
    Divide archivo de audio en fragmentos.
    """
    def create_audio_chunks(self, audio):
        chunks = split_on_silence(audio,
            min_silence_len = 500,
            silence_thresh = -40,
        )
        return chunks

    """
    Se obtiene la transcripción del audio.
    """
    def get_audio_transcription(self):
        r = sr.Recognizer()
        
        # Se aplica speech recognition
        path = self.converted_audio
        
        # Abre el archivo de audio
        folder_name = path.replace("wav","")
    
        # Crea el archivo de texto.
        fh = open(folder_name + "txt", "w+") 
        audio = AudioSegment.from_wav(path)  
    
        # Divide el audio en fragmentos.
        chunks = self.create_audio_chunks(audio)
    
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
            normalized_chunk = self.match_target_amplitude(audio_chunk, -20.0)
            
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
        video_description = "\nDescripción del Video: \n" + str(self.video_description)
        whole_text += video_description
        
        #word = "ingredientes" # TODO cambiar palabras 
        #if not word in whole_text:
        #    print("No es video-receta!")
        #    return
        
        # Guarda el texto completo del video.
        fh.write(whole_text + "\n") 
        fh.close() 
        return print("\nFull text:", whole_text)
    
    """
    Elimina todos los archivos de la carpeta creada al finalizar el procesamiento.
    El archivo de texto se guarda en la nube. #TODO
    """
    def remove_filed(self):
        for filename in os.listdir(self.current_folder):
            file_path = os.path.join(self.current_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


# In[4]:


#videourl = "https://www.youtube.com/watch?v=eQpAi5CogiQ"  #"https://www.youtube.com/watch?v=TzbvfPaGHl4" #(rajas) # "https://www.youtube.com/watch?v=eQpAi5CogiQ" (chiles) #https://www.youtube.com/watch?v=TzbvfPaGHl4 (con ingredientes)"  #"https://www.youtube.com/watch?v=qi3V_ArpDp4" 
#to_text = SoundToText(videourl)


# In[5]:


#to_text.current_folder


# In[6]:


#to_text.convert_video_to_audio()


# In[ ]:




