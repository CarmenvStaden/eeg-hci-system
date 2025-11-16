// src/pages/Games.jsx
import { useEffect, useState, useCallback } from 'react';
import {
  fetchGames,
  fetchPrescriptions,
  createPrescription,
} from '../services/games.js';

//TODO : replace with real patient ID after auth is done
const TEST_PATIENT_ID = 7;

export default function Games() {
  const [games, setGames] = useState([]);
  const [prescriptions, setPrescriptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [assigningId, setAssigningId] = useState(null);

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError('');
      try {
        const [gamesData, prescriptionsData] = await Promise.all([
          fetchGames(),
          fetchPrescriptions(),
        ]);

        const list = Array.isArray(gamesData)
          ? gamesData
          : Array.isArray(gamesData.results)
          ? gamesData.results
          : [];

        setGames(list);
        setPrescriptions(Array.isArray(prescriptionsData) ? prescriptionsData : []);
      } catch (err) {
        console.error(err);
        // Friendly 401 message
        if (String(err.message).includes('HTTP 401')) {
          setError('Unauthorized. Please sign in again.');
        } else {
          setError(err.message || 'Failed to load data');
        }
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const findPrescriptionForGame = useCallback(
    (gameId) =>
      prescriptions.find(
        (p) => p.game === gameId && p.patient === TEST_PATIENT_ID
      ),
    [prescriptions]
  );

  const handleAssign = async (gameId) => {
    setAssigningId(gameId);
    try {
      const newPresc = await createPrescription({
        patient: TEST_PATIENT_ID,
        game: gameId,
        notes: '',
      });
      setPrescriptions((prev) => [newPresc, ...prev]);
    } catch (err) {
      console.error(err);
      if (String(err.message).includes('HTTP 401')) {
        alert('Your session expired. Please sign in again.');
      } else {
        alert(`Failed to assign game: ${err.message}`);
      }
    } finally {
      setAssigningId(null);
    }
  };

  if (loading) return <div>Loading…</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <>
      <h2>Assign Games to Test Patient</h2>
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
                ? 'Pending'
                : 'Inactive'
              : '—';
            const date = isAssigned
              ? new Date(presc.created_at).toLocaleString()
              : '—';

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
                      disabled={assigningId === game.id}
                      aria-busy={assigningId === game.id}
                    >
                      {assigningId === game.id ? 'Assigning…' : 'Assign'}
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
