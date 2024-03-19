from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='harqis_core',
    version="0.1.0",
    packages=find_packages(),
    author="Brian Bartilet",
    author_email="brian.bartilet@gmail.com",
    install_requires=requirements,
    description="Heuristic Automation for a Reliable Quality Integration System",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/brianbartilet/harqis-core",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    homepage="https://github.com/brianbartilet/harqis-core",
)
