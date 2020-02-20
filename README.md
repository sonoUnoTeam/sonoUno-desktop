# SonoUno Software

## Description

SonoUno is a sonification software for two or more column tables of astronomical data. The software is being developed based on the study of other software (Sonification Sandbox, MathTrax and xSonify) and standards of accessibility like the ISO 9241-171:2008 (Guidance on software accessibility). In order to develop the first approach of graphical user interface, we perform a theoretical framework based on bibliography of user cases, focused on blind and visual impairment people.
The develop language is Python and we use modular design, in order to do collaborative work. The sonoUno now is multiplatform, tested on windows 10, Ubuntu 16, Ubuntu 18, CentOS 7, Mac Mojave and Mac Catalina; the development team work continuously to maintain this benefit. The principal goal of the SonoUno is to allow the user to open data files (txt or csv extension), reproduce the plot and sonification of the data.
Additionally, SonoUno allow to select a specific range of data on the abscissas axis, mark and save point of interest in the data, and apply predefined mathematical functions (for example, logarithm and square). In addition, the SonoUno present a bridge with Octave and allow to perform some mathematical functions with this tool on the software window. In the section settings, the user can configure the plot. We expect to include some sound configurations shortly.
Finally, the software allows the user to save the sound, the plot and a text file with the points marked on the data.

## Installation

You can install the software from source following the Install instruction. You can find one Install file in this repository for each operative system.

## Opening the software

1.	Clone or download the git repository.
2.	Open a terminal and go to the software folder. Probably you have more than one folder before you can run SonoUno.
3.	To check in which folder is sonoUno.py, use the command “ls”. The sonoUno.py must be among the files in the folder.
4.	Once you are sure that you are at the right folder, make:
```
python sonoUno.py
```
5.  A window must be open, if that is the case, the soft is ready to be used.

## Using the software

The initial window of the software only shows the plot and the reproduction options of the data, the other functionalities are hide and were shown in the user manual (is a pdf file located on this repository).
In order to probe the SonoUno, you have to import a data file. If you don’t have any data file, the installer provide a folder named “sample_data” with simple functions on the software directory.
The first step to open a data file, is to select the item Open on the menu File. This action shows a new windows of the file system of the computer, where you can choose the data file. Once you have the data file selected, press the button “Open”.
After open the data file, the SonoUno show the plot and is ready to reproduce the sound. In order to reproduce the sound, you have to press the button Play. If the software installation is correct, you must listen the sound and see a red vertical bar moving through the data, this bar indicate the position of the data that is been sonify.
If the software doesn’t produce sound, check the speakers or headphones on your computer. If the problems continue or you have another problem, inform this to the developer team.
