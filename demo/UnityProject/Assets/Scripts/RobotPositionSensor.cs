using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RobotPositionSensor : MonoBehaviour
{
    [SerializeField]
    private Collider dropZoneCollider;

    private bool inDropZone;

    private void FixedUpdate()
    {
        inDropZone = dropZoneCollider.bounds.Contains(transform.position);
    }

    public bool RobotInDropZone()
    {
        return inDropZone;
    }

}
