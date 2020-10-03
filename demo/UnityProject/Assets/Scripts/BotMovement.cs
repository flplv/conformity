using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BotMovement : MonoBehaviour 
{
    private Rigidbody rigidBody;

    private void Awake() 
    {
        rigidBody = GetComponent<Rigidbody>();
    }

    // msg parsing -- todo: do it somewhere else
    public void ProcessVelocityMessage(string message) 
    {
        var splittedStrings = message.Split(' ');
        if (splittedStrings.Length != 2)
        {
            Debug.LogError("invalid velocity message received");
            return;
        }
        var vx = float.Parse(splittedStrings[0]);
        var vz = float.Parse(splittedStrings[1]);
        SetVelocity(vx, vz);
    }

    // msg parsing -- todo: do it somewhere else
    public void ProcessSpeedAndAngleMessage(string message) 
    {
        var splittedStrings = message.Split(' ');
        if (splittedStrings.Length != 2)
        {
            Debug.LogError("invalid speed/angle message received");
            return;
        }
        var speed = float.Parse(splittedStrings[0]);
        var angle = float.Parse(splittedStrings[1]);
        SetSpeedAndAngle(speed, angle);
    }

    private void SetVelocity(float velX, float velZ) 
    {
        rigidBody.velocity = new Vector3(velX, 0f, velZ);
    }

    private void SetSpeedAndAngle(float speed, float angle) 
    {
        transform.eulerAngles = new Vector3(0f, angle, 0f);
        rigidBody.velocity = transform.forward * speed;
    }

    public void GoToPoint(Vector3 point, float speed) 
    {
        Debug.Log($"GoToPoint point: {point} speed: {speed}");
        float angle = Mathf.Atan2(point.x - transform.position.x, point.z - transform.position.z) / 2 / Mathf.PI * 360;
        SetSpeedAndAngle(speed, angle);
        StopAllCoroutines();
        StartCoroutine(StopAtDestination(point));
    }

    private IEnumerator StopAtDestination(Vector3 point) 
    {
        while (true) 
        {
            yield return new WaitForFixedUpdate();
            Vector3 xzDestination = Vector3.Scale(point, new Vector3(1f, 0f, 1f));
            Vector3 xzOrigin = Vector3.Scale(transform.position, new Vector3(1f, 0f, 1f));
            float distance = Vector3.Distance(xzDestination, xzOrigin);
            if (distance <= 0.1f) SetVelocity(0f, 0f);
        }
    }

}
