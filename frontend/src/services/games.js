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

// GET all games
export async function fetchGames() {
    const res = await authFetch("/api/gamesession/games/");
    return jsonOrThrow(res);
}

// // Legacy
// // POST create a game (requires auth)
// export async function createGame(game) {
//     const res = await authFetch("/api/gamesession/games/", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify(game),
//     });
//     return jsonOrThrow(res);
// }

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

// ---------- SESSIONS ----------

// GET my (patient) sessions (requires auth)
export async function fetchSessions() {
    const res = await authFetch("/api/gamesession/sessions/me/");
    return jsonOrThrow(res);
}

export async function getSessionsByUserId(patientId) {
  const res = await authFetch(
    `/api/gamesession/sessions/${patientId}/`
  );
  if (!res.ok) {
    throw new Error(
      `Failed to fetch sessions for patient ${patientId}: HTTP ${res.status}`
    );
  }
  return res.json();
}

// For patients looking at their own EEG data
export async function getMyEegBySession(sessionId) {
  const res = await authFetch(
    `/api/dashboards/eeg/get_my_eeg_by_session/${sessionId}/`
  );
  if (!res.ok) {
    throw new Error(
      `Failed to fetch my EEG for session ${sessionId}: HTTP ${res.status}`
    );
  }
  return res.json();
}

// For doctors looking at a specific patient's session
export async function getEegBySessionDoctor(patientId, sessionId) {
  const res = await authFetch(
    `/api/dashboards/eeg/get_eeg_by_session_doctor/${patientId}/${sessionId}/`
  );
  if (!res.ok) {
    throw new Error(
      `Failed to fetch EEG for patient ${patientId} session ${sessionId}: HTTP ${res.status}`
    );
  }
  return res.json();
}