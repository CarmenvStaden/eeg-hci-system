// src/components/Games/GamesList.jsx
import { useEffect, useState } from 'react';
import { fetchGames } from '../../services/games.js';

export default function GamesList() {
  const [games, setGames] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchGames()
      .then(data => {
        const list = Array.isArray(data) ? data : data.results ?? [];
        const adapted = list.map(game => ({
          id: game.id,
          name: game.name,
          date: '—',
          status: 'Assign',
        }));
        setGames(adapted);
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading games…</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <tbody>
      {games.length === 0 ? (
        <tr><td colSpan="4">No games found.</td></tr>
      ) : (
        games.map(g => (
          <tr key={g.id ?? g.name}>
            <td>{g.name}</td>
            <td>{g.date}</td>
            <td>{g.status === 'Pending' ? 'Pending' : '—'}</td>
            <td><button>{g.status === 'Pending' ? 'Remove' : 'Assign'}</button></td>
          </tr>
        ))
      )}
    </tbody>
  );
}
