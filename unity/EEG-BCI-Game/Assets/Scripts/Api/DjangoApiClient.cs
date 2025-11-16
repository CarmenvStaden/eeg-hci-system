// utility to POST JSON with a Bearer token and return text/HTTP code
using System.Collections;
using System.Collections.Generic;
using System.Text;
using UnityEngine;
using UnityEngine.Networking;

public class DjangoApiClient : MonoBehaviour
{
    public static IEnumerator PostJson(string url, string jsonBody, string bearerToken,
                                         System.Action<bool, long, string> done)
    {
        using (var req = new UnityWebRequest(url, UnityWebRequest.kHttpVerbPOST))
        {
            byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonBody ?? "{}");
            req.uploadHandler = new UploadHandlerRaw(bodyRaw);
            req.downloadHandler = new DownloadHandlerBuffer();
            req.SetRequestHeader("Content-Type", "application/json");
            if (!string.IsNullOrEmpty(bearerToken))
                req.SetRequestHeader("Authorization", "Bearer " + bearerToken);

            yield return req.SendWebRequest();

#if UNITY_2020_2_OR_NEWER
            bool ok = req.result == UnityWebRequest.Result.Success && (req.responseCode >= 200 && req.responseCode < 300);
#else
            bool ok = !(req.isHttpError || req.isNetworkError) && (req.responseCode >= 200 && req.responseCode < 300);
#endif
            done?.Invoke(ok, req.responseCode, req.downloadHandler?.text);
        }
    }
}
