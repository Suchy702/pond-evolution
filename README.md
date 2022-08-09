# Pond Evolution
![license](https://img.shields.io/github/license/Suchy702/pond-evolution.svg)
![status](https://img.shields.io/badge/status-development-yellow)
![python](https://img.shields.io/badge/python-3.10-blue)
![issues](https://img.shields.io/github/issues-raw/Suchy702/pond-evolution)
![build](https://img.shields.io/github/workflow/status/Suchy702/pond-evolution/test_pond_evolution/master)

A simple yet estetic program that simulates wild life deep beneath the ocean floor. Inspired by [Primer's](https://www.youtube.com/c/PrimerLearning) simulation and reinforced learning visualisations, but with more emphasis on interaction with user. The idea is simple: user defines parameters of the simulation, adds creatures and objects using simple GUI, and observes how the life, he created, evolves.

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/demo/demo3.gif" alt="demo" width="720px"/>
</p>

## Installation

Make sure you have Python 3.10 or newer. Run the following command from **pond-evolution** directory:

```pip install -r ./config/requirements.txt```

## Running

To start the program executre **main.py** file. E.g you can run this command from **pond-evolution** directory:

```python main.py```

## Usage

## Development

Project is being developed using Pycharm IDE and python 3.10 To create development environment for Pycharm do the following steps:
1. clone this github repo
2. run command  ```./config/configure_env.sh``` from **pond-evolution** directory which will create local virtual environment for python and store it in **venv** subdirectory
3. run command  ```source ./venv/bin/activate``` from **pond-evolution** to activate virtual environment
4. open this project in Pycharm, go to "Add python interpreter" and then in section "Exisitng environment" set path so that it points to **venv** directory
5. install mypy plugin for Pycharm

Project comes with two Run/Debug Configurations. One called Run which starts the application and other called Test which tests whole project using pytest. It is adviced to check code with mypy and pytest before every commit. This can be easily done in Pycharm by checking boxes "Scan with Mypy" and "Run tests" in "Before commit" section in "Commit" window.
