using UnityEngine;

// use example
public class NetMQSubscriberObject : MonoBehaviour
{
    private NetMQSubscriber _netMqListener;

    private void Start()
    {
        _netMqListener = new NetMQSubscriber(HandleMessage);
        _netMqListener.Start();
    }

    private void Update()
    {
        _netMqListener.Update();
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
        _netMqListener.Stop();
    }
}
