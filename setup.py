from setuptools import find_packages, setup

setup(
    name='wokengineers-django',
    packages=find_packages(),
    description='This is a Django helper library by wokengineers',
    license='MIT',
    version='0.0.5',
    url='https://github.com/wokengineers/wokengineers-django.git',
    author='wokengineers',
    install_requires=[ 
        "PyJWT==2.6.0"
    ],
    keywords=['pip','wokengineers','library',"django","loggers","middleware"]
    )
