﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PositionPublisher : MonoBehaviour {
	public NetMQPublisher netMQPublisher;
	private const float _sampleRate = 1f; // in seconds -- minimum is Physics Timestep
	private float _timeStart;

	private void Start() {
		_timeStart = Time.time;
	}

	private void FixedUpdate() {
		float elapsedTime = Time.time - _timeStart;
		if (elapsedTime > _sampleRate) {
			_timeStart = Time.time;
			SendPosition("position");
		}
	}

	private void SendPosition(string frameName) {
		string data = $"{transform.position.x} " +
			$"{transform.position.y} " +
			$"{transform.position.z} " +
			$"{transform.rotation.eulerAngles.y}";
		netMQPublisher.PublishData(frameName, data);
	}
}