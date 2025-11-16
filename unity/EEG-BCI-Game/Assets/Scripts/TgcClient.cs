using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

#if !UNITY_WEBGL || UNITY_EDITOR
using System.Net.Sockets;
using System.Text;
using System.Threading;
#else
using NativeWebSocket;
using System.Text;
#endif

public class TgcClient : MonoBehaviour
{
    [Header("TGC TCP Settings (Editor / Standalone)")]
    public string host = "127.0.0.1";
    public int port = 13854;

    [Header("WebGL WebSocket Settings (via tgc-proxy.js)")]
    public string wsUrl = "ws://127.0.0.1:13855";

#if !UNITY_WEBGL || UNITY_EDITOR
    TcpClient client;
    NetworkStream stream;
    Thread reader;
    volatile bool running;
#else
    NativeWebSocket.WebSocket ws;
#endif

    int rawEegValue = int.MinValue;

    public struct EegPower
    {
        public int delta, theta, lowAlpha, highAlpha, lowBeta, highBeta, lowGamma, midGamma;
    }

    // values shared between thread/WS callbacks and main thread
    public int attentionValue { get; private set; } = -1;
    public int meditationValue { get; private set; } = -1;
    EegPower latestEegPower;

    public int signalStrength { get; private set; } = -1;

    // debug message queue
    private readonly System.Collections.Concurrent.ConcurrentQueue<string> logQueue
        = new System.Collections.Concurrent.ConcurrentQueue<string>();

    // shared buffer for splitting JSON lines
    private readonly StringBuilder buffer = new StringBuilder();

    // events usable from other scripts
    public event Action<int> AttentionChanged;
    public event Action<int> MeditationChanged;
    public event Action<int> RawEegReceived;
    public event Action<EegPower> EegPowerReceived;
    public event Action<int> SignalStrengthChanged;

    async void Start()
    {
#if !UNITY_WEBGL || UNITY_EDITOR
        try
        {
            client = new TcpClient();
            client.Connect(host, port);
            stream = client.GetStream();
            running = true;

            // Ask TGC for JSON output
            var cfg = Encoding.ASCII.GetBytes("{\"enableRawOutput\":true,\"format\":\"Json\"}\n");
            stream.Write(cfg, 0, cfg.Length);

            Debug.Log($"[TGC] TCP connected to {host}:{port}. Requesting JSON…");

            reader = new Thread(ReadLoop) { IsBackground = true };
            reader.Start();
        }
        catch (Exception e)
        {
            Debug.LogError("[TGC] TCP connect failed: " + e.Message);
        }
#else
        ws = new WebSocket(wsUrl);

        ws.OnOpen += () =>
        {
            Debug.Log("[TGC] WS connected to proxy, requesting JSON…");
            // same config as TCP but through WebSocket
            var cfg = "{\"enableRawOutput\":true,\"format\":\"Json\"}\n";
            ws.SendText(cfg);
        };

        ws.OnError += (err) =>
        {
            Debug.LogError("[TGC] WS error: " + err);
        };

        ws.OnClose += (code) =>
        {
            Debug.Log("[TGC] WS closed: " + code);
        };

        ws.OnMessage += (bytes) =>
        {
            // bytes may contain partial/multiple JSON lines, just like TCP
            var chunk = Encoding.ASCII.GetString(bytes);
            ProcessChunk(chunk);
        };

        try
        {
            await ws.Connect();
        }
        catch (Exception e)
        {
            Debug.LogError("[TGC] WS connect failed: " + e.Message);
        }
#endif
    }

    void Update()
    {
        // drain debug messages
        while (logQueue.TryDequeue(out var msg))
        {
            Debug.Log(msg);
        }

        // dispatch values to listeners on main thread
        if (signalStrength >= 0)
        {
            SignalStrengthChanged?.Invoke(signalStrength);
        }
        if (attentionValue >= 0)
        {
            AttentionChanged?.Invoke(attentionValue);
        }
        if (meditationValue >= 0)
        {
            MeditationChanged?.Invoke(meditationValue);
        }
        if (rawEegValue != int.MinValue)
        {
            RawEegReceived?.Invoke(rawEegValue);
            rawEegValue = int.MinValue;
        }
        EegPowerReceived?.Invoke(latestEegPower);
    }

#if !UNITY_WEBGL || UNITY_EDITOR
    void ReadLoop()
    {
        var buf = new byte[4096];
        while (running)
        {
            try
            {
                int n = stream.Read(buf, 0, buf.Length);
                if (n <= 0) break;

                var chunk = Encoding.ASCII.GetString(buf, 0, n);
                ProcessChunk(chunk);
            }
            catch (Exception e)
            {
                Debug.LogWarning("[TGC] ReadLoop ended: " + e.Message);
                break;
            }
        }
        running = false;
    }
#endif

    /// <summary>
    /// Handles arbitrary chunks from TCP or WebSocket, splits by '\r',
    /// and feeds complete JSON lines into HandleMessage.
    /// </summary>
    void ProcessChunk(string chunk)
    {
        lock (buffer)
        {
            buffer.Append(chunk);

            int idx;
            while ((idx = buffer.ToString().IndexOf('\r')) >= 0)
            {
                string line = buffer.ToString(0, idx);
                buffer.Remove(0, idx + 1);

                if (!string.IsNullOrWhiteSpace(line))
                {
                    HandleMessage(line);
                }
            }
        }
    }

    void HandleMessage(string jsonLine)
    {
        //  signal strength
        if (jsonLine.Contains("\"poorSignalLevel\""))
        {
            int sig = Extract(jsonLine, "\"poorSignalLevel\":");
            signalStrength = sig;
            logQueue.Enqueue($"SignalStrength={sig}");
        }

        // Minimal parse: eSense (attention/meditation)
        if (jsonLine.Contains("\"eSense\""))
        {
            int att = Extract(jsonLine, "\"attention\":");
            int med = Extract(jsonLine, "\"meditation\":");

            attentionValue = att;
            meditationValue = med;

            logQueue.Enqueue($"[TGC] Attention={att}, Meditation={med}");
        }

        if (jsonLine.Contains("\"rawEeg\""))
        {
            int raw = Extract(jsonLine, "\"rawEeg\":");
            rawEegValue = raw;
        }

        if (jsonLine.Contains("\"eegPower\""))
        {
            latestEegPower = new EegPower
            {
                delta = Extract(jsonLine, "\"delta\":"),
                theta = Extract(jsonLine, "\"theta\":"),
                lowAlpha = Extract(jsonLine, "\"lowAlpha\":"),
                highAlpha = Extract(jsonLine, "\"highAlpha\":"),
                lowBeta = Extract(jsonLine, "\"lowBeta\":"),
                highBeta = Extract(jsonLine, "\"highBeta\":"),
                lowGamma = Extract(jsonLine, "\"lowGamma\":"),
                midGamma = Extract(jsonLine, "\"midGamma\":")
            };
        }
    }

    int Extract(string s, string key)
    {
        int i = s.IndexOf(key, StringComparison.Ordinal);
        if (i < 0) return -1;
        i += key.Length;

        int j = i;
        while (j < s.Length && (char.IsDigit(s[j]) || s[j] == '-')) j++;

        if (int.TryParse(s.Substring(i, j - i), out var val))
            return val;

        return -1;
    }

    async void OnDestroy()
    {
#if !UNITY_WEBGL || UNITY_EDITOR
        running = false;
        try { stream?.Close(); } catch { }
        try { client?.Close(); } catch { }
#else
        if (ws != null && ws.State == WebSocketState.Open)
        {
            try { await ws.Close(); } catch { }
        }
#endif
    }
}
