from setuptools import find_packages, setup

# Making the setup configuration
setup(
    name='src',
    packages=find_packages(),
    version='0.1.0',
    description='Model for Predicting Car price in the United State',
    author='Psalishol Samuel',
    license='MIT',
    packages=find_packages(),
    author_email= "psalishol80@gmail.com",
    long_description=open('README.md').read(),
    install_requires=[
       "Python >= 1.1.1",
       "Scikit-learn",
       "Scrapy",
       "Pandas",
       "Numpy",
       "fastapi",
       "uvicorn",
       "tensorflow >= 2.3.1"   
       
       
   ],
)



