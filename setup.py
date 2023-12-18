from setuptools import find_packages,setup
#from typing import List

HYFEN_E_DOT='-e .'
def get_requirments(file_path):
    '''
    this function will return list of requirments.
    '''
    requirments=[]
    with open(file_path) as file_obj:
        requirments=file_obj.readlines()
    requirments=[requirment.replace("\n","") for requirment in requirments]
    if HYFEN_E_DOT in requirments:
        requirments.remove(HYFEN_E_DOT)
    return requirments



setup(
    name='mlproject',
    version='0.0.1',
    author='Aakash',
    author_email='aakashpokkanayil@gmail.com',
    packages=find_packages(), # find_packages is a special function which can find all modules under your source(src) directory
    install_requires=get_requirments('requirements.txt') # this will return all packages names mentioned in requirements.txt to install_requires parameter by a custom fn get_requirments.
)

