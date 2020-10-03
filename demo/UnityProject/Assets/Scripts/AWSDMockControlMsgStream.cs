using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AWSDMockControlMsgStream : MonoBehaviour {
    public BotMovement botMovement;
    private float _speed;
    private float _angle;

    private void FixedUpdate() {
        if(Input.GetKey(KeyCode.W)) {
            _speed += 0.01f;
        }
        if (Input.GetKey(KeyCode.S)) {
            _speed -= 0.01f;
        }
        if (Input.GetKey(KeyCode.A)) {
            _angle -= 1f;
        }
        if (Input.GetKey(KeyCode.D)) {
            _angle += 1f;
        }

        // angle restriction 0 to 360
        if (_angle > 360f) _angle -= 360f;
        if (_angle < 0f) _angle += 360f;

        string msg = _speed.ToString() + " " + _angle.ToString();
        botMovement.ProcessSpeedAndAngleMessage(msg);
    }

}