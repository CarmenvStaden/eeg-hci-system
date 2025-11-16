import styled from "styled-components";

const Card = styled.section`
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1rem;
`;

export default function HomeSpecialist() {
  const patients = [
    { name: "Patient A", caseId: "#C-125", status: "Complete" },
    { name: "Patient B", caseId: "#C-317", status: "Pending" },
    { name: "Test Patient", caseId: "#C-217", status: "Complete" },
  ];

  return (
    <>
      <h2>Welcome, Specialist!</h2>
      <Card>
        <div style={{display:"flex", justifyContent:"space-between", alignItems:"center"}}>
          <div>Add / Accept Patient</div>
          <button title="Add">＋</button>
        </div>

        <table style={{marginTop:"1rem"}}>
          <thead>
            <tr><th>Patient</th><th>Case</th><th>Status</th><th>Actions</th></tr>
          </thead>
          <tbody>
            {patients.map(p=>(
              <tr key={p.name}>
                <td>{p.name}</td>
                <td>{p.caseId}</td>
                <td>{p.status}</td>
                <td style={{display:"flex", gap:"0.5rem"}}>
                  <a href="/reports">View</a>
                  <a href="/games">Assign</a>
                  <button>⋯</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </>
  );
}
