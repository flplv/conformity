using System.Collections.Generic;
using UnityEngine;

public class NetworkRequestHandler : MonoBehaviour 
{
    [SerializeField]
    private float botSpeed = 1f;
    
    [SerializeField]
    private SimulationTickControl simulationControl;

    [SerializeField]
    private ObjectGrasper objectGrasper;

    [SerializeField]
    private ObjectPositionSensor objectPositionSensor;

    [SerializeField]
    private RobotPositionSensor robotPositionSensor;

    [SerializeField]
    private BotMovement botMovement;

    [SerializeField]
    private Transform dropzonePoint;

    private NetMQReplier netMqReplier;

    private List<IPackedRoutine> mainThreadRoutines = new List<IPackedRoutine>();

    private void Start() 
    {
        netMqReplier = new NetMQReplier(HandleMessage);
        netMqReplier.Start();
    }

    public void ScheduleDropObjectEffect()
    {
        mainThreadRoutines.Add(new DropObjectEffect(objectGrasper));
    }

    public void ScheduleGraspObjectEffect()
    {
        mainThreadRoutines.Add(new GraspObjectEffect(objectGrasper));
    }

    public void ScheduleGoToDropzoneEffect()
    {
        mainThreadRoutines.Add(new GoToDropzoneEffect(botMovement, dropzonePoint, botSpeed));
    }

    public void ScheduleGoToObjectEffect()
    {
        mainThreadRoutines.Add(new GoToObjectEffect(botMovement, objectPositionSensor, botSpeed));
    }

    private void Update() 
    {
        foreach (var routine in mainThreadRoutines) 
        {
            routine.Execute();
        }
        mainThreadRoutines.Clear();
    }
    
    // Not on main thread
    private string HandleMessage(string message) 
    {
        string response = "bad_message";

        // tick simulation
        if (message == "tick") 
        {
            simulationControl.Tick();
            response = "tick_ok";
        }

        // sensors
        if (message == "sensor_objectinsight") 
            response = objectPositionSensor.ObjectInOmniSight().ToString(); // true / false
        if (message == "sensor_objectinrange") 
            response = objectGrasper.ObjectInRange().ToString(); // true / false
        if (message == "sensor_objectgrasped") 
            response = objectGrasper.ObjectGrasped().ToString(); // true / false
        if (message == "sensor_robotindropzone") 
            response = robotPositionSensor.RobotInDropZone().ToString(); // true / false
        
        // control
        if (message == "control_gotoobjectposition")
        {
            ScheduleGoToObjectEffect();
            response = "ok";
        }
        if (message == "control_gotodropzone")
        {
            ScheduleGoToDropzoneEffect();
            response = "ok";
        }
        if (message == "control_graspobject")
        {
            ScheduleGraspObjectEffect();
            response = "ok";
        }
        if (message == "control_dropobject")
        {
            ScheduleDropObjectEffect();
            response = "ok";
        }
        return response;
    }

    private interface IPackedRoutine
    {
        void Execute();
    }

    private class DropObjectEffect : IPackedRoutine
    {
        private ObjectGrasper objectGrasper;

        public DropObjectEffect(ObjectGrasper objectGrasper)
        {
            this.objectGrasper = objectGrasper;
        }

        public void Execute()
        {
            objectGrasper.DropObject();
        }
    }

    private class GraspObjectEffect : IPackedRoutine
    {
        private ObjectGrasper objectGrasper;

        public GraspObjectEffect(ObjectGrasper objectGrasper)
        {
            this.objectGrasper = objectGrasper;
        }

        public void Execute()
        {
            objectGrasper.GraspObject();
        }
    }

    private class GoToDropzoneEffect : IPackedRoutine
    {
        private BotMovement botMovement;
        private Transform dropzonePoint;
        private float speed;

        public GoToDropzoneEffect(BotMovement botMovement, Transform dropzonePoint, float speed)
        {
            this.botMovement = botMovement;
            this.dropzonePoint = dropzonePoint;
            this.speed = speed;
        }

        public void Execute()
        {
            botMovement.GoToPoint(dropzonePoint.position, speed);
        }
    }

    private class GoToObjectEffect : IPackedRoutine
    {
        private BotMovement botMovement;
        private ObjectPositionSensor objectPositionSensor;
        private float speed;

        public GoToObjectEffect(BotMovement botMovement, ObjectPositionSensor objectPositionSensor, float speed)
        {
            this.botMovement = botMovement;
            this.objectPositionSensor = objectPositionSensor;
            this.speed = speed;
        }

        public void Execute()
        {
            if (objectPositionSensor.ObjectInOmniSight())
            {
                Vector3 objectPoint = objectPositionSensor.ObjectInOmniSightPosition();
                botMovement.GoToPoint(objectPoint, speed);
            }
        }
    }

    private void OnDestroy() 
    {
        netMqReplier.Stop();
    }

}
