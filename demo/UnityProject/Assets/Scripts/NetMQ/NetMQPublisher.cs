using System.Collections;
using UnityEngine;
using NetMQ;
using NetMQ.Sockets;

public class NetMQPublisher : MonoBehaviour 
{
    private PublisherSocket pubSocket;

    public void PublishData(string topic, byte[] data) 
    {
        pubSocket.SendMoreFrame(topic).SendFrame(data);
    }

    public void PublishData(string topic, string data) 
    {
        pubSocket.SendMoreFrame(topic).SendFrame(data);
    }

    private void OnEnable() 
    {
        PreparePublishing();
    }

    private void OnDisable() 
    {
        StopPublishing();
    }

    private void PreparePublishing() 
    {
        AsyncIO.ForceDotNet.Force();
        pubSocket = new PublisherSocket();
        pubSocket.Options.SendHighWatermark = 100;
        pubSocket.Bind("tcp://localhost:12344");
    }

    private void StopPublishing() 
    {
        pubSocket.Close();
        NetMQConfig.Cleanup();
    }

}
