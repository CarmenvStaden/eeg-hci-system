import { useState } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";
import HealthCheck from "../components/HealthCheck.jsx";
import { loginUser } from "../services/auth";

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
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [type, setType] = useState("patient");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const onSubmit = async () => {
    setError(null);
    try {
      await loginUser({ email, password });
      sessionStorage.setItem("mm_userType", type);
      navigate(type === "patient" ? "/home/patient" : "/home/specialist");
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh", // Full screen height
      }}
    >
      <Card style={{ padding: "2rem", width: "300px", textAlign: "center" }}>
        <h2 style={{ marginTop: 0 }}>Login</h2>
        <div style={{ display: "grid", gap: "0.6rem" }}>
          {error && <p style={{ color: "red" }}>{error}</p>}
          <input
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <label style={{ display: "grid", gap: "0.3rem" }}>
            <span>I am a...</span>
            <select value={type} onChange={(e) => setType(e.target.value)}>
              <option value="patient">Patient</option>
              <option value="specialist">Specialist</option>
            </select>
          </label>
          <div
            style={{
              display: "flex",
              gap: "0.5rem",
              marginTop: "0.2rem",
              alignItems: "center",
              justifyContent: "center", // center the button too
            }}
          >
            <button onClick={onSubmit}>Login</button>
          </div>
          <div
            style={{
              display: "flex",
              gap: "0.5rem",
              marginTop: "0.2rem",
              alignItems: "center",
              justifyContent: "center", // center the link
            }}
          >
            <a href="/signup">Create an account</a>
          </div>
        </div>
      </Card>
    </div>
  );
}
