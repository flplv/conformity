using System.Collections;
using System.Diagnostics;
using System.Threading;
using NetMQ;
using NetMQ.Sockets;

public class NetMQReplier
{
    public delegate string MessageDelegate(string message);
    private bool listenerCancelled;
    private readonly MessageDelegate messageDelegate;
    private readonly Thread listenerWorker;
    private readonly Stopwatch contactWatch;

    public NetMQReplier(MessageDelegate messageDelegate) 
    {
        this.messageDelegate = messageDelegate;
        contactWatch = new Stopwatch();
        contactWatch.Start();
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

    private void ListenerWork() 
    {
        AsyncIO.ForceDotNet.Force();
        using (var server = new ResponseSocket()) 
        {
            server.Bind("tcp://*:12346");

            while (!listenerCancelled) 
            {
                string message;
                if (!server.TryReceiveFrameString(out message)) continue;
                contactWatch.Restart();
                var response = messageDelegate(message);
                server.SendFrame(response);
            }
        }
        NetMQConfig.Cleanup();
    }

}