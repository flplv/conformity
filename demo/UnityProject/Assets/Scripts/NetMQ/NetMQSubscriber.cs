using System.Collections.Concurrent;
using System.Threading;
using NetMQ;
using NetMQ.Sockets;
using UnityEngine;

public class NetMQSubscriber 
{
    public delegate void MessageDelegate(string message);
    private readonly Thread listenerWorker;
    private bool listenerCancelled;
    private readonly MessageDelegate messageDelegate;
    private readonly ConcurrentQueue<string> messageQueue = new ConcurrentQueue<string>();

    public NetMQSubscriber(MessageDelegate messageDelegate) 
    {
        this.messageDelegate = messageDelegate;
        listenerWorker = new Thread(ListenerWork);
    }

    public void Start() 
    {
        listenerCancelled = false;
        listenerWorker.Start();
    }

    public void Stop() 
    {
        listenerCancelled = true;
        listenerWorker.Join();
    }

    public void Update() 
    {
        while (!messageQueue.IsEmpty) 
        {
            string message;
            if (messageQueue.TryDequeue(out message)) 
            {
                messageDelegate(message);
            } 
            else break;
        }
    }

    private void ListenerWork() 
    {
        AsyncIO.ForceDotNet.Force();
        using (var subSocket = new SubscriberSocket()) 
        {
            subSocket.Options.ReceiveHighWatermark = 1000;
            subSocket.Connect("tcp://localhost:12345");
            subSocket.Subscribe("");
            while (!listenerCancelled) 
            {
                string frameString;
                if (!subSocket.TryReceiveFrameString(out frameString)) continue;
                Debug.Log(frameString);
                messageQueue.Enqueue(frameString);
            }
            subSocket.Close();
        }
        NetMQConfig.Cleanup();
    }

}