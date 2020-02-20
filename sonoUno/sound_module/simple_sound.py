# -*- coding: utf-8 -*-

import time
import platform
import numpy as np
import pygame
from scipy import signal
from data_export.data_export import DataExport as eErr


#Reproductor de sonido raw
class reproductorRaw (object):
    def __init__ (self, volume=0.5, min_freq = 110.0, max_freq = 2600.0, time_base = 1.0, duty_cycle = 1.0):
        self.Fs = 44100
        self.volume = volume
        self.minFreq = min_freq
        self.maxFreq = max_freq
        self.dutyCycle = duty_cycle
        self.setTimebase(time_base)
        self.waveform = self.get_available_waveforms()[0]
        pygame.mixer.init(self.Fs, -16, channels = 1,buffer=1024)

        self._lastFreq = 0

        """
        use en sonouno.py los metodos:
            get_waveformlist - para recuperar la lista y ponerla en la interfaz
            set_waveform - para devolverte el string de la forma de onda
                que selecciono el usuario
        si te parece bien podes usar esos nombres, sino los podes cambiar
        """

    def setVolume(self, volume):
        if volume > 100:
            volume = 100
        self.volume = volume/100.0

    def getVolume(self):
        return self.volume

    def setMinFreq(self, freq):
        self.minFreq = freq

    def getMinFreq(self):
        return self.minFreq

    def setMaxFreq(self, freq):
        self.maxFreq = freq

    def getMaxFreq(self):
        return self.maxFreq

    def setTimebase(self, time_base):
        self.timeBase = time_base
        self.nSamples = int(self.dutyCycle*self.timeBase*self.Fs)
        self.n = np.arange(0.0, self.nSamples)
        self.mask = 1/(1+np.exp((self.n-0.9*self.nSamples)/(0.1*self.nSamples)))

    def getTimebase(self):
        return self.timeBase

    def setDutyCycle(self, dc):
        self.dutyCycle = dc

    def getDutyCycle(self):
        return self.dutyCycle

    def get_available_waveforms(self):
        return ['sine','sawtooth', 'square', 'synthwave']

    def set_waveform(self, waveform):
        self.waveform = waveform

    def generate_waveform(self, freq):
        wf = self.waveform
        if self._lastFreq == 0:
            self._lastFreq = freq
        fchirp = np.linspace(self._lastFreq, freq, len(self.n) )
        self._lastFreq = freq
        x = 2*np.pi*fchirp/self.Fs*self.n
        if wf == 'sine':
            return np.sin(x)
        if wf == 'sawtooth':
            return signal.sawtooth(x)
        if wf == 'square':
            return signal.square(x)
        if wf == 'synthwave' :
            return np.sin(x)+0.25*np.sin(2*x)

    #Es el método encargado de generar las notas y reproducirlas
    def pitch (self, value, cont):
        freq = self.maxFreq*value+self.minFreq
        #El corte repentino del sonido resulta en un ruido "pop"
        #la máscara minimiza el ruido. Se puede evaluar diferentes tipos,
        #como ventanas Hamming, Hannig, Blackman...
        print(self.volume)
        f = self.mask*self.volume*2**15*self.generate_waveform(freq)
        self.sound = pygame.mixer.Sound(f.astype('int16'))
        self.sound.play()


#Esta clase es la que se comunica con la clase principal.
class simpleSound(object):
    def __init__(self):
        #instancia de la clase DataExport para imprimir los print y los errores en los archivos correspondientes
        self.expErrSs = eErr()
        #Se instancia la clase que se genera el sonido usando PyGame.
        self.reproductor = reproductorRaw()
    #Éste método modifica el valor para producir la nota y lo envía a la clase reproductorMidi
    def makeSound(self, data, x):
        try:
            if not (x == -1):
                #Aquí se llama al método que genera y envía la nota a fluidsynth
                self.reproductor.pitch(data[x], x)
            else:
                self.reproductor.pitch(0, 0, x)
        except Exception as e:
            self.expErrSs.writeexception(e)
        #En un futuro se puede pedir confirmación al método pitch y devolverla.
    #Aquí se genera el archivo de salida con el sonido, por el momento no depende del tempo seleccionado.

    def saveSound(self, path, dataX, dataY):
        #Se genera un objeto Track
        try:
            localTrack = track.Track()

        except Exception as e:
            self.expErrSs.writeexception(e)
        #Se recorre el array agregando las notas al Track.
        try:
            rango, offset = self.reproductor.getRange()
            for x in range (0, dataX.size):
                localTrack.add_notes(Note(int((dataY[x]*rango)+offset)))
        except Exception as e:
            self.expErrSs.writeexception(e)
        #Finalmente se guarda el la ruta seleccionada.
        try:
            #MidiFileOut.write_Track(path, localTrack)
            #TODO: Escribir archivo de salida (wav?)
            self.expErrSs.writeinfo("Metodo no implementado")
        except Exception as e:
            self.expErrSs.writeexception(e)
