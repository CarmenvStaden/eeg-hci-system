import { useNavigate } from "react-router-dom";
import styled from "styled-components";

const Card = styled.div`
  max-width: 380px;
  margin: 8vh auto;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.2rem;
  box-shadow: 0 8px 20px rgba(0,0,0,0.04);
`;

export default function Login() {
  const navigate = useNavigate();

  const loginAs = (type) => {
    sessionStorage.setItem("mm_userType", type);
    navigate(type === "patient" ? "/home/patient" : "/home/specialist");
  };

  return (
    <Card>
      <h2 style={{marginTop: 0}}>Login</h2>
      <div style={{display:"grid", gap:"0.6rem"}}>
        <input placeholder="Username" />
        <input type="password" placeholder="Password" />
        <div style={{display:"flex", gap:"0.5rem", marginTop:"0.2rem"}}>
          <button onClick={() => loginAs("patient")}>Login as Patient</button>
          <button onClick={() => loginAs("specialist")}>Login as Specialist</button>
        </div>
        <a href="/signup">Create an account</a>
      </div>
    </Card>
  );
}
