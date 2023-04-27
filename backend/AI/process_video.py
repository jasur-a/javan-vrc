#!/usr/bin/env python
# coding: utf-8

# Manipulación de Audio 
import moviepy.editor as mp
from pytube import YouTube 

# Otras librerías
import os, shutil
from AI.sound_to_text import read_audio_file, get_audio_transcription

# Variables globales
to_audio = os.getcwd() + "/"+ "Converted_audio.wav"
current_folder = os.getcwd() + "/Converted_results"

    
    #def __init__(self, video_file):
        # self.path = path
        # self.videoUrl = url
        # self.name = ""
        # self.yt = self.Download()
        # self.localUrl = ''
        #self.yt = ''


     #   self.video_file = video_file
    #    self.video_description = ""
        #self.current_folder = self.current_directory + "/Converted_results"
        
    # def Download(self):
    #     #por ahora para archivos de internet
    #     file = self.Network()
    #     print(file)
    #     return file

    # def Network(self):
    #     yt = YouTube(self.videoUrl)
    #     yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    #     if not os.path.exists(self.path):
    #         os.makedirs(self.path)
    #     localUrl = yt.download(self.path)
    #     self.localUrl = localUrl
    #     return yt


"""
Descarga un video de YouTube.
"""
def download_from_youtube(video_file):
    yt_file = YouTube(video_file)
    video_description = yt_file.description
        
    yt_file = yt_file.streams.get_highest_resolution()
    if not os.path.exists(current_folder):
        os.makedirs(current_folder)
    yt_file.download(current_folder)
        
    return video_description
    #  yt_file.close()


def extract_text(video_file):
    yt_file = YouTube(video_file)
    video_description = yt_file.description
        
    yt_file = yt_file.streams.get_highest_resolution()
    if not os.path.exists(current_folder):
        os.makedirs(current_folder)
    yt_file.download(current_folder)
        
    return video_description
     #  yt_file.close()

    
"""
Convierto un video a audio. 
"""
def convert_video_to_audio(video_file, type):
    if type == "url": #optimizar en frontend
        video_description = download_from_youtube(video_file)
        convert_to_audio()
        read_audio_file()
        get_audio_transcription(video_description)
    else:
        #video_file = os.getcwd() + "\Converted_results\Chiles Rellenos sin Capear De Mi Rancho A Tu Cocina.mp4"
        print(video_file)
        to_audio = os.getcwd() + "/"+ "Converted_audio.wav"
        clip = mp.VideoFileClip(video_file)
        clip.audio.write_audiofile(to_audio)
        print("Conversión a audio ha sido finalizada...")
        read_audio_file()
        get_audio_transcription()
    #self.remove_filed() #TODO error => no elimina mp4
        

"""
Convierte un video a audio.
"""
def convert_to_audio():
    for file in os.listdir(current_folder):
        file = current_folder + "/" + file
        if file.endswith(".mp4"):
            raw_string = r"{}".format(file)
            raw_audio = r"{}".format(to_audio)
                
            clip = mp.VideoFileClip(raw_string)
            clip.audio.write_audiofile(raw_audio)
            print("Conversión a audio ha sido finalizada...")
                
    
"""
Elimina todos los archivos de la carpeta creada al finalizar el procesamiento.
El archivo de texto se guarda en la nube. #TODO
"""
def remove_filed():
    for filename in os.listdir(current_folder):
        file_path = os.path.join(current_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            