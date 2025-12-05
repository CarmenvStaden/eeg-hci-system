// src/pages/HomePatient.jsx
import { useEffect, useMemo, useState } from "react";
import styled from "styled-components";
import { fetchPrescriptions, fetchGames, fetchSessions } from "../services/games.js";

const Card = styled.section`
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1rem;
`;

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
  const [sessions, setSessions] = useState([]); 
  const [username, setUsername] = useState('')

  useEffect(() => {
    let alive = true;
    async function load() {
      setLoading(true);
      setErr("");
      try {
        const [gamesData, prescData, sessData] = await Promise.all([
          fetchGames(),
          fetchPrescriptions(),
          fetchSessions(),      
        ]);

        // normalize games (array or paginated)
        const gameList = Array.isArray(gamesData)
          ? gamesData
          : Array.isArray(gamesData?.results)
          ? gamesData.results
          : [];

        const prescList = Array.isArray(prescData) ? prescData : [];
        const sessionList = Array.isArray(sessData) ? sessData : []; 

        if (!alive) return;

        setGames(gameList);
        setPrescriptions(prescList);
        setSessions(sessionList); 
        // if (patient?.username) setUsername(patient.username);
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

  // Filter patient prescriptions
  const myPrescriptions = useMemo(
    () =>
      [...prescriptions].sort(
        (a, b) =>
          new Date(b.created_at || 0).valueOf() -
          new Date(a.created_at || 0).valueOf()
      ),
    [prescriptions]
  );

  // Sorted sessions (newest first)
  const mySessions = useMemo(
    () =>
      [...sessions].sort(
        (a, b) =>
          new Date(b.start_time || 0).valueOf() -
          new Date(a.start_time || 0).valueOf()
      ),
    [sessions]
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
        <h3 style={{ marginTop: "1rem" }}>Assigned Games:</h3>
        {assignedActive.length === 0 ? (
          <p>No active prescriptions.</p>
        ) : (
          <ul>
            {assignedActive.map((p) => {
              const g = gameById.get(p.game);
              const name = g?.name ?? `Game #${p.game}`;
              // TODO: Adjust play link to real game-playing route
              // HARD-CODED LINK TO UNITY WEBGL BUILD of attention game only
              const playHref = `/game/index.html?game_id=${p.game}&prescription_id=${p.id}`;
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
        {mySessions.length === 0 ? (
          <p>No sessions yet.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Session</th>
                <th>Date</th>
                <th>Game</th>
                <th>Prescription</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {mySessions.map((s) => {
                const g = gameById.get(s.game);
                const gameName = g?.name ?? `Game #${s.game}`;
                const prescLabel = s.prescription ? `Rx #${s.prescription}` : "—";
                const status = s.end_time ? "Completed" : "In progress";

                return (
                  <tr key={`sess-${s.id}`}>
                    <td>{`Session #${s.id}`}</td>
                    <td>{formatDate(s.start_time)}</td>
                    <td>
                      {/* TODO: if reports are session-based, switch to /reports/sessions/${s.id} */}
                      {s.prescription ? (
                        <a href={`/reports/${s.prescription}`}>{gameName}</a>
                      ) : (
                        gameName
                      )}
                    </td>
                    <td>{prescLabel}</td>
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
