using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraPublisher : MonoBehaviour {
    public ImageSynthesis imageSynthesis;
	public NetMQPublisher netMQPublisher;
	private float _timeStart;
    private const float _sampleRate = 1f; // in seconds

    private void Start() {
		_timeStart = Time.time;
    }

    private void FixedUpdate() {
		float elapsedTime = Time.time - _timeStart;
		if (elapsedTime > _sampleRate) {
			_timeStart = Time.time;
			SendCameraFrame("sensor_camera", "_id");
        }
    }

    private void SendCameraFrame(string frame_name, string capturePassName, int width = -1, int height = -1) {
		if (width <= 0 || height <= 0) {
			width = Screen.width;
			height = Screen.height;
		}

		// execute as coroutine to wait for the EndOfFrame before capture
		StartCoroutine(WaitForEndOfFrameAndSend(frame_name, capturePassName, width, height));
	}

	private IEnumerator WaitForEndOfFrameAndSend(string frame_name, string capturePassName, int width, int height) {
		yield return new WaitForEndOfFrame();
		var buffer = imageSynthesis.GetPNGBufferFromCapturePass(capturePassName, width, height);
		netMQPublisher.PublishData(frame_name, buffer);
	}
}
