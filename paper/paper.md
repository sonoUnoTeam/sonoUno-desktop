---
title: 'SonoUno development: a User Centred Sonification software for data analysis'
tags:
  - sonification
  - inclusion
  - astrophysics
  - open source
  - user centred design
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

In general, people think about information and nature based on a visual approach, but if we go back to our childhood and try to understand the world through our different senses, a new way of understanding the information arises. Even when it’s challenging to think of a method to understand astrophysics through other sensorial inputs, sonification is a technique that uses non-speech audio to translate data into sound. The sonification field has grown continuously over the recent years, especially since 1992 with the International Community for Auditory Display-ICAD conferences. In this contribution, a sonification software, sonoUno, and its application in astronomy are presented, without neglecting the analysis possibilities for data from various disciplines. The differences between the present development from others are: it is user centred from the beginning, with several contacts with end users along the design and a focus group test; it seeks a way to bring autonomy to its functional diverse users; and it presents a simple first framework, with the mathematical operations and settings in the menu. A description of the software and some cases of use are presented.

# Introduction

The use of sonification in astronomy has existed for years, some recent examples are a sonification of the zCOSMOS astronomical dataset, where the authors describe the dataset and the sonification strategy used [@bardellietal2021]; the LightSound, an electronic device that allows the conversion of light into sound and it is used to observe eclipses [@lightsound2020]; See-Through-Sound, a project dedicated to converting images into sound to allow visually impaired people to detect objects around them [@henriquesetal2014]; R-Scuti, an audio-visual installation that proposes the conversion of astronomical data from the AAVSO (American Association of Variable Star Observers) database into an exhibition environment, using recordings of variable star observations [@laurentizetal2021]; and an accessible science lab, research that highlights the need for multimodal approaches in teaching and learning environments, presenting principles for inclusive material design based on user-centred design and universal design for teaching environments [@reynagaetal2020].

Furthermore, @zanella2022, after an international sound workshop held in August 2021, created a repository with existing software until December 2021, which yields a result of 98 projects developed since 1962, many of them discontinued, with a lack of documentation or without evidence of applications in science. Almost 80% of the sonification projects have been carried out between 2011 and 2021. Until 2017, the date on which this sonification software development began, only 50% of the software included in the mentioned repository had started its development.

Nevertheless, in most cases, the sonification mapping of the dataset was defined by its creator and shared as a final product or even with some musicalization, not clearly devoted to research. The ICAD conference intended to bring together multidisciplinary experts working in this field of sonification, since its creation in 1992, in its repository there are a lot of works that @andreopoulouYgoudarzi2021 grouped into six categories (sonification methods, sonification tools/system, review/opinion, exploratory, perception/evaluation studies and other). This systematic review of the ICAD repository highlights a high percentage of papers devoted to sonification methods and tools, in contrast to a low percentage of papers devoted to design methodologies, perception studies, and evaluation methods. In contrast, during The Audible Universe 2, a workshop organized by Lorentz Center\footnote{\url{https://www.lorentzcenter.nl/the-audible-universe-2.html}}, the usefulness of evaluation methods and perception studies were pointed out.

In this sense and taking into account the increasing examples of sonification in astrophysics, sonoUno is a sonification software to translate data from two or more column tables into sound.  It is an open-source program with a modular design, that allows users to open different datasets, and explore them through visual and auditory display, the last permitting them to adjust visual and sound settings to enhance their perception (a full view of the Graphic User Interface (GUI) is shown in \autoref{fig:fig1}). This project is user centred from the beginning, to reach that goal at first the ISO 9241-171:2008 standard was used to analyze the accessibility of three previous software [@ise2a2017; @ijskd2022] and construct the first GUI mock-up; second, a theoretical framework centred on visual disability was designed and applied to the software in development [@casadoetal2019], the consequent ISO analysis to sonoUno show very good results. Finally, a focus group session was conducted with people with and without visual disabilities to test the first version of sonoUno, some recommendations and updates arise from that study [@casadoFG2022] (the first view of the GUI after all the updates was shown in \autoref{fig:fig2}).

SonoUno was programmed purely in Python, its modular design with the use of agile methodology, allows programmers to divide the tasks, organize the job and make the cooperative work between the team easier. In this case, the modules are Data Input, Data Output, Data Transformation, Sonification, Graphic User Interface design, and Core. One important remark is the possibility of using each module alone without the need of the graphic user interface (GUI), so some users could import the sound module from bash to produce sonification without installing the whole program.

Another important point was the actual sound library and implementation on sonoUno, it produces sound from its sinusoidal parameters without any additional feature, each data point on the dataset produces a differentiated tone that faithfully represents the numerical data. In addition, the sonification of each point ensures a good correlation between the visual and sound representation, in consequence, a good match between the two human sensory styles. SonoUno software's principal aim is research through sonification, it is very important to understand and correlate sonification with visualization (the actual practice to research in astronomy) in conjunction with a deeper analysis of human sound perception.

![Graphic User Interface with all the panels visible.\label{fig:fig1}](figures/fig7.png)

![The first framework of the GUI, the data deployed is a galaxy spectrum downloaded from the SDSS database\footnote{\url{https://skyserver.sdss.org/dr12/en/tools/explore/Summary.aspx?ra=179.689293428354&dec=-0.454379056007667}.\label{fig:fig2}](figures/fig6.png)

# Statement of need

Most tools that produce data sonification are centered on specific data and devoted to outreach. But sonoUno principal aim’s is research, and moreover, a multimodal approach to knowledge, allowing people with disabilities to explore scientific data and make science. As a first result after the use of sonoUno in its triple functioning: graphic deployment, sonorization of the data, and use of mathematical function, was observed that the tool is sufficient for the purpose of inclusion in general: a) it is possible to deploy data sets in the same way that recommend the data owners; b) the sonification is precise and detects the data features, permitting: marking over the plot, changing intervals, volume, pitch, frequency and adapting the output to the perception of each user; c) it is possible to apply mathematical functions to the data. The output of the software: graph, sound, marks, and data plotted; can be saved and reopened for future or more detailed analysis, even using another tool. Furthermore, the graphic user interface was modified according to the user testing activities following a user centred design framework from the beginning [@casadoFG2022]. 

According to @wandatesis2013, sonification could enhance the actual data display, and, @iau367;@casadoFG2022’s work reinforces that assumption. In addition, it was tested that astronomical datasets could be displayed in sonoUno in the same form as other visualization tools, with the benefit of sonification and allowing it to be used by people with different learning styles.

# Cases of use

In addition to tests inside the research team, sonoUno has been used by other research groups with their own datasets. Some examples are:

\begin{itemize}
  \item the work of Carlos Morales Socorro with variables star, in CEP Las Palmas, Spain, where a training program using sonification was conducted, and a blind student could discover a variable star for the first time in history\footnote{\url{https://astronomiayeducacion.org/taller-2-de-sonificacion-descubriendo-el-universo/?cn-reloaded=1&cn-reloaded=1}};
  \item the ``Sensing the Dynamic Universe'' project, led by a research group at Harvard [@wandaetal2019], display a web page with information about variables star and use sonoUno to generate the videos of data visualizations and sonification\footnote{\url{https://lweb.cfa.harvard.edu/sdu/rrlyrae.html}}, even in this project a Fork of the sonoUno code was created to make some updates\footnote{\url{https://github.com/joepalmo/sonoUno}};
  \item the GitHub repository “SonoUno-Raspberry-Pi”\footnote{\url{https://github.com/Physicslibrary/SonoUno-Raspberry-Pi}} of Hartwell Fong, where it is shown the possibility of using sonoUno in a Raspberry Pi, also this user write to us asking for the possibility to include some tactile technology in the software, that could be implemented in a short future;
  \item ``The Sound of BEARS''\footnote{\url{https://stephenserjeant.github.io/sounds-of-bears/}} is a web page that uses sonoUno web version to display a video with the sonification of ALMA data, reinforcing the need to make astronomy more accessible.
\end{itemize}

# Conclusions

The use of sound to communicate, detect or analyze data features has been used for many years, however, the use of sonification (the use of sound to represent data) formally began in the 90s. Maybe, it is too early to compare it with the visual display in the sense of the possibility to study data only through sonification, especially since we have used visual tools for centuries and learned about visual display since elementary school. In contrast, the first approach to sound display usually occurs when people already have a degree or as a consequence of a disability. Perception studies and an earlier approximation to this technique are needed.

It is important to mention that our experience shows that the use of more than one sense improves the detection of specific features in the data. In any case and in order to acquire a deep comprehension of multimodal analysis, training courses are needed. Besides, in order to know the sonification process better and investigate how it can be used in the research field, new sound perception experiments need to be done, with available tools like sonoUno and with different datasets.

The authors expect to encourage more people to help with future steps and software maintenance, taking into account that this development is completely open source and the sonification technique is part of the new approach to the study of nature.

# Acknowledgements

The authors want to give their thanks to the people who tested the tool, participated in the training activities, and shared their experiences, ideas, suggestions, and comments. The contributions and feedback of Julieta Carricondo Robino, Aldana Palma, Carlos Morales Socorro, Richard Green, Poshak Gandhi, Gaston Jaren, Southampton Sight, students at the University of Mendoza and ITeDA, and many volunteers at the Focus Groups and beyond testing the software are deeply appreciated. In addition, thanks to IAU Office of Astronomy for Development-SAAO-South Africa and the University of Southampton for all their support to this development.

This work was funded by the National Council of Scientific Research of Argentina (CONICET) and has been performed partially under the Project REINFORCE (GA 872859) with the support of the EC Research Innovation Action under the H2020 Programme SwafS-2019-1.

# References
