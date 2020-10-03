using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WheelRotate : MonoBehaviour 
{
    [SerializeField]
    private float tireDiameter = 0.3f;

    private Rigidbody rigidbody;
    private Transform objectToRotate;
    private float eulerAngle;
    private float objectAngleY;
    private float objectAngleZ;

    private void Awake() {
        rigidbody = GetComponentInParent<Rigidbody>();
        objectToRotate = transform.GetChild(0);
        objectAngleY = objectToRotate.localEulerAngles.y;
        objectAngleZ = objectToRotate.localEulerAngles.z;
    }

    private void Update() {
        float deltaMovement = Time.deltaTime * transform.InverseTransformDirection(rigidbody.velocity).z;
        float angleStep = 360 / (tireDiameter * Mathf.PI) * deltaMovement;
        eulerAngle += angleStep;
        objectToRotate.localEulerAngles = new Vector3(eulerAngle, objectAngleY, objectAngleZ);
    }
}
