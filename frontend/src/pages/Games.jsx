export default function Games() {
  const games = [
    { name: "Attention", date: "10/29/25", status: "Pending" },
    { name: "Full Diagnostic", date: "10/29/25", status: "Assign" },
    { name: "Baseline", date: "10/23/25", status: "Assign" },
  ];
  return (
    <>
      <h2>Assign Games to Patient B</h2>
      <table>
        <thead>
          <tr><th>Game</th><th>Date</th><th>Status</th><th>Action</th></tr>
        </thead>
        <tbody>
          {games.map(g=>(
            <tr key={g.name}>
              <td>{g.name}</td>
              <td>{g.date}</td>
              <td>{g.status === "Pending" ? "Pending" : "—"}</td>
              <td><button>{g.status === "Pending" ? "Remove" : "Assign"}</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}
