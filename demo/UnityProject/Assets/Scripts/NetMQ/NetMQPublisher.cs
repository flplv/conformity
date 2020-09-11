using System.Collections;
using UnityEngine;
using NetMQ;
using NetMQ.Sockets;

public class NetMQPublisher : MonoBehaviour {
    private PublisherSocket _pubSocket;

    private void OnEnable() {
        PreparePublishing();
    }

    public void PublishData(string topic, byte[] data) {
        _pubSocket.SendMoreFrame(topic).SendFrame(data);
    }

    public void PublishData(string topic, string data) {
        _pubSocket.SendMoreFrame(topic).SendFrame(data);
    }

    private void PreparePublishing() {
        AsyncIO.ForceDotNet.Force();
        _pubSocket = new PublisherSocket();
        _pubSocket.Options.SendHighWatermark = 100;
        _pubSocket.Bind("tcp://localhost:12344");
    }

    private void StopPublishing() {
        _pubSocket.Close();
        NetMQConfig.Cleanup();
    }

    private void OnDisable() {
        StopPublishing();
    }
}
