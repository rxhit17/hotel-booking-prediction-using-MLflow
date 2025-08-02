from setuptools import setup,find_packages 

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name='MLops-project-1',
    version="0.1",
    author="Rohit",
    packages=find_packages(),
    install_requires = requirements,
)