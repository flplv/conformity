using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WheelRotate : MonoBehaviour
{
    [SerializeField]
    private float tireDiameter = 0.3f;
    private Rigidbody _rigidbody;
    private Transform _objectToRotate;
    private float _eulerAngle;
    private float _objectAngleY;
    private float _objectAngleZ;

    private void Awake() {
        _rigidbody = GetComponentInParent<Rigidbody>();
        _objectToRotate = transform.GetChild(0);
        _objectAngleY = _objectToRotate.localEulerAngles.y;
        _objectAngleZ = _objectToRotate.localEulerAngles.z;
    }

    private void Update() {
        float deltaMovement = Time.deltaTime * transform.InverseTransformDirection(_rigidbody.velocity).z;
        float angleStep = 360 / (tireDiameter * Mathf.PI) * deltaMovement;
        _eulerAngle += angleStep;
        _objectToRotate.localEulerAngles = new Vector3(_eulerAngle, _objectAngleY, _objectAngleZ);
    }
}
