using System.Diagnostics;
using System.Threading;
using NetMQ;
using NetMQ.Sockets;

public class NetMQReplier
{
    public delegate string MessageDelegate(string message);

    public bool Connected;

    private bool _listenerCancelled;
    
    private readonly MessageDelegate _messageDelegate;
    
    private readonly Thread _listenerWorker;

    private readonly Stopwatch _contactWatch;

    private const long ContactThreshold = 1000;

    public NetMQReplier(MessageDelegate messageDelegate)
    {
        _messageDelegate = messageDelegate;
        _contactWatch = new Stopwatch();
        _contactWatch.Start();
        _listenerWorker = new Thread(ListenerWork);
    }

    public void Start()
    {
        _listenerCancelled = false;
        _listenerWorker.Start();
    }

    public void Stop()
    {
        _listenerCancelled = true;
        _listenerWorker.Join();
    }

    private void ListenerWork()
    {
        AsyncIO.ForceDotNet.Force();
        using (var server = new ResponseSocket())
        {
            server.Bind("tcp://*:12346");

            while (!_listenerCancelled)
            {
                Connected = _contactWatch.ElapsedMilliseconds < ContactThreshold;
                string message;
                if (!server.TryReceiveFrameString(out message)) continue;
                _contactWatch.Restart();
                var response = _messageDelegate(message);
                server.SendFrame(response);
            }
        }
        NetMQConfig.Cleanup();
    }

}