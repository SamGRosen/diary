from distutils.core import setup

with open('README.rst', encoding='utf-8') as f:
      long_description = f.read()

setup(name='diary',
      version='1.0.0',
      description='Async Logging',
      long_description=long_description,
      author='Sam Rosen',
      author_email='samrosen90@gmail.com',
      url='https://github.com/GreenVars/diary',
      license='MIT',
      classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Logging Tools',
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
