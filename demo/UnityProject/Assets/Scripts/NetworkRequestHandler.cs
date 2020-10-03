using UnityEngine;

public class NetworkRequestHandler : MonoBehaviour {
    public SimulationTickControl simulationControl;
    private NetMQReplier _netMqReplier;
    private string _response;

    private void Start() {
        _netMqReplier = new NetMQReplier(HandleMessage);
        _netMqReplier.Start();
    }

    private string HandleMessage(string message) {
        // Not on main thread
        if (message == "tick") {
            simulationControl.Tick();
            _response = "tick_ok";
        }
        if (message == "sensor_1") _response = "this_is_sensor_1_data";
        if (message == "control_1") _response = "control_1_ok";
        return _response;
    }

    private void OnDestroy() {
        _netMqReplier.Stop();
    }
}
