using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ObjectDetectionHider : MonoBehaviour
{
    [SerializeField]
    public Transform detectableObjectsContainer;

    [SerializeField]
    public Transform undetectableObjectsContainer;

    [SerializeField]
    public Collider dropzoneTrigger;

    private void OnTriggerEnter(Collider other)
    {
        if (other == dropzoneTrigger)
        {
            transform.SetParent(undetectableObjectsContainer);
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if (other == dropzoneTrigger)
        {
            transform.SetParent(detectableObjectsContainer);
        }
    }

}
