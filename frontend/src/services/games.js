// File contains all game-session related API calls

import { authFetch } from "./http";

// ---------- helpers ----------
async function jsonOrThrow(res) {
    if (!res.ok) {
      let msg = `HTTP ${res.status}`;
      try {
        const err = await res.json();
        msg += `: ${JSON.stringify(err)}`;
      } catch {}
      throw new Error(msg);
    }
    return res.json();
  }

// ---------- GAMES ----------

// GET all games (auth optional; if endpoint requires auth, authFetch will attach token)
export async function fetchGames() {
    const res = await authFetch("/api/gamesession/games/");
    return jsonOrThrow(res);
}

// POST create a game (requires auth)
export async function createGame(game) {
    const res = await authFetch("/api/gamesession/games/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(game),
    });
    return jsonOrThrow(res);
}

// ---------- PRESCRIPTIONS ----------

// GET prescriptions (requires auth)
export async function fetchPrescriptions() {
    const res = await authFetch("/api/gamesession/prescriptions/");
    return jsonOrThrow(res);
}

// POST create prescription (requires auth)
export async function createPrescription({ patient, game, notes = "" }) {
    const res = await authFetch("/api/gamesession/prescriptions/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ patient, game, notes }),
    });
    return jsonOrThrow(res);
}
