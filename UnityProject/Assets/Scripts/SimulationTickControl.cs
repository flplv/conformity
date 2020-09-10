using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SimulationTickControl : MonoBehaviour
{
    private bool _tickReceived = false;

    // Allow simulation to run one more tick
    public void Tick() {
        _tickReceived = true;
    }

    private void OnEnable() {
        StartCoroutine(TimeStepControl());
    }

    // On next physics update, pause simulation and wait for Tick()
    private IEnumerator TimeStepControl() {
        while (true) {
            yield return new WaitForFixedUpdate();
            Time.timeScale = 0f;
            yield return new WaitUntil(() => _tickReceived);
            Time.timeScale = 1f;
            _tickReceived = false;
        }
    }

    private void OnDisable() {
        StopAllCoroutines();
        Time.timeScale = 1f;
    }

}
