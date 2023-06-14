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

The sonification field has grown continuously over the recent years, especially since 1992 with the International Community for Auditory Display-ICAD conferences. Sonification is by definition the use of non-speech audio to translate data into sound, in this case, a sonification software, sonoUno, and its application in astronomy are presented, without neglecting the analysis possibilities for data from various disciplines. The differences between the present development from others are: it is user centred from the beginning, with several contacts with end users along the design and a focus group test; it seeks a way to bring autonomy to its functional diverse users; and it presents a simple first framework, with the mathematical operations and settings in the menu. A description of the software, the impact on the design after end users' contacts, its functionalities, and some specific applications using different sets of astrophysical datasets are presented.

In general, people think about information and nature based on a visual approach, but what if we go back to our childhood and try to understand the world through our different senses? In this contribution a new way to face astrophysical data is presented, emphasizing the possibility of multisensorial scientific work.

# Introduction

The human being by nature explores the world through all his senses, however, there is a marked predominance in the use of visual displays to make sense of data sets under study. This is the case in astronomy,  even with evidence of the benefits of the auditory display as a complement to visual display \cite{wandatesis2013}.

The use of sonification in astronomy has existed for years, some recent examples are a sonification of the zCOSMOS astronomical dataset, where the authors describe the dataset and the sonification strategy used \cite{bardellietal2021}; the LightSound, an electronic device that allows the conversion of light into sound and it is used to observe eclipses \cite{lightsound2020}; See-Through-Sound, a project dedicated to converting images into sound to allow visually impaired people to detect objects around them \cite{henriquesetal2014}; R-Scuti, an audio-visual installation that proposes the conversion of astronomical data from the AAVSO (American Association of Variable Star Observers) database into an exhibition environment, using recordings of variable star observations \cite{laurentizetal2021}; and an accessible science lab, research that highlights the need for multimodal approaches in teaching and learning environments, presenting principles for inclusive material design based on user-centred design and universal design for teaching environments \cite{reynagaetal2020}.

Nevertheless, in most cases, the sonification mapping of the dataset was defined by its creator and shared as a final product, not clearly devoted to research. The ICAD conference intended to bring together multidisciplinary experts working in this field of sonification, since its creation in 1992, in its repository there are a lot of works that \citet{andreopoulouYgoudarzi2021} grouped into six categories (sonification methods, sonification tools/system, review/opinion, exploratory, perception/evaluation studies and other). This systematic review of the ICAD repository highlights a high percentage of papers devoted to sonification methods and tools, in contrast to a low percentage of papers devoted to design methodologies, perception studies, and evaluation methods. It is alarming that the perception studies present a growth between 2005-2009, but decreased by under 1% to 2019; even when \citet{fergusonYbrewster2017} point out the importance of perception studies in auditory displays and report some psychoacoustic parameters and talk about how people perceive it. 

In this sense and taking into account the increasing examples of sonification in astrophysics, sonoUno aims to provide an open-source platform that allows users to open different datasets, and explore them through visual and auditory display, the last permitting to adjust visual and sound settings to enhance their perception. This project is user centred from the beginning, to reach that goal at first the ISO 9241-171:2008 standard was used to analyse the accessibility of three previous software \cite{ise2a2017,ijskd2022} and construct the first Graphic User Interface (GUI) mock-up; second, a theoretical framework centred on visual disability was designed and applied to the software in development \cite{casadoetal2019}, the consequent ISO analysis to sonoUno show very good results. Finally, a focus group session was conducted with people with and without visual disabilities to test the first version of sonoUno, some recommendations and updates arise from that study \cite{casadoFG2022}. In this contribution, the final version and architecture of sonoUno were explained and the new functionalities are tested with astronomical data sets.

# Previous works



# Statement of need

`Gala` is an Astropy-affiliated Python package for galactic dynamics. Python
enables wrapping low-level languages (e.g., C) for speed without losing
flexibility or ease-of-use in the user-interface. The API for `Gala` was
designed to provide a class-based and user-friendly interface to fast (C or
Cython-optimized) implementations of common operations such as gravitational
potential and force evaluation, orbit integration, dynamical transformations,
and chaos indicators for nonlinear dynamics. `Gala` also relies heavily on and
interfaces well with the implementations of physical units and astronomical
coordinate systems in the `Astropy` package [@astropy] (`astropy.units` and
`astropy.coordinates`).

`Gala` was designed to be used by both astronomical researchers and by
students in courses on gravitational dynamics or astronomy. It has already been
used in a number of scientific publications [@Pearson:2017] and has also been
used in graduate courses on Galactic dynamics to, e.g., provide interactive
visualizations of textbook material [@Binney:2008]. The combination of speed,
design, and support for Astropy functionality in `Gala` will enable exciting
scientific explorations of forthcoming data releases from the *Gaia* mission
[@gaia] by students and experts alike.

# Mathematics

Single dollars ($) are required for inline mathematics e.g. $f(x) = e^{\pi/x}$

Double dollars make self-standing equations:

$$\Theta(x) = \left\{\begin{array}{l}
0\textrm{ if } x < 0\cr
1\textrm{ else}
\end{array}\right.$$

You can also use plain \LaTeX for equations
\begin{equation}\label{eq:fourier}
\hat f(\omega) = \int_{-\infty}^{\infty} f(x) e^{i\omega x} dx
\end{equation}
and refer to \autoref{eq:fourier} from text.

# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

Figures can be included like this:
#![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
#![Caption for example figure.](figure.png){ width=20% }

# Acknowledgements

We acknowledge contributions from Brigitta Sipocz, Syrtis Major, and Semyeong
Oh, and support from Kathryn Johnston during the genesis of this project.

# References
