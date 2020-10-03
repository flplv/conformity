using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ObjectPositionSensor : MonoBehaviour
{
    [SerializeField]
    private Camera cameraDetector;

    [SerializeField]
    private Transform detectableObjects;

    [SerializeField]
    public Transform omnisightPoint;
    
    private Transform transformInCameraSight;
    private Transform transformInOmniSight;

    private void FixedUpdate()
    {
        transformInCameraSight = null;
        transformInOmniSight = null;
        foreach (Transform detectableObject in detectableObjects)
        {
            var renderer = detectableObject.GetComponent<Renderer>();
            bool isActive = detectableObject.gameObject.activeInHierarchy;
            bool isInOmnidirectionalLineOfSight = IsInLineOfSight(omnisightPoint.position, detectableObject);
            bool isInCameraLineOfSight = IsInLineOfSight(cameraDetector.transform.position, detectableObject);
            bool isRendered = renderer.IsVisibleFrom(cameraDetector);

            if (isActive && isInOmnidirectionalLineOfSight)
            {
                transformInOmniSight = detectableObject;
            }
            if (isActive && isInCameraLineOfSight && isRendered)
            {
                transformInCameraSight = detectableObject;
            }
        }
    }

    public bool ObjectInCameraSight()
    {
        return transformInCameraSight != null;
    }

    public bool ObjectInOmniSight()
    {
        return transformInOmniSight != null;
    }

    public Vector3 ObjectInCameraSightPosition()
    {
        return transformInCameraSight?.position ?? new Vector3(0, 0, 0);
    }

    public Vector3 ObjectInOmniSightPosition()
    {
        return transformInOmniSight?.position ?? new Vector3(0, 0, 0);
    }

    private static bool IsInLineOfSight(Vector3 origin, Transform destinationTransform)
    {
        RaycastHit hitInfo;
        Physics.Linecast(origin, destinationTransform.position, out hitInfo);
        bool clearPath = hitInfo.transform?.GetInstanceID() == destinationTransform.GetInstanceID();
        return clearPath;
    }

}
