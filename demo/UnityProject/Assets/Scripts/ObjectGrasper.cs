using System.Collections;
using System.Collections.Generic;
using System.Dynamic;
using UnityEngine;

public class ObjectGrasper : MonoBehaviour
{
    [SerializeField]
    private Transform graspableObjects;

    [SerializeField]
    private Transform graspingPosition;

    private List<GameObject> inRangeObjects = new List<GameObject>();
    private GameObject graspedObject;

    public void GraspObject()
    {
        // already grasping something
        if (graspedObject != null) return;
        
        // nothing to grasp
        if (inRangeObjects.Count == 0) return;

        graspedObject = inRangeObjects[0];
        inRangeObjects.RemoveAt(0);
        graspedObject.GetComponent<Rigidbody>().isKinematic = true;
    }

    public void DropObject()
    {
        // nothing to release
        if (graspedObject == null) return;

        graspedObject.transform.position += graspingPosition.forward * 0.5f;
        graspedObject.GetComponent<Rigidbody>().isKinematic = false;
        graspedObject = null;
    }

    public bool ObjectGrasped()
    {
        return graspedObject != null;
    }

    public bool ObjectInRange()
    {
        if (inRangeObjects.Count > 0) return true;
        return false;
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.transform.parent == graspableObjects)
        {
            inRangeObjects.Add(other.gameObject);
        }
    }

    private void OnTriggerExit(Collider other)
    {
        inRangeObjects.Remove(other.gameObject);
    }
    
    private void Update()
    {
        if (graspedObject != null)
        {
            graspedObject.transform.position = graspingPosition.position;
        }
    }

}
