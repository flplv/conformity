## Tick-Based Robot Simulator

This is a four wheeled robot made in Unity with locked timestep simulation. 

You interact with it through ZMQ network messages using a simple REQ-REP pattern.

To advance the simulation in 1 tick (default: 2 ms) you need to send the appropriate request message. You can also send messages to retrieve data or issue commands. 

#### Current protocol:

* Effect: Tick simulation forward
  * REQ: "tick"
  * REP: "tick_ok"
* Effect: Check if there's any graspable object in line of sight
  * REQ: "sensor_objectinsight"
  * REP: "True" or "False"
* Effect: Check if there's any graspable object in grasp range
  * REQ: "sensor_objectinrange"
  * REP: "True" or "False"
* Effect: Check if there's any object currently grasped
  * REQ: "sensor_objectgrasped"
  * REP: "True" or "False"
* Effect: Check if robot is in drop zone
  * REQ: "sensor_robotindropzone"
  * REP: "True" or "False"
* Effect: Make the robot go to a graspable object position currently in sight
  * REQ: "control_gotoobjectposition"
  * REP: "ok"
* Effect: Make the robot go to drop zone position
  * REQ: "control_gotodropzone"
  * REP: "ok"
* Effect: Make the robot grasp a graspable object in range
  * REQ: "control_graspobject"
  * REP: "ok"
* Effect: Make the robot drop the currently grasped object
  * REQ: "control_dropobject"
  * REP: "ok"

#### To open/build this project you need Unity 2019.4.8f1

###### Open the project in the editor or build directly with the following commands:

###### Build for Windows:
`"C:\UnityPath\Unity.exe" -quit -batchmode -buildWindows64Player "WinBuild\GoRobot.exe"`

###### Build for Linux:
`"C:\UnityPath\Unity.exe" -quit -batchmode -buildLinux64Player "LinuxBuild\GoRobot.exe"`

