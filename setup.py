from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='microglia_sim',
    version='0.1.0',
    description='Agent-based microglial chemotaxis simulation with purinergic signaling',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Vlada Misici',
    url='https://github.com/vladamisici/microglia_sim',
    packages=find_packages(),
     install_requires=[
         'numpy>=1.19',
         'scipy',
         'numpy>=1.19',
         'scipy>=1.8',
         'numba',
         'matplotlib',
         'pyyaml'
     ],
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)