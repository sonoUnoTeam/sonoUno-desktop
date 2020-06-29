from setuptools import setup, find_packages
import platform

system_type = platform.uname()[0]
if system_type == 'Linux':
    dist_name = platform.dist()[0].lower()
    dist_ver = platform.dist()[1].split('.')[0]  

    minor=int(platform.python_version()[2])

    if minor < 7:
        cp = str(30+minor)
    else:
        cp = '37'

    if dist_name == 'ubuntu':
        if dist_ver == '14':
            dist =  'ubuntu-14.04'
        if dist_ver == '16':
            dist = 'ubuntu-16.04'
        if dist_ver == '18' or dist_ver == '19':
           dist = 'ubuntu-18.04' 
    else:
        dist = '-'.join([dist_name, dist_ver])

    wxpython_url = 'wxPython @ https://extras.wxpython.org/wxPython4/extras/linux/gtk3/'+dist+'/wxPython-4.0.7.post2-cp'+cp+'-cp'+cp+'m-linux_x86_64.whl'

else:
    wxpython_url = 'wxpython'

#Available wxPython repos:
#centos-7
#debian-8
#debian-9
#fedora-23
#fedora-24
#fedora-26
#fedora-27
#fedora-28

setup(name='sonoUno',
      version='3.1.0',
      description='Data sonorization tool',
      url='http://github.com/sonounoteam/sonouno',
      author='Johanna Casado',
      author_email='johi.ceh@gmail.com',
      license='MIT',
      package_dir={"": "sonoUno"},
      packages= find_packages('sonoUno', exclude=['sample_data']),
      scripts=['sonoUno/sonoUno'],
      python_requires='>3.5.0',
      install_requires=[
        'cycler',
        'kiwisolver',
        'matplotlib',
        'numpy',
        'pandas',
        'Pillow',
        'pygame',
        'pyparsing',
        'python-dateutil',
        'pytz',
        'six',
        'oct2py',
        wxpython_url,
      ],
      zip_safe=True)
