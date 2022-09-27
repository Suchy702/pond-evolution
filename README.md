    ██████╗  ██████╗ ███╗   ██╗██████╗ 
    ██╔══██╗██╔═══██╗████╗  ██║██╔══██╗
    ██████╔╝██║   ██║██╔██╗ ██║██║  ██║
    ██╔═══╝ ██║   ██║██║╚██╗██║██║  ██║
    ██║     ╚██████╔╝██║ ╚████║██████╔╝
    ╚═╝      ╚═════╝ ╚═╝  ╚═══╝╚═════╝ 
    ███████╗██╗   ██╗ ██████╗ ██╗     ██╗   ██╗████████╗██╗ ██████╗ ███╗   ██╗
    ██╔════╝██║   ██║██╔═══██╗██║     ██║   ██║╚══██╔══╝██║██╔═══██╗████╗  ██║
    █████╗  ██║   ██║██║   ██║██║     ██║   ██║   ██║   ██║██║   ██║██╔██╗ ██║
    ██╔══╝  ╚██╗ ██╔╝██║   ██║██║     ██║   ██║   ██║   ██║██║   ██║██║╚██╗██║
    ███████╗ ╚████╔╝ ╚██████╔╝███████╗╚██████╔╝   ██║   ██║╚██████╔╝██║ ╚████║
    ╚══════╝  ╚═══╝   ╚═════╝ ╚══════╝ ╚═════╝    ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                                          

![license](https://img.shields.io/github/license/Suchy702/pond-evolution?colorA=192330&colorB=c70039&style=for-the-badge)
![status](https://img.shields.io/badge/status-finished-green?colorA=192330&colorB=00e600&style=for-the-badge)
![python](https://img.shields.io/badge/python-3.10-blue?colorA=192330&colorB=309cdd&style=for-the-badge)
![issues](https://img.shields.io/github/issues-raw/Suchy702/pond-evolution?colorA=192330&style=for-the-badge)
![build](https://img.shields.io/github/workflow/status/Suchy702/pond-evolution/test_pond_evolution/master?colorA=192330&style=for-the-badge)

A simple yet estetic program that simulates wild life deep beneath the ocean floor. Inspired by [Primer's](https://www.youtube.com/c/PrimerLearning) simulation and reinforced learning visualisations, but with more emphasis on interaction with user. The idea is simple: user defines parameters of the simulation, adds creatures and objects using simple GUI, and observes how the life, he created, evolves.

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/demo/demo3.gif" alt="demo" width="720px"/>
</p>

## Running

Make sure you have python3.10 or newer installed.
To start the program execute **run_for_linux.sh** or **run_for_windows.bat** depending on which OS is being used. Alternatively run the following command from **pond-evolution** directory:
```
python main.py
```

## Usage

Upon start of the program user is greeted with the following window:

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/readme/settings.png" alt="settings"/>
</p>

Here one can tweak parameters of the simulation. The current options include:

- **Resolution** - defines resolution of the simulation and window size (unless fullscreen mode is selected).
- **Full screen mode** - defines whether or not program should be run in fullscreen mode. Program will be rendered in previously selected resolution and then scaled to fit user's screen.
- **Pond size** - size of pond in which simulation takes place. Default value depends on selected resolution and guarantees that whole pond is visible without any need to move camera.
- **Show statistics** - after simulation ends various graphs can be shown to represent how the number of fish and their traits varied with respect to time.
- **Empty pond** - by default simulation starts with randomly spawned fish and plants. This settings turns it off.
- **No worms from heaven** - by default worms fall from top to ocean ground. This settings removes worms completely.
- **No alga from hell** - by default alga makers will keep spawning algae. This settings removes algae completely.
- **Trait penalty** - changes degree to which negative effects of size/speed/eyesight influences fish (see "Traits" section). 0 turns it off completely. Values higher that 200 are not advised.
- **Energy value** - defines how much energy fish gets when it eats alga or worm.

When "Run simulations" is clicked new window is opened. This is where the simulation happens.

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/readme/main.png" alt="main" width="720px"/>
</p>

Bottom of the screen contains User Panel which displays basic controls. Bottom right corner contains information about current cycle of evolution. 

### Controls
1. movement - **arrows** move camera, **+/-** zooms in and out, **\<key c\>** centers camera 

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/readme/movement.gif" alt="move" width="500px"/>
</p>

2. object addition - **\<left click\>** can be used to place new objects into the simulation. Type of placed object can be changed with **\<key q\>**

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/readme/add.gif" alt="add" width="500px"/>
</p>

3. jump 100 evolution cycles - **\<key j\>** skips 100 cycles of evolution. It may take a few seconds...

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/readme/jump.gif" alt="jump" width="500px"/>
</p>

4. speed - **\<key ,\>** slows down simulation and **\<key .\>** speeds it up

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/readme/speed.gif" alt="speed" width="500px"/>
</p>

### Evolution

There are four types of of objects with fish being the only inteligent species:

1. **Alga Maker**

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/img/seaweed.svg" alt="seaweed" width="50px"/>
</p>

    This plant is forever stuck to the bottom of the ocean.
    Occasionally spawns algae.

2. **Alga**

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/img/alga.svg" alt="alga" width="50px"/>
</p>

    Produced from Alga Makers. Slowly floats to the top in straight line.
    Can be eaten by herbivores.

3. **Worm**

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/img/worm.svg" alt="worm" width="50px"/>
</p>

    Randomly dropped from heavens. Slowly floats to the bottom in zigzag manner.
    Can be eaten by carnivores.

3. **Fish**

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/img/omnivore_fish.svg" alt="f1" width="50px"/>
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/img/herbivore_fish.svg" alt="f2" width="50px"/>
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/img/carnivore_fish.svg" alt="f3" width="50px"/>
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/img/predator_fish.svg" alt="f4" width="50px"/>
</p>

    Intelligent species that evolves with each new generation.
    Fish have traits defining their size, speed and eyesight.
    Predator fish can eat another if it is bigger than the other one.
    Each fish has limited eyesight. It sees only things inside circle
    of given radius (manhattan metric circle).
    Fish will try to move to the location of nearest food, but only if
    the spot with food is not occupied by too many fish
    (they are introverted and prefer to keep themselves to themselves).
    If fish notices a predator, then it tries to run away.
    If fish ate enough food it will reproduce and then die.
    Newborn fish have traits of their parents with small random changes.
    
    Traits:
    
    - size - the bigger the fish the harder it is for other fish to eat it,
      but requires more food to live and reproduce
    - speed - the higher the speed the further fish can move in one go,
      but requires more food to live and reproduce
    - eyesight - the higher the eyesight the bigger the radius in which
      fish sees things
      
    Types of fish:
     
    - 🟡 omnivore - eats alae and worms
    - 🟢 herbivore - eats only algae
    - 🟣 carnivore - eats only worms
    - 🔴 predator - eats only other fish
    
### Statistics

If approproate settings is checked, at the end of simulation two graphs will be shown. First one represents change in population of fish by their type:

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/readme/population.png" alt="population" width="700px"/>
</p>

The other one shows how fish's traits changed with respect to time, type of fish and trait:

<p align="center">
  <img src="https://github.com/Suchy702/pond-evolution/blob/master/resources/readme/traits.png" alt="traits" width="700px"/>
</p>
    
## Development

Project is being developed using Pycharm IDE and python 3.10 To create development environment for Pycharm do the following steps:
1. clone this github repo
2. run command  ```./configure_env.sh``` from **pond-evolution** directory which will create local virtual environment for python and store it in **venv** subdirectory
3. run command  ```source ./venv/bin/activate``` from **pond-evolution** to activate virtual environment
4. open this project in Pycharm, go to "Add python interpreter" and then in section "Exisitng environment" set path so that it points to **venv** directory
5. install mypy plugin for Pycharm

Project comes with two Run/Debug Configurations. One called Run which starts the application and other called Test which tests whole project using pytest. It is adviced to check code with mypy and pytest before every commit. This can be easily done in Pycharm by checking boxes "Scan with Mypy" and "Run tests" in "Before commit" section in "Commit" window.
