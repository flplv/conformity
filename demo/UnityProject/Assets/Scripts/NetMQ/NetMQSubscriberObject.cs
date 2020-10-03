using UnityEngine;

public class NetMQSubscriberObject : MonoBehaviour 
{
    private NetMQSubscriber netMQSubscriber;

    private void Start() 
    {
        netMQSubscriber = new NetMQSubscriber(HandleMessage);
        netMQSubscriber.Start();
    }

    private void Update() 
    {
        netMQSubscriber.Update();
    }

    private void HandleMessage(string message) 
    {
        var splittedStrings = message.Split(' ');
        if (splittedStrings.Length != 3) return;
        var x = float.Parse(splittedStrings[0]);
        var y = float.Parse(splittedStrings[1]);
        var z = float.Parse(splittedStrings[2]);
        transform.position = new Vector3(x, y, z);
    }

    private void OnDestroy() 
    {
        netMQSubscriber.Stop();
    }

}
