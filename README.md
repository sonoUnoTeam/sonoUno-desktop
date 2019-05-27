# sonoUno
SonoUno is a sonification software for two column tables of astronomical data. The develop language is Python and we use modular design, in order to do collaborative work. The sonoUno now is multiplatform, tested on windows, Ubuntu y Mac High Sierra; the development team work continuously to maintain this benefit. The principal goal of the SonoUno is to allow the user to open data files (txt or csv extension), reproduce the plot and sonification of the data. At the moment, the sonification is perform by variation of pitch in differents instruments.
Additionally, SonoUno allow to select a specific range of data on the abscissas axis, mark and save point of interest in the data, and apply predefined mathematical functions (for example, logarithm and square). In the section settings, the user can configure the plot and change between several predefined instruments (acoustic piano, clavinet, celesta and tubular bells, between others). We expect to include more sound configurations shortly.
Finally, the software allows the user to save the sound, the plot and a text file with the points marked on the data.

# Software installation
## 1. Ubuntu
### 1.1. Python and needed libraries
If you installed previously the soft at your computer, do not take into account this section. If not, the next steps are the libraries installation.
1.	Go to the Ubuntu terminal and execute the ‘python’ command:
2.	If the version is 3.x.x, type exit() and check with ‘python2’. If the version here is 2.7.x we can continue with the following steps, if not, you must  install or update python 2.7 in the operating system, using the command:
2.a.	sudo apt-get install --upgrade python
3.	Once that we checked that we have python 2.7 installed (is called python2 in this instructive), we can proceed with the libraries installation.
4.	First you have to type:
4.a.	sudo apt update
5.	Install wxPython with the next command:
5.a.	python2 -m pip install --user -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython
NOTE: The installation can take several minutes, be patient. If the installation take more than 30 minutes cancel the process (Ctrl+C) and execute the command once again.
6.	Install matplotlib 2.2.3 or upper:
6.a.	python2 -m pip install --user -U matplotlib
7.	Install pandas:
a.	python2 -m pip install --user -U pandas
8.	Install numpy: 
8.a.	sudo python2 -m pip install -U numpy
9.	Install fluidsynth:
9.a.	sudo apt-get install fluidsynth
10.	Install mingus:
10.a.	python2 -m pip install --user -U mingus
NOTE: If any of the last libraries (from 5 to 10) is missing, the soft does not run. The installation can take several minutes.
### 1.2. Run the software
1.	Unzip the file or download the git repository.
2.	Open a terminal and go to the software folder. Probably you have more than one folder before you can run SonoUno.
3.	To check in which folder is sonoUno.py, use the command “ls”. The sonoUno.py must be among the files in the folder.
4.	Once you are sure that you are at the right folder, make:
4.a.	python2 sonoUnoB.py
NOTE: If you have the error “ImportError: libSDL-1.2.so.0: cannot open shared object file: No such file or directory”; run “sudo apt-get install libsdl-ttf2.0-0”. If don’t solve the problem, contact the development team.
5.	A window must be open, if that is the case, the soft is ready to be used.

## 2. MacOS
### 2.1. Python and needed libraries
If you installed previously the soft at your computer, do not take into account this section. If not, the next steps are python and the libraries installation.
1.	Go to the terminal and execute the ‘python’ command:
2.	If the version is 3.x.x, type exit() and check with ‘python2’. If the version is 2.7.x, you can continue with the following steps. If not, you must update or install python 2.7.15 in the operating system, using the installer on https://www.python.org/ftp/python/2.7.15/python-2.7.15-macosx10.6.pkg 
3.	After install python, check if you have pip installed on your system with the next command:
3.a.	python2 -m pip -V
NOTE: To install pip you can try “easy_install pip” or “sudo easy_install pip” if admin privilege is needed.
4.	Once that we checked that we have python 2.7.x and pip installed (is called python2 in this instructive), we can proceed with the libraries installation.
5.	Install wxPython 4.0 with the next command: 
5.a.	python2 -m pip install --user wxPython 
NOTE: The installation can take several minutes, be patient. If the installation take more than 30 minutes cancel the process (Ctrl+C) and execute the command once again.
6.	Install matplotlib 2.2.3 or upper: 
6.a.	python -m pip install --user matplotlib
7.	Install pandas: 
7.a.	python -m pip install --user pandas
8.	Install numpy: 
8.a.	python -m pip install --user numpy
9.	Install fluidsynth: 
9.a.	brew install fluid-synth
10.	Install mingus: 
10.a.	python -m pip install --user mingus
NOTE: If any of the last libraries (from 5 to 10) is missing, the soft does not run. The installation can take several minutes.
### 2.2. Run the software
1.	Unzip the file or download the git repository.
2.	Open a terminal and go to the software folder. Probably you have more than one folder before you can run SonoUno.
3.	To check in which folder is sonoUno.py, use the command “ls”. The sonoUno.py must be among the files in the folder.
4.	Once you are sure that you are at the right folder, make:
4.a.	python sonoUnoB.py
5.	A window must be open, if that is the case, the soft is ready to be used.

## 3. Windows
### 3.1. Prerequisites
Only for windows, the better installation of fluidsynth is through the QSynth software, located in https://sourceforge.net/projects/qsynth/files/. You can download an executable file and install this software.
When you have the installer, by default in Download folder of the file system. To execute the installer, do double click on the file named “qsynth-x.x.x-setup”. If the installer ask for permission click Yes.
The first window is a welcome and recommendation, click Next to continue. Next, the license agreement is shown, the user can read the text and then click “I Agree” to continue with the process. The QSynth setup ask for the destination folder, by default is “C:\Program Files (x86)\QSynth”. The next step is for select the destination folder of the start menu and then press “Install”. The installation process takes a few minutes, with a status bar that is filling on the window. When the installation is finished the “Next” button is enable (Image 33), and the final window said that the program is installed on the computer.
If you don't have python 2.7 installed, an installer is provide on the official website (https://www.python.org/downloads/release/python-2715/). Once you have the installer, double click on it. Maybe the installer ask for confirmation, click Execute.
The first step on the python installer is to select whether to install python: for all users or just for me; in this tutorial “Install just for me” was selected. Next, the user can select the destination directory, by default is “C:\Python27\”. Then, the installer allows the user to customize the installation, in this window the default settings are keep. When the next button are press the installer ask for permission before installing the software, click yes and the next window present a status bar that is filling. Finally, the last windows inform that the process is complete.
The next important step is to set the environment variables, the only part that differs between Windows 7 and 10 is the location of control panel button on the start menu. On Windows 7, click the start menu and the control panel button is on the right, but on Windows 10, the user have to select “All apps” and search for “Window system” folder, the control panel button is inside this folder.
In the control panel window, select “System and security”, then “System” and finally, “Advance system settings”. In the new window bottom the user can find the “Environment variables” button, witch one open the environment variables window, where the user can set the PATH variable.
Another way to access to the environment variables windows is typing “environment variable” on the start menu, the button “Edit the system environment variables” open the same window that the first way.
Once the user is in the environment variables window, if the user variable PATH exist, the user has to click on “Edit” and add the new path to the variable. On the other hand, if the PATH user variable does not exist, the user must click on the “New” button, that action open a pop-up window where the user can set the variable name and value. The name of the variable is “PATH” and the value is the new path, in this case the directory of the QSynth installation folder (by default C:\Program Files (x86)\QSynth) and the two directories needed for python: C:\Python27 and C:\Python27\Scripts. Finally, click Ok and Ok.
The last part is to install the libraries, to do that the user have to open the command window, typing “cmd” or "Windows PowerShell" (the last, only on windows 10) on the start menu. Follow the nexts steps:
1.	Install wxPython with the next command: 
1.a.	python -m pip install -U wxPython 
NOTE: The installation can take several minutes, be patient. If the installation take more than 30 minutes cancel the process (Ctrl+C) and execute the command once again.
2.	Install matplotlib 2.2.3 or upper:
2.a.	python -m pip install -U matplotlib
3.	Install pandas:
3.a.	python -m pip install -U pandas
4.	Install numpy: 
4.a.	python -m pip install -U numpy
5.	Install mingus:
5.a.	python -m pip install -U mingus
NOTE: If any of the last libraries (from 1 to 5) is missing, the soft does not run. The installation can take several minutes.
### 3.2. Run the software
1.	Unzip the file or download the git repository.
2.	Open a terminal and go to the software folder. Probably you have more than one folder before you can run SonoUno.
3.	To check in which folder is sonoUno.py, use the command “dir”. The sonoUno.py must be among the files in the folder.
4.	Once you are sure that you are at the right folder, make:
4.a.	python sonoUnoB.py
5.  A window must be open, if that is the case, the soft is ready to be used.

# Using the software
The initial window of the software only shows the plot and the reproduction options of the data, the other functionalities are hide and were shown in the next chapters. This design was based on a user cases study.
In order to probe the SonoUno, you have to import a data file. If you don’t have a data file, the installer provide a folder named “sample_data” with simple functions on the software directory.
The first step to open a data file, is to select the item Open on the menu File. This action shows a new windows of the file system of the computer, where you can choose the data file. Once you have the data file selected, press the button “Open”.
After open the data file, the SonoUno show the plot and is ready to reproduce the pitch variation in Piano. In order to reproduce the sound, you have to press the button Play. If the software installation is correct, you must listen a pitch variation on Piano and see a red vertical bar moving through the data, this bar indicate the position of the data that is been sonificated.
If the software doesn’t produce sound, check the speakers or headphones on your computer. If the problems continue or you have another problem, inform this to the developer team.
