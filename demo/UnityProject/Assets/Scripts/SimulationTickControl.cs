using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SimulationTickControl : MonoBehaviour 
{
    private bool tickReceived = false;

    // Allow simulation to run one more tick
    public void Tick() 
    {
        tickReceived = true;
    }

    private void OnEnable() 
    {
        StartCoroutine(TimeStepControl());
    }

    // On next physics update, pause and wait for Tick()
    private IEnumerator TimeStepControl() 
    {
        while (true) 
        {
            yield return new WaitForFixedUpdate();
            Time.timeScale = 0f;
            yield return new WaitUntil(() => tickReceived);
            Time.timeScale = 1f;
            tickReceived = false;
        }
    }

    private void OnDisable() 
    {
        StopAllCoroutines();
        Time.timeScale = 1f;
    }

}
