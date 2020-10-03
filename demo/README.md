## Tick-Based Robot Simulator

This is a four wheeled robot made in Unity with locked timestep simulation. 

You interact with it through ZMQ network messages using a simple REQ-REP pattern.

To advance the simulation in 1 tick (default: 2 ms) you need to send the appropriate request message. You can also send messages to retrieve data or issue commands. 

#### Current protocol:

* Effect: Tick simulation forward
  * REQ: "tick"
  * REP: "tick_ok"
* Effect: Do Nothing
  * REQ: "sensor_1"
  * REP: "this_is_sensor_1_data"
* Effect: Do Nothing
  * REQ: "control_1"
  * REP: "control_1_ok"

#### To open/build this project you need Unity 2019.4.8f1

###### Open the project in the editor or build directly with the following commands:

###### Build for Windows:
`"C:\UnityPath\Unity.exe" -quit -batchmode -buildWindows64Player "WinBuild\GoRobot.exe"`

###### Build for Linux:
`"C:\UnityPath\Unity.exe" -quit -batchmode -buildLinux64Player "LinuxBuild\GoRobot.exe"`

