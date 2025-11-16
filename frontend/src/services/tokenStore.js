const KEY = "authTokens"; // { access, refresh }

export const tokenStore = {
    get() {
        const raw = sessionStorage.getItem(KEY);
        return raw ? JSON.parse(raw) : { access: null, refresh: null };
    },
    set({ access, refresh }) {
        sessionStorage.setItem(KEY, JSON.stringify({ access, refresh }));
    },
    setAccess(access) {
        const cur = tokenStore.get();
        sessionStorage.setItem(KEY, JSON.stringify({ ...cur, access }));
    },
    clear() {
        sessionStorage.removeItem(KEY);
    },
    hasRefresh() {
        const { refresh } = tokenStore.get();
        return Boolean(refresh);
    },
};

export function isJwtExpired(token) {
    if (!token) return true;
    const [, payload] = token.split(".");
    if (!payload) return true;
    try {
        const json = JSON.parse(atob(payload.replace(/-/g, "+").replace(/_/g, "/")));
        const now = Math.floor(Date.now() / 1000);
        return typeof json.exp === "number" ? json.exp <= now : true;
    } catch {
        return true;
    }
}
