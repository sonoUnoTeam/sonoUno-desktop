# -*- coding: utf-8 -*-

import time
import platform

from dataExport.dataExport import dataExport as eErr
from mingus.containers import track
from mingus.containers import Note
from mingus.containers.instrument import MidiInstrument
from mingus.midi import midi_file_out as MidiFileOut
#es necesario detectar el SO para importar fluidsynth
if platform.system() == 'Windows':
    import os
    local = os.getcwd()
    try:
        os.chdir(local + '\qsynth')
    except WindowsError:
        raise Exception(ImportError, "Couldn't find the FluidSynth library.")
    from mingus.midi import fluidsynth
    os.chdir(local)
else:
    from mingus.midi import fluidsynth

#Esta clase es la que se comunica con fluidsynth
class reproductorMidi (object):
    def __init__ (self):
        #instancia de la clase dataExport para imprimir los print y los errores en los archivos correspondientes
        self.expErrRep = eErr()
        #configuración para emitir sonidos midi
        #instancia de la clase MidiInstrument
        self.midiInst = MidiInstrument()
    #Método encargado de iniciar la comunicación con fluidsynth, se detectó que si no se inicia cada vez
    #que se inicia el sonido, no se escucha adecuadamente.
    def openMidi (self, soundFont):
        #Se debe detectar la plataforma, porque difieren en el driver por defecto.
        try:
            platformName = platform.system()
            if platformName == 'Windows':
                fluidsynth.init(str(soundFont).encode('ascii'), str("dsound").encode('ascii'))
            else:
                if platformName == 'Linux':
                    #fluidsynth.init(str(soundFont).encode('ascii'), str("alsa").encode('ascii'))
                    fluidsynth.init((soundFont), str("alsa").encode('ascii'))
                else:
                    if platformName == 'Darwin':
                        fluidsynth.init((soundFont), ("coreaudio"))
                    else:
                        self.expErrRep.writeInfo("The operative system is unknown, the software can't open fluidsynth.")
        except Exception as e:
            self.expErrRep.writeException(e)
    #Se planea permitir al usuario ingresar una fuente de sonido particular.
    #Aún no se conoce lo suficiente la librería mingus como para implementarlo.
#    def setSoundFont (self, soundFont):
#        fluidsynth.midi.load_sound_font(soundFont)
#        pass
    #Se permite al usuario elegir entre los diferentes instrumentos.
    def setInstrument (self, inst):
        #Los argumentos son (channel, instrument)
        #fluidsynth.midi.set_instrument(1, inst)
#        fluidsynth.midi.set_instrument(0, 11)
#        fluidsynth.midi.set_instrument(0, inst)
        #fluidsynth.midi.set_instrument(0, 10)
    #Valores para Grand piano acustico (1): 85-11
        try:
            if inst==1:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 85
                self.offset = 11
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para Piano brillante acustico (2): 95-7
        try:
            if inst==2:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 89
                self.offset = 7
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para Grand piano electrico (3): 90-8
        try:
            if inst==3:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 88
                self.offset = 8
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para Piano de cantina (4): 90-5
        try:
            if inst==4:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 90
                self.offset = 5
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para Piano Rhodes electrico (5): 67-25
        try:
            if inst==5:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 67
                self.offset = 25
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para Piano electrico chorus (6): 80-20
        try:
            if inst==6:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 80
                self.offset = 20
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para Clavicordio (7): 83-15
        try:
            if inst==7:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 81
                self.offset = 15
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para Clavecín (8): 80-13
        try:
            if inst==8:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 80
                self.offset = 13
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para Celesta (9): 95-7
        try:
            if inst==9:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 95
                self.offset = 7
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para Glockenspiel (10): 90-10
        try:
            if inst==10:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 86
                self.offset = 10
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para Caja de musica (11): 60-35
        try:
            if inst==11:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 60
                self.offset = 35
        except Exception as e:
            self.expErrRep.writeException(e)        
    #Valores para vibrafono (12): 63-30
        try:
            if inst==12:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 63
                self.offset = 30
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para marimba (13): 72-26
        try:
            if inst==13:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 72
                self.offset = 26
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para xilofono (14): 68-25
        try:
            if inst==14:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 68
                self.offset = 25
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para tubular bells (15): 70-15
        try:
            if inst==15:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 70
                self.offset = 15
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para salterio/dulcimer (16): 73-24
        try:
            if inst==16:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 73
                self.offset = 24
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para organo Hammond/ drawbar organ (17): 50-27
        try:
            if inst==17:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 50
                self.offset = 27
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para organo percusivo (18): 60-24
        try:
            if inst==18:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 60
                self.offset = 24
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para organo rock (19): 68-16
        try:
            if inst==19:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 68
                self.offset = 16
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para armonio (21): 63-23
        try:
            if inst==21:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 63
                self.offset = 23
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para organo iglesia (21): 57-20
        try:
            if inst==20:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 57
                self.offset = 20
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para acordeon (22): 55-18
        try:
            if inst==22:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 55
                self.offset = 18
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para armónica (23): 53-20
        try:
            if inst==23:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 53
                self.offset = 20
        except Exception as e:
            self.expErrRep.writeException(e)
    #Valores para bandoneón (24): NO FUNCIONA
    #Valores para guitarra española (25): 53-20
        try:
            if inst==23:
                fluidsynth.midi.set_instrument(0, inst)
                self.rango = 60
                self.offset = 15
        except Exception as e:
            self.expErrRep.writeException(e)

        #Esta última linea va al final y se utiliza para resetear, actualizar el instrumento y los rangos.
        fluidsynth.midi.fs.program_reset()
        
    #Se genera un método que devuelva los instrumentos disponibles en la fuente de sonido cargada.
    def getInstrument (self):
        #Devuelve el array con los diferentes instrumentos y el rango de notas que manejan.
        return self.midiInst.names, self.midiInst.range
    
    def getRange(self):
        return self.rango, self.offset
    
    #Es el método encargado de generar las notas y reproducirlas
    def pitch (self, value, volume, cont):
        #Se debe parar la nota antes de enviar la siguiente.
        try:
            if not (cont == -1):
                if not cont==0:
                    fluidsynth.stop_Note(self.n, 0)
                #Genera la nota a reproducir.
                self.n = Note(int(value*self.rango)+self.offset)
                #Esta parte es confusa aún.
                self.n.velocity = volume
                #Se envía la nota a reproducir.
                fluidsynth.play_Note(self.n, 0)
            else:
                fluidsynth.stop_Note(self.n, 0)
        except Exception as e:
            self.expErrRep.writeException(e)
        
#Esta clase es la que se comunica con la clase principal.
class simpleSound(object):
    def __init__(self):
        #instancia de la clase dataExport para imprimir los print y los errores en los archivos correspondientes
        self.expErrSs = eErr()
        #Se instancia la clase que se comunica con fluidsynth.
        self.reproductor = reproductorMidi()
    #Éste método modifica el valor para producir la nota y lo envía a la clase reproductorMidi
    def makeSound(self, data, x):
        try:
            if not (x == -1):
                #cuando se comience a utilizar este dato, se pedirá como parámetro de entrada.
                volume=100
                #Aquí se llama al método que genera y envía la nota a fluidsynth 
                self.reproductor.pitch(data[x], volume, x)
            else:
                self.reproductor.pitch(0, 0, x)
        except Exception as e:
            self.expErrRep.writeException(e)
        #En un futuro se puede pedir confirmación al método pitch y devolverla.
    #Aquí se genera el archivo de salida con el sonido, por el momento no depende del tempo seleccionado.
    def saveSound(self, path, dataX, dataY):
        #Se genera un objeto Track
        try:
            localTrack = track.Track()
            rango, offset = self.reproductor.getRange()
        except Exception as e:
            self.expErrRep.writeException(e)
        #Se recorre el array agregando las notas al Track.
        try:
            for x in range (0, dataX.size):
                localTrack.add_notes(Note(int((dataY[x]*rango)+offset)))
        except Exception as e:
            self.expErrRep.writeException(e)
        #Finalmente se guarda el la ruta seleccionada.
        try:
            MidiFileOut.write_Track(path, localTrack)
        except Exception as e:
            self.expErrRep.writeException(e)
    #Se genera este método por si fuera necesario en un intento por eliminar las instancias de fluidsynth
    #y volver a generarlas.
    def refreshMidi (self):
        #aquí se debe cerrar el midi!!
        try:
            del self.reproductor
            time.sleep(0.01)
            self.reproductor = reproductorMidi()
        except Exception as e:
            self.expErrRep.writeException(e)
