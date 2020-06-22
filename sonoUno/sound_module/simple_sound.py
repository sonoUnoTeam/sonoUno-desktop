# -*- coding: utf-8 -*-

import time
import platform
import numpy as np
import pygame
import wave
from scipy import signal
from data_export.data_export import DataExport as eErr


#Reproductor de sonido raw
class reproductorRaw (object):
    def __init__ (self,
            volume=0.5,
            min_freq = 500.0,
            max_freq = 5000.0,
            fixed_freq = 440,
            time_base = 0.25,
            duty_cycle = 1.0,
            min_volume = 0,
            max_volume=1,
            logscale=False):
        self.f_s = 44100 #Sampling frequency
        self.volume = volume
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.fixed_freq = fixed_freq
        self.min_volume = min_volume
        self.max_volume = max_volume
        self.logscale = logscale
        self.duty_cycle = duty_cycle
        self.waveform = self.get_available_waveforms()[0]

        pygame.mixer.init(self.f_s, -16, channels = 1,buffer=1024)

        self._last_freq = 0
        self._last_time = 0

        self.set_adsr(0.01,0.15,25,0.5)
        self.set_time_base(time_base)
        self.set_discrete()
        self.set_mapping('frequency')

        self.sound_buffer = b''

        """
        use en sonouno.py los metodos:
            get_waveformlist - para recuperar la lista y ponerla en la interfaz
            set_waveform - para devolverte el string de la forma de onda
                que selecciono el usuario
        si te parece bien podes usar esos nombres, sino los podes cambiar
        """

    def set_volume(self, volume):
        if volume > 100:
            volume = 100
        self.volume = volume/100.0

    def get_volume(self):
        return self.volume

    def set_min_freq(self, freq):
        self.min_freq = freq

    def get_min_freq(self):
        return self.min_freq

    def set_max_freq(self, freq):
        self.max_freq = freq

    def get_max_freq(self):
        return self.max_freq

    def set_fixed_freq(self, freq):
        self.fixed_freq = freq

    def get_fixed_freq(self):
        return self.fixed_freq

    def set_logscale(self, logscale=True):
        self.logscale = logscale

    def set__volume(self, volume):
        self.min_volume = volume/100.0

    def set_max_volume(self, volume):
        self.max_volume = volume/100.0

    def get_max_volume(self):
        return self.max_volume

    def get_min_volume(self):
        return self.min_volume

    def set_time_base(self, time_base):
        self.time_base = time_base
        self.n_samples = int(self.duty_cycle*self.time_base*self.f_s)
        self.n = np.arange(0.0, self.n_samples)
        self.env = self._adsr_envelope()

    def get_envelope(self):
        return self._adsr_envelope()

    def get_time_base(self):
        return self.time_base

    def set_adsr(self, a, d, s, r):
        self._adsr = {'a':a,'d':d,'s':s,'r':r}

    def get_adsr(self):
        return self._adsr

    def set_duty_cycle(self, dc):
        self.duty_cycle = dc

    def get_duty_cycle(self):
        return self.duty_cycle

    def get_available_waveforms(self):
        return ['sine', 'synthwave','flute','piano',
            'celesta', 'pipe organ']

    def set_waveform(self, waveform):
        self.waveform = waveform

    def set_mapping(self, mapping):
        if mapping in ['frequency','volume']:
            self.mapping = mapping
        else:
            return -1

    def get_mapping(self):
        return self.mapping

    def set_continuous(self):
        self.set_adsr(0.1,0.15,95,0.1)
        self.continuous = True

    def set_discrete(self):
        self.set_adsr(0.01,0.15,25,0.5)
        self.continuous = False

    def _generate_tone(self, x, harmonics):
        tone = np.zeros(len(x))
        for n,a in harmonics:
            # A filter would be mor elegant, but the low freq artifact occur
            # anyway so this is the only way I found that really works
            if self._last_freq*n < 16000:
                tone += a*np.sin(n*x)
        return tone

    def generate_waveform(self, freq, delta_t=0):
        wf = self.waveform
        if self._last_freq == 0:
            self._last_freq = freq

        if self._last_time+self.get_time_base() > time.time():
            self._last_freq = freq
        f0 = self._last_freq
        f1 = freq

        t = time.time()

        if delta_t == 0:
            t0 = self._last_time
            self._last_time = t
        else:
            t0 = t - delta_t

        t1 = t0+self.get_time_base()

        if self.continuous:
            f_int = freq #(f0*(t1-t)+f1*(t-t0))/(t1-t0)
        else:
            f_int = freq

        fchirp = np.linspace(f_int, freq, len(self.n) )
        self._last_freq = freq
        x = 2*np.pi*fchirp/self.f_s*self.n
        if wf == 'sine':
            return self._generate_tone(x, [(1,1)])
        if wf == 'sawtooth':
            return signal.sawtooth(x)
        if wf == 'square':
            return signal.square(x)
        if wf == 'synthwave':
            return np.sin(x)+0.25*np.sin(2*x)
        if wf == 'flute':
            harmonics=[(1,0.6),(2.02,0.06),(3,0.02),(4,0.006),(5,0.004)]
            self.set_adsr(0.05, 0.2, 95, 0.1)
            return self._generate_tone(x, harmonics)
        if wf == 'piano':
            self.set_adsr(0.05, 0.3, 50, 0.4)
            harmonics = [(1, 0.1884), (2.05, 0.0596), (3.04, 0.0473), (3.97, 0.0631),
                (5.05, 0.0018), (6, 0.0112), (7, 0.02), (8, 0.005), (9, 0.005),
                (10, 0.0032), (12, 0.0032), (13, 0.001), (14, 0.001),
                (15, 0.0018)]
            return self._generate_tone(x, harmonics)
        if wf == 'celesta':
            self.set_adsr(0.1, 0.1, 50, 0.2)
            harmonics = [(1,0.316),(4,0.040)]
            return self._generate_tone(x, harmonics)
        if wf == 'pipe organ':
            self.set_adsr(0.1, 0.3, 20, 0.2)
            harmonics = [(0.5,0.05),(1,0.05),(2,0.05),(4,0.05),
                (6,0.014),(0.25,0.014),(0.75,0.014),
                (1.25,0.006),(1.5,0.006)]

            return self._generate_tone(x, harmonics)

    # Very simple linear AttackDecaySustainRelease implementation
    # These defaults are not meaningful
    def _adsr_envelope(self):
        a = int(self.n_samples*self._adsr['a'])
        d = int(self.n_samples*self._adsr['d'])
        s = self._adsr['s']/100.0
        r = int(self.n_samples*self._adsr['r'])
        env = np.zeros(self.n_samples)
        env[    :a] = np.linspace(0,1,a)
        env[ a:a+d] = np.linspace(1,s,d)
        env[a+d:-r] = s*np.ones(self.n_samples-a-d-r)
        env[   -r:] = np.linspace(s,0,r)
        return env

    #Es el método encargado de generar las notas y reproducirlas
    def pitch (self, value, cont):
        if self.logscale:
            value = np.log10(100*value+1)/2 #This is to achieve reasoable values
            print(value)
        if self.mapping == 'frequency':
            freq = self.max_freq*value+self.min_freq
            vol = self.volume
        else:
            vol = self.max_volume*value+self.min_volume
            freq = self.fixed_freq
        self.env = self._adsr_envelope()
        f = self.env*vol*2**14*self.generate_waveform(freq)
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
    def make_sound(self, data, x):
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

    def save_sound(self, path, data_x, data_y):
        #Se genera un objeto Track
        try:
            output_file = wave.open(path,'w')

        except Exception as e:
            self.expErrSs.writeexception(e)
        #Se recorre el array agregando las notas al Track.
        try:
            #rango, offset = self.reproductor.getRange()
            rep = self.reproductor
            sound_buffer=b''
            for x in range (0, data_x.size):
                freq = rep.max_freq*data_y[x]+self.reproductor.min_freq
                self.env = rep._adsr_envelope()
                f = self.env*rep.volume*2**15*rep.generate_waveform(freq,
                    delta_t = 1)
                s = pygame.mixer.Sound(f.astype('int16'))
                sound_buffer += s.get_raw()
                #localTrack.add_notes(Note(int((dataY[x]*rango)+offset)))
            output_file = wave.open(path,'w')
            output_file.setframerate(rep.f_s)
            output_file.setnchannels(1)
            output_file.setsampwidth(2)
            output_file.writeframesraw(sound_buffer)
            output_file.close()


        except Exception as e:
            self.expErrSs.writeexception(e)
        #Finalmente se guarda el la ruta seleccionada.
        try:
            #MidiFileOut.write_Track(path, localTrack)
            #TODO: Escribir archivo de salida (wav?)
            self.expErrSs.writeinfo("Metodo no implementado")
        except Exception as e:
            self.expErrSs.writeexception(e)
