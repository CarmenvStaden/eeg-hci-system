using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System.Collections;

// Sends a GET to /accounts/hello/ endpoint and logs the response text.

public class HealthCheck : MonoBehaviour
{
    // Dev URL:
    [SerializeField]
    private string healthUrl = "http://127.0.0.1:8000/api/accounts/hello/";

    private IEnumerator Start()
    {
        using (var req = UnityWebRequest.Get(healthUrl))
        {
            Debug.Log($"[HealthCheck] Sending GET request to {healthUrl}");
            yield return req.SendWebRequest();

#if UNITY_2020_2_OR_NEWER
            bool ok = req.result == UnityWebRequest.Result.Success && req.responseCode == 200;
#else
            bool ok = !(req.isNetworkError || req.isHttpError) && req.responseCode == 200;
#endif

            if (!ok)
            {
                Debug.LogError($"[HealthCheck] Failed: HTTP {req.responseCode} - {req.error}");
                Debug.LogError(req.downloadHandler.text);
            }
            else
            {
                Debug.Log($"[HealthCheck] Success ({req.responseCode}): {req.downloadHandler.text}");
            }
        }
    }
}
