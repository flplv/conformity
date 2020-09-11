using System.Collections.Concurrent;
using System.Threading;
using NetMQ;
using NetMQ.Sockets;
using UnityEngine;

public class NetMQSubscriber {
    public delegate void MessageDelegate(string message);
    private readonly Thread _listenerWorker;
    private bool _listenerCancelled;
    private readonly MessageDelegate _messageDelegate;
    private readonly ConcurrentQueue<string> _messageQueue = new ConcurrentQueue<string>();

    public NetMQSubscriber(MessageDelegate messageDelegate) {
        _messageDelegate = messageDelegate;
        _listenerWorker = new Thread(ListenerWork);
    }

    public void Start() {
        _listenerCancelled = false;
        _listenerWorker.Start();
    }

    public void Stop() {
        _listenerCancelled = true;
        _listenerWorker.Join();
    }

    public void Update() {
        while (!_messageQueue.IsEmpty) {
            string message;
            if (_messageQueue.TryDequeue(out message)) {
                _messageDelegate(message);
            } else break;
        }
    }

    private void ListenerWork() {
        AsyncIO.ForceDotNet.Force();
        using (var subSocket = new SubscriberSocket()) {
            subSocket.Options.ReceiveHighWatermark = 1000;
            subSocket.Connect("tcp://localhost:12345");
            subSocket.Subscribe("");
            while (!_listenerCancelled) {
                string frameString;
                if (!subSocket.TryReceiveFrameString(out frameString)) continue;
                Debug.Log(frameString);
                _messageQueue.Enqueue(frameString);
            }
            subSocket.Close();
        }
        NetMQConfig.Cleanup();
    }
}