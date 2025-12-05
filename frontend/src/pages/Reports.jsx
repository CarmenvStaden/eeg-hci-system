// TODO: fix page broken for specialists 
import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, CartesianGrid, ResponsiveContainer,  } from "recharts";
import jsPDF from "jspdf";
import { fetchSessions, getSessionsByUserId, getEegBySessionDoctor } from "../services/games.js";

export default function Reports({ isDoctor = false, patientId, patientName }) {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedSessionId, setSelectedSessionId] = useState(null);

  const [graphData, setGraphData] = useState([]);   // EEG readings for chart
  const [graphOpen, setGraphOpen] = useState(false);
  const [graphLoading, setGraphLoading] = useState(false);

  // Fetch sessions depending on role
  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        setError(null);

        const data = isDoctor
          ? await getSessionsByUserId(patientId)
          : await fetchSessions();

        setSessions(data);
      } catch (err) {
        setError(err.message || "Failed to load sessions");
      } finally {
        setLoading(false);
      }
    }

    if (!isDoctor || (isDoctor && patientId != null)) {
      load();
    }
  }, [isDoctor, patientId]);

  // Helper to convert API session → display row
  const displayRows = sessions.map((s, index) => {
    const hasEeg = s.eeg_readings && s.eeg_readings.length > 0;

    const date =
      s.start_time
        ? new Date(s.start_time).toLocaleDateString("en-US", {
            month: "2-digit",
            day: "2-digit",
            year: "2-digit",
          })
        : "—";

    const gameLabel = `Game ${s.game}`; // TODO: map to real name later

    return {
      id: s.id,
      label: `Session ${index + 1}`,
      date,
      game: gameLabel,
      status: hasEeg ? "Complete" : "Pending",
    };
  });

  function transformEegToChartData(eegReadings) {
    // If data is dense downsample later
    return eegReadings.map((r, idx) => ({
      index: idx + 1,
      time: new Date(r.timestamp).toLocaleTimeString("en-US", {
        hour12: false,
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      }),
      attention: r.attention,
      meditation: r.meditation,
    }));
  }

  async function fetchEegDataForSession(sessionId) {
    if (!isDoctor) {
      // PATIENT: use the EEG readings already embedded in the session object
      const session = sessions.find((s) => s.id === sessionId);
      return session?.eeg_readings || [];
    } else {
      // DOCTOR: use the doctor endpoint
      const eegData = await getEegBySessionDoctor(patientId, sessionId);
      return eegData;
    }
  }

  async function handleGraphView() {
    if (!selectedSessionId) return;

    try {
      setGraphLoading(true);
      setGraphOpen(true); // open modal so spinner shows

      const eegData = await fetchEegDataForSession(selectedSessionId);
      const chartData = transformEegToChartData(eegData);
      setGraphData(chartData);
    } catch (err) {
      console.error(err);
      alert("Failed to load EEG data for graph view.");
      setGraphOpen(false);
    } finally {
      setGraphLoading(false);
    }
  }

  function computeEegStats(eegReadings) {
    if (!eegReadings.length) {
      return {
        count: 0,
        avgAttention: 0,
        avgMeditation: 0,
      };
    }

    const count = eegReadings.length;

    const sumAttention = eegReadings.reduce((sum, r) => sum + (r.attention || 0), 0);
    const sumMeditation = eegReadings.reduce((sum, r) => sum + (r.meditation || 0), 0);

    return {
      count,
      avgAttention: sumAttention / count,
      avgMeditation: sumMeditation / count,
    };
  }

  async function handleExportPdf() {
    if (!selectedSessionId) return;

    try {
      const eegData = await fetchEegDataForSession(selectedSessionId);
      const stats = computeEegStats(eegData);

      // Find the session info for better labeling
      const session = sessions.find((s) => s.id === selectedSessionId);
      const start = session?.start_time ? new Date(session.start_time) : null;
      const end = session?.end_time ? new Date(session.end_time) : null;

      const doc = new jsPDF();

      // Title
      doc.setFontSize(16);
      doc.text("EEG Session Report", 20, 20);

      // Basic info
      doc.setFontSize(12);
      doc.text(`Session ID: ${selectedSessionId}`, 20, 35);

      if (isDoctor) {
        doc.text(`Patient ID: ${patientId}`, 20, 42);
      }

      if (start) {
        doc.text(`Start Time: ${start.toLocaleString()}`, 20, 50);
      }
      if (end) {
        doc.text(`End Time: ${end.toLocaleString()}`, 20, 58);
      }

      doc.text(`Number of EEG samples: ${stats.count}`, 20, 70);
      doc.text(`Average Attention: ${stats.avgAttention.toFixed(2)}`, 20, 82);
      doc.text(`Average Meditation: ${stats.avgMeditation.toFixed(2)}`, 20, 90);

      const filename = isDoctor
        ? `eeg_report_patient_${patientId}_session_${selectedSessionId}.pdf`
        : `eeg_report_session_${selectedSessionId}.pdf`;

      doc.save(filename);
    } catch (err) {
      console.error(err);
      alert("Failed to export PDF.");
    }
  }

  const title = isDoctor
    ? `Reports — ${patientName || `Patient #${patientId}`}`
    : "Reports — Test Patient"; // or "Reports — My Sessions"

  if (loading) return <p>Loading sessions…</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!displayRows.length) return <p>No sessions found.</p>;

  return (
    <>
      <h2>{title}</h2>

      <table>
        <thead>
          <tr>
            <th>Session</th>
            <th>Date</th>
            <th>Game</th>
            <th>Status</th>
            <th>Select</th>
          </tr>
        </thead>
        <tbody>
          {displayRows.map((row) => (
            <tr key={row.id}>
              <td>{row.label}</td>
              <td>{row.date}</td>
              <td>
                {/* Later route to a detailed session page */}
                <a href={`/reports/session/${row.id}`}>{row.game}</a>
              </td>
              <td>{row.status}</td>
              <td>
                <input
                  type="radio"
                  name="selectedSession"
                  checked={selectedSessionId === row.id}
                  onChange={() => setSelectedSessionId(row.id)}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div style={{ marginTop: "0.8rem", display: "flex", gap: "0.5rem" }}>
        <button onClick={handleExportPdf} disabled={!selectedSessionId}>
          Export PDF
        </button>
        <button onClick={handleGraphView} disabled={!selectedSessionId}>
          Graph View
        </button>
      </div>

      {/* Graph Modal */}
      {graphOpen && (
        <div
          style={{
            position: "fixed",
            inset: 0,
            backgroundColor: "rgba(0,0,0,0.4)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 999,
          }}
          onClick={() => setGraphOpen(false)}
        >
          <div
            style={{
              background: "white",
              padding: "1rem",
              borderRadius: "8px",
              minWidth: "70vw",
              minHeight: "50vh",
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.5rem" }}>
              <h3 style={{ margin: 0 }}>EEG Graph — Session {selectedSessionId}</h3>
              <button onClick={() => setGraphOpen(false)}>Close</button>
            </div>

            {graphLoading ? (
              <p>Loading EEG data…</p>
            ) : graphData.length === 0 ? (
              <p>No EEG data available for this session.</p>
            ) : (
              <div style={{ width: "100%", height: 400 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={graphData}
                    margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="attention" dot={false} />
                    <Line type="monotone" dataKey="meditation" dot={false} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
}