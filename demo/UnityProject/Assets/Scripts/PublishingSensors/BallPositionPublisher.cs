using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BallPositionPublisher : MonoBehaviour {
    public Camera cameraDetector;
    public Renderer[] ballRenderers;

    private void FixedUpdate() {
        foreach (Renderer ballRenderer in ballRenderers) {
            bool isRendered = ballRenderer.IsVisibleFrom(cameraDetector);
            RaycastHit hitInfo;
            Physics.Linecast(cameraDetector.transform.position, ballRenderer.transform.position, out hitInfo);
            bool isInLineOfSight = hitInfo.transform?.GetInstanceID() == ballRenderer.transform?.GetInstanceID();

            if (isRendered && isInLineOfSight)
                print($"{ballRenderer.name} visible");
            else
                print($"{ballRenderer.name} NOT visible");
        }
    }
}
