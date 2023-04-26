#!/usr/bin/env python
# coding: utf-8

import os, shutil
from pytube import YouTube 
import json
class Video(object):
    """
    Define un archivo con formato de video.
    """
    def __init__(self, video_file):
        # self.path = path
        # self.videoUrl = url
        # self.name = ""
        # self.yt = self.Download()
        # self.localUrl = ''
        #self.yt = ''

        self.video_name = ""
        self.videoUrl = ""
        self.video_file = video_file
        self.current_directory = os.getcwd()
        self.video_description = ""
        self.current_folder = self.current_directory + "/Converted_results"
        self.converted_audio = self.current_folder + "/"+ "Converted_audio.wav"
        
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
    def download_from_youtube(self):
        yt_file = YouTube(self.video_file)
        self.video_description = yt_file.description
        
        yt_file = yt_file.streams.get_highest_resolution()
        if not os.path.exists(self.current_folder):
            os.makedirs(self.current_folder)
        yt_file.download(self.current_folder)
      #  yt_file.close()


    def extract_text(self):
        yt_file = YouTube(self.video_file)
        self.video_description = yt_file.description
        
        yt_file = yt_file.streams.get_highest_resolution()
        if not os.path.exists(self.current_folder):
            os.makedirs(self.current_folder)
        yt_file.download(self.current_folder)
      #  yt_file.close()


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

