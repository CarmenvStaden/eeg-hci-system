// src/components/CreateGameTest.jsx
import { useState } from 'react';
import { createGame } from '../services/games.js';

export default function CreateGameTest() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleCreate = async () => {
    setError('');
    try {
      const newGame = await createGame({
        name: 'Full Diagnostic',
        description: 'Game consists of 6 levels, testing the a full EEG range.',
      });
      console.log('Created game:', newGame);
      setResult(newGame);
    } catch (err) {
      console.error(err);
      setError(err.message);
    }
  };

  return (
    <div>
      <button onClick={handleCreate}>
        Create "Full Diagnostic"
      </button>

      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {result && (
        <pre>{JSON.stringify(result, null, 2)}</pre>
      )}
    </div>
  );
}
