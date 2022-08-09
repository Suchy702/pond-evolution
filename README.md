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

Upon start of the program user is greeted with the following window:

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/readme/settings.png" alt="settings"/>
</p>

Here one can tweak parameters of the simulation. The current options include:

- **Resolution** - defines resolution of the simulation and window size (unless fullscreen mode is selected)
- **Full screen mode** - defines whether or not program should be run in fullscreen mode. Program will be rendered in previously selected resolution and then scaled to fit user's screen
- **Show statistics** - after simulation ends various graphs can be shown to represent how the number of fish and their traits varied with respect to time
- **Empty pond** - by default simulation starts with randomly spawned fish and plants. This settings turns it off
- **No worms from heaven** - by default worms fall from top to ocean ground. This settings removes worms completely.

When "Run simulations" is clicked new window is opened. This is where the simulation happens.

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/readme/main.png" alt="demo" width="720px"/>
</p>

Bottom of the screen contains User Panel which displays basic controls. Bottom right corner contains information about current cycle of evolution. 

### Controls
1. movement - **arrows** move camera, **+/-** zooms in and out, **\<key c\>** centers camera 

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/readme/movement.gif" alt="demo" width="500px"/>
</p>

2. object addition - **\<left click\>** can be used to place new objects into the simulation. Type of placed object can be changed with **\<key q\>**

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/readme/add.gif" alt="demo" width="500px"/>
</p>

3. jump 100 evolution cycles - **\<key j\>** skips 100 cycles of evolution. It may take a few seconds...

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/readme/jump.gif" alt="demo" width="500px"/>
</p>

4. speed - **\<key ,\>** slows down simulation and **\<key .\>** speeds it up

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/readme/speed.gif" alt="demo" width="500px"/>
</p>

### Evolution

There are four types of of objects with fish being the only inteligent species:

1. **Alga Maker**

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/img/seaweed.svg" alt="demo" width="50px"/>
</p>

    This plant is forever stuck to the bottom of the ocean. Occasionally spawns algae.

2. **Alga**

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/img/alga.svg" alt="demo" width="50px"/>
</p>

    Produced from Alga Makers. Slowly floats to the top in straight line. Can be eaten by herbivores.

3. **Worm**

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/img/worm.svg" alt="demo" width="50px"/>
</p>

    Randomly dropped from heavens. Slowly floats to the bottom in zigzag manner. Can be eaten by carnivores.

3. **Fish**

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/img/omnivore_fish.svg" alt="demo" width="50px"/>
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/img/herbivore_fish.svg" alt="demo" width="50px"/>
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/img/carnivore_fish.svg" alt="demo" width="50px"/>
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/img/predator_fish.svg" alt="demo" width="50px"/>
</p>

    Intelligent species that evolves with each new generation. Fish have traits defining their size, speed and eyesight. One fish can eat another if it is bigget than it.
    
    - size - the bigger the fish the harder it is for other fish to eat it, but requires more food to live and reproduce
    - speed - the higher the speed the further fish can move in one go, but requires more food to live and reproduce
    - eyesight - the higher the eyesight the 


## Development

Project is being developed using Pycharm IDE and python 3.10 To create development environment for Pycharm do the following steps:
1. clone this github repo
2. run command  ```./config/configure_env.sh``` from **pond-evolution** directory which will create local virtual environment for python and store it in **venv** subdirectory
3. run command  ```source ./venv/bin/activate``` from **pond-evolution** to activate virtual environment
4. open this project in Pycharm, go to "Add python interpreter" and then in section "Exisitng environment" set path so that it points to **venv** directory
5. install mypy plugin for Pycharm

Project comes with two Run/Debug Configurations. One called Run which starts the application and other called Test which tests whole project using pytest. It is adviced to check code with mypy and pytest before every commit. This can be easily done in Pycharm by checking boxes "Scan with Mypy" and "Run tests" in "Before commit" section in "Commit" window.
