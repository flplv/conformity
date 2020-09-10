using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BotMovement : MonoBehaviour
{
    private Rigidbody _rigidBody;

    private void Awake() {
        _rigidBody = GetComponent<Rigidbody>();
    }

    // TBD protocols
    public void ProcessVelocityMessage(string message) {
        var splittedStrings = message.Split(' ');
        if (splittedStrings.Length != 2) {
            Debug.LogError("invalid velocity message received");
            return;
        }
        var vx = float.Parse(splittedStrings[0]);
        var vz = float.Parse(splittedStrings[1]);
        //Debug.Log("Setting velocity vx:" + vx.ToString() + " vz:" + vz.ToString());
        SetVelocity(vx, vz);
    }

    public void ProcessSpeedAndAngleMessage(string message) {
        var splittedStrings = message.Split(' ');
        if (splittedStrings.Length != 2) {
            Debug.LogError("invalid speed/angle message received");
            return;
        }
        var speed = float.Parse(splittedStrings[0]);
        var angle = float.Parse(splittedStrings[1]);
        //Debug.Log("Setting speed:" + speed.ToString() + " angle:" + angle.ToString());
        SetSpeedAndAngle(speed, angle);
    }

    private void SetVelocity(float velX, float velZ) {
        _rigidBody.velocity = new Vector3(velX, 0f, velZ);
    }

    private void SetSpeedAndAngle(float speed, float angle) {
        transform.eulerAngles = new Vector3(0f, angle, 0f);
        _rigidBody.velocity = transform.forward * speed;
    }
}
