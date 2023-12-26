# line-follower-simulator
This project aims to design a straightforward simulator for a line follower robot using Python.

![main_v2](https://github.com/yanvgf/line-follower-simulator/assets/93750334/a14c2e0a-82ea-421b-ac81-ecccedde902f)

The robot is capable of navigating along user-designed tracks utilized as maps, given that the line is distinguishable from the rest of the map, commonly by being darker. The robot's movements are governed by the user-defined control logic and sensor positioning. In the video above, the robot employs a PID control strategy to accurately trace the specified line.

**Note**: This project is currently under development, and several features are yet to be implemented.

## Requirements
To begin, install the necessary packages. The **requirements.txt** file contains all the required packages and their versions for running this project.

For those using conda, create a new environment using the following command (Linux or WSL):

```bash
$ conda create --name line-follower-simulator --file requirements.txt
```

Alternatively, you can install the packages via pip:

```bash
$ pip install -r requirements.txt
```

## Usage

The main interaction occurs through two files: setup.py and main.py.

### setup.py

In this file, users configure robot parameters (chassis width, wheel radius, initial speed, number of sensors, etc.) and position it within the arena. However, **a default setup is already available for users to skip this stage if they wish**. Parameters need to be specified within the code, as displayed in the image below:

![parameters](https://github.com/yanvgf/line-follower-simulator/assets/93750334/52166420-4667-4d0d-96c8-1950de09ee16)

Once the parameters are set, execute the setup.py file using the following command:

```bash
$ python setup.py
```

A prompt will appear in the terminal asking whether the user wants to overwrite the existing setup file. To create a custom setup, users should respond with 'yes' (y).

![overwrite](https://github.com/yanvgf/line-follower-simulator/assets/93750334/ff891163-c0d3-4ac3-9182-331f4eddf454)

First, users will be prompted to place the robot within the arena. This involves clicking on the map to position the robot and scrolling to rotate it. Then, sensors must be positioned on the robot by simply left-clicking to place each sensor.

![setup_v2](https://github.com/yanvgf/line-follower-simulator/assets/93750334/472d1e60-ce6c-4895-9372-5ab255cccaae)

The setup process is complete once all sensors are positioned. The robot's position, sensor placements, and parameters will be automatically saved in the setup.txt file, eliminating the need to repeat this procedure every time.

### main.py

The simulation executes based on the robot parameters and setup defined in the setup stage. To run the simulation, use the following command:

```bash
$ python main.py
```

The simulation will continue until the robot reaches the goal or until you close the window.

### Changing robot and map images

Users can modify the robot and map images by replacing the robot.png and map.png files in the images folder. **Ensure that your robot is positioned at zero angle in the image (i.e., pointing to the right)**.

The robot will follow any black or dark line present on the map.

## References

Some of the code used in this project was based on the following videos:

- [Algobotics: Simulating an Obstacle Avoidance Robot Using Python | From Scratch](https://www.youtube.com/watch?v=pmmUi6DasoM)
- [robojunkies: How to code your Line follower robot with PID control and working code!](https://www.youtube.com/watch?v=8Lj5ycrT9Fw)
- [Tech with Tim: How to Make a Game in Python](https://www.youtube.com/watch?v=waY3LfJhQLY)


