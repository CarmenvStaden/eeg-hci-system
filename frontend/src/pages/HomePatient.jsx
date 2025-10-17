import styled from "styled-components";

const Card = styled.section`
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1rem;
`;

export default function HomePatient() {
  const assigned = [
    { name: "Treatment A", action: "Play" },
    { name: "Treatment B", action: "Play" },
  ];
  const history = [
    { session: "Session A", date: "10/22/25", game: "Treatment", status: "Pending" },
    { session: "Session B", date: "10/23/25", game: "Full Diagnostic", status: "Complete" },
    { session: "Session C", date: "10/23/25", game: "Baseline", status: "Complete" },
  ];

  return (
    <>
      <h2>Welcome, Patient B!</h2>
      <Card>
        <div style={{display:"flex", justifyContent:"space-between", alignItems:"center"}}>
          <nav style={{display:"flex", gap:"0.6rem"}}>
            <a className="active">Home</a>
            <a>Logout</a>
          </nav>
          <button title="Add">＋</button>
        </div>

        <h3 style={{marginTop:"1rem"}}>Assigned Games:</h3>
        <ul>
          {assigned.map((g)=>(
            <li key={g.name} style={{display:"flex", gap:"0.6rem", alignItems:"center"}}>
              <span>{g.name}</span>
              <a href="/play">{g.action}</a>
            </li>
          ))}
        </ul>

        <h3 style={{marginTop:"1rem"}}>History</h3>
        <table>
          <thead>
            <tr><th>Session</th><th>Date</th><th>Game</th><th>Status</th></tr>
          </thead>
          <tbody>
            {history.map((r)=>(
              <tr key={r.session}>
                <td>{r.session}</td>
                <td>{r.date}</td>
                <td><a href="/reports">{r.game}</a></td>
                <td>{r.status}</td>
              </tr>
            ))}
          </tbody>
        </table>

        <div style={{marginTop:"0.8rem", display:"flex", gap:"0.5rem"}}>
          <button>Export PDF</button>
          <button>Graph View</button>
        </div>
      </Card>
    </>
  );
}
