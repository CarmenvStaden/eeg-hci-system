// src/pages/Assign.jsx
import { useEffect, useState, useCallback } from 'react';
import {
  fetchGames,
  fetchPrescriptions,
  createPrescription,
} from '../services/games.js';
import { listPatients } from "../services/specialistDash.js"; 

export default function Assign() {
    const [games, setGames] = useState([]);
    const [prescriptions, setPrescriptions] = useState([]);
    const [patients, setPatients] = useState([]);     
    const [selectedPatientId, setSelectedPatientId] = useState(null); 

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [assigningId, setAssigningId] = useState(null);


    useEffect(() => {
        async function loadPatientsAndGames() {
        setLoading(true);
        setError("");
        try {
            // Load patients and games in parallel
            const [patientsData, gamesData] = await Promise.all([
            listPatients(),
            fetchGames(),
            ]);

            const patientsList = Array.isArray(patientsData) ? patientsData : [];
            setPatients(patientsList);

            const list = Array.isArray(gamesData)
            ? gamesData
            : Array.isArray(gamesData.results)
            ? gamesData.results
            : [];
            setGames(list);

            // Choose a default patient (first one) if none selected
            if (patientsList.length > 0 && !selectedPatientId) {
            setSelectedPatientId(patientsList[0].id);
            }
        } catch (err) {
            console.error(err);
            if (String(err.message).includes("HTTP 401")) {
            setError("Unauthorized. Please sign in again.");
            } else {
            setError(err.message || "Failed to load data");
            }
        } finally {
            setLoading(false);
        }
        }

        loadPatientsAndGames();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    // load prescriptions whenever the selected patient changes
    useEffect(() => {
        if (!selectedPatientId) return;

        async function loadPrescriptionsForPatient() {
        try {
            setError("");
            const prescriptionsData = await fetchPrescriptions(selectedPatientId);
            setPrescriptions(
            Array.isArray(prescriptionsData) ? prescriptionsData : []
            );
        } catch (err) {
            console.error(err);
            if (String(err.message).includes("HTTP 401")) {
            setError("Unauthorized. Please sign in again.");
            } else {
            setError(err.message || "Failed to load prescriptions");
            }
        }
        }

        loadPrescriptionsForPatient();
    }, [selectedPatientId]);

    // perscription helpers
    const findPrescriptionForGame = useCallback(
        (gameId) =>
        prescriptions.find(
            (p) => p.game === gameId && p.patient === selectedPatientId
        ),
        [prescriptions, selectedPatientId]
    );

  const handleAssign = async (gameId) => {
    if (!selectedPatientId) {
      alert("Please select a patient first.");
      return;
    }

    setAssigningId(gameId);
    try {
      const newPresc = await createPrescription({
        patient: selectedPatientId,
        game: gameId,
        notes: "",
      });
      setPrescriptions((prev) => [newPresc, ...prev]);
    } catch (err) {
      console.error(err);
      if (String(err.message).includes("HTTP 401")) {
        alert("Your session expired. Please sign in again.");
      } else {
        alert(`Failed to assign game: ${err.message}`);
      }
    } finally {
      setAssigningId(null);
    }
  };

  if (loading) return <div>Loading…</div>;
  if (error) return <div>Error: {error}</div>;

  const selectedPatient = patients.find((p) => p.id === selectedPatientId);

  return (
    <>
      <h2>Assign Games</h2>

      <div style={{ marginBottom: "1rem" }}>
        <label>
          Patient:&nbsp;
          <select
            value={selectedPatientId || ""}
            onChange={(e) =>
              setSelectedPatientId(
                e.target.value ? Number(e.target.value) : null
              )
            }
          >
            <option value="">Select a patient</option>
            {patients.map((p) => (
              <option key={p.id} value={p.id}>
                {p.username} ({p.email})
              </option>
            ))}
          </select>
        </label>
      </div>

      {selectedPatient && (
        <p style={{ marginBottom: "1rem" }}>
          <strong>{selectedPatient.username}</strong>
        </p>
      )}

      <table>
        <thead>
          <tr>
            <th>Game</th>
            <th>Date</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {games.map((game) => {
            const presc = findPrescriptionForGame(game.id);
            const isAssigned = !!presc;
            const status = isAssigned
              ? presc.active
                ? "Pending"
                : "Inactive"
              : "—";
            const date = isAssigned
              ? new Date(presc.created_at).toLocaleString()
              : "—";

            return (
              <tr key={game.id}>
                <td>{game.name}</td>
                <td>{date}</td>
                <td>{status}</td>
                <td>
                  {isAssigned ? (
                    <button disabled>Assigned</button>
                  ) : (
                    <button
                      onClick={() => handleAssign(game.id)}
                      disabled={assigningId === game.id || !selectedPatientId}
                      aria-busy={assigningId === game.id}
                    >
                      {assigningId === game.id ? "Assigning…" : "Assign"}
                    </button>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </>
  );
}

