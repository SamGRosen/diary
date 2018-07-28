from distutils.core import setup
import os.path
here = os.path.abspath(os.path.dirname(__file__))

try:
      with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
            long_description = f.read()
except:
      long_description = ""

setup(name='diary',
      packages=['diary'],
      scripts=['diary/bin/diary'],
      version='0.1.5',
      description='Async Logging',
      long_description=long_description,
      author='Sam Rosen',
      author_email='samrosen90@gmail.com',
      url='https://github.com/SamGRosen/diary',
      license='MIT',
      classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.1',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
      ],
      keywords='logging async asynchronous parallel threading',
     )
