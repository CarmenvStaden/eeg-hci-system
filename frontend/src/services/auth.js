import { tokenStore } from "./tokenStore";
import { jwtDecode } from "jwt-decode";


// ---------- REGISTER ----------

export async function registerUser({ email, username, password, password2}) {
    const headers = {
        'Content-Type': 'application/json',
    };

    const res = await fetch('/api/accounts/register/', {
        method: 'POST',
        headers,
        body: JSON.stringify({
            email,
            username,
            password,
            password2
        }),
    });

    if (!res.ok) {
        let msg = `HTTP ${res.status}`;
        try {
        const err = await res.json();
        msg += `: ${JSON.stringify(err)}`;
        } catch (_) {}
        throw new Error(msg);
    }

    return res.json();
}

// ---------- LOGIN/LOGOUT ----------

export async function loginUser({ email, password }) {
    const res = await fetch("/api/accounts/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
        let msg = `HTTP ${res.status}`;
        try { msg += `: ${JSON.stringify(await res.json())}`; } catch {}
        throw new Error(msg);
    }

    const data = await res.json(); // expecting { access, refresh }
    if (!data.access || !data.refresh) {
        throw new Error("Login response missing tokens");
    }

    // store token
    tokenStore.set({ access: data.access, refresh: data.refresh });

    // decode the access token to read role info
    // payload.is_doctor and payload.is_patient come from CustomTokenObtainPairSerializer in backend
    const payload = jwtDecode(data.access);

    // string to use on the frontend
    const userType = payload.is_doctor ? "specialist" : "patient";

    // return everything 
    return { ...data, payload, userType };
}

export function logoutUser() {
    tokenStore.clear();
}