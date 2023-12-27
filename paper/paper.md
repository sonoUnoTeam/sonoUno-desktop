---
title: 'SonoUno development: a User-Centered Sonification software for data analysis'
tags:
  - sonification
  - inclusion
  - astrophysics
  - open source
  - user-centered design
  - graphic user interface
authors:
  - name: Johanna Casado
    orcid: 0000-0001-9528-5034
    corresponding: true 
    affiliation: "1, 2" # (Multiple affiliations must be quoted)
  - name: Gonzalo de la Vega
    equal-contrib: true # (This is how you can denote equal contributions between multiple authors)
    affiliation: 3
  - name: Beatriz García
    orcid: 0000-0003-0919-2734
    equal-contrib: true 
    affiliation: "1, 4"
affiliations:
 - name: Instituto en Tecnologías de Detección y Astropartículas (CNEA, CONICET, UNSAM), Mendoza, Argentina
   index: 1
 - name: Instituto de Bioingeniería, Facultad de Ingeniería, Universidad de Mendoza, Argentina
   index: 2
 - name: Independent Researcher, Argentina
   index: 3
 - name: Universidad Tecnológica Nacional - Regional Mendoza, Argentina
   index: 4
date: 14 June 2023
bibliography: paper.bib

---

# Summary

In general, people think about information and nature based on a visual approach, but if we go back to our childhood and try to understand the world through our different senses, a new way of understanding the information arises. Sonification is a technique that uses non-speach audio to translate data into sound and it is a commonly-used approach to exploring astrophysical data through sensory inputs. This field has grown continuously over the recent years, especially since 1992 with the start of the International Community for Auditory Display (ICAD) conferences. In this contribution, a sonification software, sonoUno, and its application in astronomy are presented, without neglecting the analysis possibilities for data from various disciplines. The main distinguishing features of the development presented here are: it is user-centered from the beginning, with several contacts with end users along the design and a focus group test; it seeks a way to bring autonomy to its functionally-diverse users; and it presents a simple first framework, with the mathematical operations and settings in the menu. A description of the software and some cases of use are presented.

# Introduction

The use of sonification in astronomy has existed for years, some recent examples are a sonification of the zCOSMOS astronomical dataset, where the authors describe the dataset and the sonification strategy used [@bardellietal2021]; the LightSound, an electronic device that allows the conversion of light into sound and it is used to observe eclipses [@lightsound2020]; See-Through-Sound, a project dedicated to converting images into sound to allow visually impaired people to detect objects around them [@henriquesetal2014]; R-Scuti, an audio-visual installation that proposes the conversion of astronomical data from the AAVSO (American Association of Variable Star Observers) database into an exhibition environment, using recordings of variable star observations [@laurentizetal2021]; and an accessible science lab, research that highlights the need for multimodal approaches in teaching and learning environments, presenting principles for inclusive material design based on user-centered design and universal design for teaching environments [@reynagaetal2020].

After an international sonification workshop held in August of 2021, @zanella2022 created a repository of existing software as of December 2021 which contained 98 projects developed since 1962. Unfortunately many of them were no longer actively developed, lacked documentation and had no evidence of science applications. Almost 80% of the sonification projects have been carried out between 2011 and 2021. As of 2017, the date on which this sonification software development began, only 50% of the software included in the mentioned repository had started its development.

In most cases, the sonification mapping of the dataset was defined by its creator and shared as a final product or even with some musicalization, not clearly devoted to research. The ICAD conferences intend to bring together multidisciplinary experts working in the field of sonification, in its repository there are a lot of works that @andreopoulouYgoudarzi2021 grouped into six categories: sonification methods, sonification tools/system, review/opinion, exploratory, perception/evaluation studies and other. This systematic review of the ICAD repository highlights a high percentage of papers devoted to sonification methods and tools, in contrast to a low percentage of papers devoted to design methodologies, perception studies, and evaluation methods. Fortunately, during The Audible Universe 2, a workshop organized by Lorentz Center\footnote{\url{https://www.lorentzcenter.nl/the-audible-universe-2.html}}, the usefulness of evaluation methods and perception studies were pointed out [@AU2023].

In this sense and taking into account the increasing examples of sonification, only some actual developments related to astronomy, astrophysics, and accessibility will be mentioned here. StarSound started its development at the same time as SonoUno; it offers a complete sound synthesizer customizable by the user. By nature, synthesizers in general present a lot of buttons and require setting a lot of variables, but paying attention to the accessibility of visually impaired people, StarSound allows setting them in a text field too. The IDATA project, beyond their numerous activities centered on accessible astronomical software and materials, launched the Afterglow Access Software, which allows users to open and produce sound from image files\footnote{\url{https://idataproject.org/resources/}}.

Some other developments center their efforts on sonification and don’t present a graphic user interface; this is the case of Soni-py\footnote{\url{https://github.com/lockepatton/sonipy}}, Astronify\footnote{\url{https://astronify.readthedocs.io/en/latest/}} and STRAUSS\footnote{\url{https://github.com/james-trayford/strauss}}. Soni-py is a Python package devoted to the sonification of scatter plots; it presents examples and demos in its documentation. Astronify allows the sonification of any time series data, which means any data set where the first column was set as time and the second column as pitch; it is an active open-access development with proper documentation and examples with Light Curve.

On the other hand, STRAUSS is a Python toolkit developed with the aim of improving the current visual display of data and accessibility using sonification. It offers the possibility of being used by people without knowledge of sound design or programming through predefined examples and default settings. However, it provides documentation that allows for more advanced usage, enabling the modification of sound parameters. One direct application of this development is in the "Audio Universe" project, in which they have recently published a tour of the solar system, for which they have used the STRAUSS tool\footnote{For more information, you can access the following link: \url{https://www.audiouniverse.org/}}. @strauss2021 explains how this tour was developed using different instruments for each planet, along with sound configuration to represent the distance and position of each object.

sonoUno is a sonification software to translate time series data into sound.  It is an open-source program with a modular design that allows users to open different datasets and explore them through visual and auditory display, the last permitting them to adjust visual and sound settings to enhance their perception (a full view of the Graphic User Interface (GUI) is shown in \autoref{fig:fig1}). This project is user-centered from the beginning. To reach that goal we follow three main actions. First, the ISO 9241-171:2008 standard was used to analyze the accessibility of three previous software [@ise2a2017; @ijskd2022] and construct the first GUI mock-up. Second, a theoretical framework centered on visual disability was designed and applied to the software in development [@casadoetal2019]; the consequent ISO analysis of SonoUno shows very good results. And finally, a focus group session was conducted with people with and without visual disabilities to test the first version of SonoUno. Some recommendations and updates arise from that study [@casadoFG2022]. The first view of the GUI after all the updates is shown in \autoref{fig:fig2}.

SonoUno is programmed purely in Python. Its modular design, with the use of agile methodology, allows programmers to divide the tasks, organize the job, and make the cooperative work between the team easier. In this case, the modules are Data Input, Data Output, Data Transformation, Sonification, Graphic User Interface Design, and Core. One important feature is the possibility of using each module alone without the need for a graphic user interface (GUI), so some users could import the sound module from bash to produce sonification without installing the graphic user interface library wxPython.

Another important feature is the actual sound library and implementation on SonoUno. It produces sound from its sinusoidal parameters without any additional features, and each data point on the dataset produces a differentiated tone that faithfully represents the numerical data. In addition, the sonification of each point ensures a good correlation between the visual and sound representations and, consequently, a good match between the two human sensory styles. The principal aim os SonoUno is research through sonification; it is very important to understand and correlate sonification with visualization (the actual practice of research in astronomy) in conjunction with a deeper analysis of human sound perception.

![Graphic User Interface with all the panels visible.\label{fig:fig1}](figures/fig7.png)

![The first framework of the GUI, the data deployed is a galaxy spectrum downloaded from the \href{https://skyserver.sdss.org/dr12/en/tools/explore/Summary.aspx?ra=179.689293428354&dec=-0.454379056007667}{SDSS database}.\label{fig:fig2}](figures/fig6.png)

# Statement of need

Most tools that produce data sonification are centered on specific data and devoted to outreach. But sonoUno principal aim’s is research, and moreover, a multimodal approach to knowledge, allowing people with disabilities to explore scientific data and carry out reasearch. sonoUno has three main functionalities: graphic deployment, sonorization of the data, and use of mathematical functions. During our user tests it was observed that the tool allows for (a) deployment of data sets, (b) precise sonification to detects the data features, permitting: marking over the plot, changing intervals, volume, pitch, frequency and adapting the output to the perception of each user and (c) application of math functions. The output of the software (graph, sound, marks, and data plotted) can be saved and reopened for future or more detailed analysis, even using another tool. Finally, the graphic user interface was modified according to the user testing activities following a user-centered design framework from the beginning [@casadoFG2022]. 

According to @wandatesis2013, sonification could enhance the actual data display and the works of Casado et al. reinforce this claim [@casadoetal2019;@casadoFG2022]. In addition, it was tested that astronomical datasets could be displayed in sonoUno in the same form as other visualization tools, with the benefit of sonification and allowing it to be used by people with different learning styles.

# Cases of use

In addition to tests inside the research team, sonoUno has been used by other research groups with their own datasets. Some examples are detailed below.

- The work of Carlos Morales Socorro with variables star, in CEP Las Palmas, Spain, where a training program using sonification was conducted, and a blind student could discover a variable star for the first time in history\footnote{\url{https://astronomiayeducacion.org/taller-2-de-sonificacion-descubriendo-el-universo/}}.

- The ``Sensing the Dynamic Universe'' project, led by a research group at Harvard [@wanda2019], displays a web page with information about variable star and uses sonoUno to generate the videos of data visualizations and sonification\footnote{\url{https://lweb.cfa.harvard.edu/sdu/rrlyrae.html}}. This project created a fork of the sonoUno code to make some updates\footnote{\url{https://github.com/joepalmo/sonoUno}}.

- The GitHub repository “SonoUno-Raspberry-Pi”\footnote{\url{https://github.com/Physicslibrary/SonoUno-Raspberry-Pi}} by Hartwell Fong shows the possibility of using sonoUno in a Raspberry Pi. This user also contacted us asking for the possibility to include some tactile technology in the software, that could be implemented in the near future.

- The Sound of BEARS\footnote{\url{https://stephenserjeant.github.io/sounds-of-bears/}} is a web page that uses sonoUno web version to display a video with the sonification of ALMA data, reinforcing the need to make astronomy more accessible.

# Conclusions

The use of sound to communicate, detect or analyze data features has been used for many years, however, the use of sonification (the use of sound to represent data) formally began in the 90s. Maybe, it is too early to compare it with the visual display in the sense of the possibility to study data only through sonification, especially since we have used visual tools for centuries and learned about visual displays since elementary school. In contrast, the first approach to sound display usually occurs when people already have a degree or as a consequence of a disability. Perception studies and an earlier approximation to this technique are needed.

It is important to mention that our experience shows that the use of more than one sense improves the detection of specific features in the data. In any case and in order to acquire a deep comprehension of multimodal analysis, training courses are needed. Besides, in order to know the sonification process better and investigate how it can be used in the research field, new sound perception experiments need to be done, with available tools like sonoUno and with different datasets.

The authors hope to encourage more people to help with future steps and software maintenance, taking into account that this development is completely open source and the sonification technique is part of the new approach to the study of nature.

# Acknowledgements

The authors want to give their thanks to the people who tested the tool, participated in the training activities, and shared their experiences, ideas, suggestions, and comments. The contributions and feedback of Julieta Carricondo Robino, Aldana Palma, Carlos Morales Socorro, Richard Green, Poshak Gandhi, Gaston Jaren, Southampton Sight, students at the University of Mendoza and ITeDA, and many volunteers at the Focus Groups and beyond testing the software are deeply appreciated. In addition, thanks to IAU Office of Astronomy for Development-SAAO-South Africa and the University of Southampton for all their support to this development.

This work was funded by the National Council of Scientific Research of Argentina (CONICET) and has been performed partially under the Project REINFORCE (GA 872859) with the support of the EC Research Innovation Action under the H2020 Programme SwafS-2019-1.

# References
