export default function Reports() {
  const sessions = [
    { session: "Session A", date: "11/12/25", game: "Treatment", status: "Pending" },
    { session: "Session B", date: "10/29/25", game: "Full Diagnostic", status: "Complete" },
    { session: "Session C", date: "10/23/25", game: "Baseline", status: "Complete" },
  ];
  return (
    <>
      <h2>Reports — Test Patient</h2>
      <table>
        <thead>
          <tr><th>Session</th><th>Date</th><th>Game</th><th>Status</th></tr>
        </thead>
        <tbody>
          {sessions.map(s=>(
            <tr key={s.session}>
              <td>{s.session}</td>
              <td>{s.date}</td>
              <td><a href="/reports">{s.game}</a></td>
              <td>{s.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div style={{marginTop:"0.8rem", display:"flex", gap:"0.5rem"}}>
        <button>Export PDF</button>
        <button>Graph View</button>
      </div>
    </>
  );
}
