// utility to shape JSON sent to the Django endpoints.
using System;

[Serializable]
public class StartSessionRequest
{
    public int game_id;          // exactly as API expects
    public int prescription_id;  // exactly as API expects
}

[Serializable]
public class StartSessionResponse
{
    public int id;               // session id returned by server
}

[Serializable]
public class EegReadingRequest
{
    public int session;
    public string timestamp;       // ISO8601, UTC
    public float attention;        // 0..1
    public float meditation;       // 0..1
    public float delta;
    public float theta;
    public float low_alpha;
    public float high_alpha;
    public float low_beta;
    public float high_beta;
    public float low_gamma;
    public float mid_gamma;
}
