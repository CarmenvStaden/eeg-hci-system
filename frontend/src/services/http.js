// Adds Authorization: Bearer <access>, and if it gets 401, it tries to refresh with { refresh } (no cookies needed for now).
// src/services/http.js
import { tokenStore, isJwtExpired } from "./tokenStore";

async function refreshAccessToken() {
    const { refresh } = tokenStore.get();
    if (!refresh) throw new Error("No refresh token");

    const res = await fetch(`/api/accounts/token/refresh/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh }),
    });

    if (!res.ok) {
        tokenStore.clear();
        throw new Error("Failed to refresh");
    }

    const data = await res.json(); // expecting { access: "..." }
    if (!data.access) throw new Error("Malformed refresh response");
    tokenStore.setAccess(data.access);
    return data.access;
}

export async function authFetch(path, init = {}) {
    const url = path.startsWith("http") ? path : `${path}`;
    const headers = new Headers(init.headers || { "Content-Type": "application/json" });

    let { access } = tokenStore.get();
    if (!access || isJwtExpired(access)) {
        try {
        access = await refreshAccessToken();
        } catch {
        access = null; // will likely 401
        }
    }

    if (access) headers.set("Authorization", `Bearer ${access}`);

    let res = await fetch(url, { ...init, headers });

    if (res.status === 401) {
    tokenStore.clear();
    }

    return res;
}
