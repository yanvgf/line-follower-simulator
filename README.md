# WiSARD-line-follower
Design and simulation of a line follower robot based on WiSARD weightless neural networks.

## Requirements

First, install the required packages. The **requirements.txt** file contains all the packages and versions needed to run this project.

If you use conda, you can create a new environment with the following command (in Linux or WSL):

```bash
$ conda create --name wisard-line-follower --file requirements.txt
```

Or you can install the packages with pip:

```bash
$ pip install -r requirements.txt
```

## Usage

To run the simulation, execute the following command:

```bash
$ python main.py
```

Before the simulation starts, you will be asked to position the robot in the map. It is as simple as clicking on the map where you want to place the robot and scrolling to rotate it. When you are done, press any key and the simulation will start.

The simulation will run until the robot reaches the goal or until you close the window.

### Changing the robot and map images

You can change the robot and map images by replacing the files **robot.png** and **map.png** in the **images** folder. **Please make sure your robot is positioned with angle zero in the image (i.e. is pointing to the right).**

The robot will follow any black (or dark) line on the map.

### Changing the simulation parameters

You can change the simulation parameters simply by changing the values in the beginning of the **scripts/main.py** file. Some of the parameters are:

- chassis' width
- motors' maximum speed
- wheel's radius
- sensors' positions

## References

Some of the code used in this project was based on the following videos:

- [Algobotics: Simulating an Obstacle Avoidance Robot Using Python | From Scratch](https://www.youtube.com/watch?v=pmmUi6DasoM)
- [robojunkies: How to code your Line follower robot with PID control and working code!](https://www.youtube.com/watch?v=8Lj5ycrT9Fw)
- [Tech with Tim: How to Make a Game in Python](https://www.youtube.com/watch?v=waY3LfJhQLY)