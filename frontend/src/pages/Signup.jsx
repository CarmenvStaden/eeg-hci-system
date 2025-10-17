import { useState } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";

const Card = styled.div`
  max-width: 420px;
  margin: 8vh auto;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.2rem;
`;

export default function Signup() {
  const [type, setType] = useState("patient");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    sessionStorage.setItem("mm_userType", type);
    navigate(type === "patient" ? "/home/patient" : "/home/specialist");
  };

  return (
    <Card>
      <h2 style={{marginTop:0}}>Sign Up</h2>
      <form onSubmit={handleSubmit} style={{display:"grid", gap:"0.6rem"}}>
        <input placeholder="Username" required />
        <input type="password" placeholder="Password" required />
        <input type="password" placeholder="Confirm Password" required />
        <label style={{display:"grid", gap:"0.3rem"}}>
          <span>I am a...</span>
          <select value={type} onChange={e=>setType(e.target.value)}>
            <option value="patient">Patient</option>
            <option value="specialist">Specialist</option>
          </select>
        </label>
        <button type="submit">Create Account</button>
      </form>
    </Card>
  );
}
