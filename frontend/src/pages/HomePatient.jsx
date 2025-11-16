// src/pages/HomePatient.jsx
import { useEffect, useMemo, useState } from "react";
import styled from "styled-components";
import { fetchPrescriptions, fetchGames } from "../services/games.js";
import { fetchUsers } from "../services/user.js";

const Card = styled.section`
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1rem;
`;

const PATIENT_ID = 7; // TODO: replace with logged-in patient's id from your auth/profile

function formatDate(iso) {
  try {
    return new Date(iso).toLocaleString();
  } catch {
    return "—";
  }
}

export default function HomePatient() {
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");
  const [prescriptions, setPrescriptions] = useState([]);
  const [games, setGames] = useState([]);
  const [username, setUsername] = useState('')

  useEffect(() => {
    let alive = true;
    async function load() {
      setLoading(true);
      setErr("");
      try {
        const [gamesData, prescData, users] = await Promise.all([
          fetchGames(),
          fetchPrescriptions(),
          fetchUsers(),              
        ]);

        // normalize games (array or paginated)
        const gameList = Array.isArray(gamesData)
          ? gamesData
          : Array.isArray(gamesData?.results)
          ? gamesData.results
          : [];

        const prescList = Array.isArray(prescData) ? prescData : [];

        // find patient by id
        const patient = Array.isArray(users)
          ? users.find((u) => u.id === PATIENT_ID)
          : null;

        if (!alive) return;

        setGames(gameList);
        setPrescriptions(prescList);
        if (patient?.username) setUsername(patient.username);
      } catch (e) {
        console.error(e);
        const msg = String(e?.message || "Failed to load");
        if (msg.includes("HTTP 401")) {
          setErr("Unauthorized. Please sign in again.");
        } else {
          setErr(msg);
        }
      } finally {
        if (alive) setLoading(false);
      }
    }
    load();
    return () => {
      alive = false;
    };
  }, []);


  // Build index to map game id -> name/link
  const gameById = useMemo(() => {
    const map = new Map();
    for (const g of games) map.set(g.id, g);
    return map;
  }, [games]);

  // Filter to THIS patient's prescriptions
  const myPrescriptions = useMemo(
    () =>
      prescriptions
        .filter((p) => p.patient === PATIENT_ID)
        .sort(
          (a, b) =>
            new Date(b.created_at || 0).valueOf() -
            new Date(a.created_at || 0).valueOf()
        ),
    [prescriptions]
  );

  const assignedActive = useMemo(
    () => myPrescriptions.filter((p) => Boolean(p.active)),
    [myPrescriptions]
  );

  if (loading) return <div>Loading…</div>;
  if (err) return <div>Error: {err}</div>;

  return (
    <>
      <h2>Welcome, {username || 'Patient'}!</h2>
      <Card>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <h4>Request Treatment</h4>
          <button title="Add">＋</button>
        </div>

        <h3 style={{ marginTop: "1rem" }}>Assigned Games:</h3>
        {assignedActive.length === 0 ? (
          <p>No active prescriptions.</p>
        ) : (
          <ul>
            {assignedActive.map((p) => {
              const g = gameById.get(p.game);
              const name = g?.name ?? `Game #${p.game}`;
              // TODO: Adjust play link to real game-playing route
              //const playHref = `/play/${p.game}`;
              // HARD-CODED LINK TO UNITY WEBGL BUILD
              const playHref = "/game/index.html";
              return (
                <li
                  key={`rx-${p.id}`}
                  style={{ display: "flex", gap: "0.6rem", alignItems: "center" }}
                >
                  <span>{name}</span>
                  <a href={playHref}>Play</a>
                </li>
              );
            })}
          </ul>
        )}

        <h3 style={{ marginTop: "1rem" }}>History</h3>
        {myPrescriptions.length === 0 ? (
          <p>No history yet.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Prescription</th>
                <th>Date</th>
                <th>Game</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {myPrescriptions.map((p) => {
                const g = gameById.get(p.game);
                const gameName = g?.name ?? `Game #${p.game}`;
                // TODO: later track completion on the prescription, swap in real field.
                const status = p.active ? "Pending" : "Inactive";
                return (
                  <tr key={`row-${p.id}`}>
                    <td>{`Rx #${p.id}`}</td>
                    <td>{formatDate(p.created_at)}</td>
                    <td>
                      {/* Adjust report*/}
                      <a href={`/reports/${p.id}`}>{gameName}</a>
                    </td>
                    <td>{status}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}

        <div style={{ marginTop: "0.8rem", display: "flex", gap: "0.5rem" }}>
          <button>Export PDF</button>
          <button>Graph View</button>
        </div>
      </Card>
    </>
  );
}
