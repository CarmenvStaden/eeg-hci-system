import { useState } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";
import { registerUser } from "../services/auth";

const Card = styled.div`
  max-width: 420px;
  margin: 8vh auto;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.2rem;
`;

export default function Signup() {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [type, setType] = useState("patient");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      await registerUser({
        email,
        username,
        password,
        password2,
        is_doctor: type === "specialist",
        is_patient: type === "patient",
      });

      sessionStorage.setItem("mm_userType", type);
      navigate(type === "patient" ? "/home/patient" : "/home/specialist");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <Card>
      <h2 style={{ marginTop: 0 }}>Sign Up</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleSubmit} style={{ display: "grid", gap: "0.6rem" }}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Confirm Password"
          value={password2}
          onChange={(e) => setPassword2(e.target.value)}
          required
        />
        <label style={{ display: "grid", gap: "0.3rem" }}>
          <span>I am a...</span>
          <select value={type} onChange={(e) => setType(e.target.value)}>
            <option value="patient">Patient</option>
            <option value="specialist">Specialist</option>
          </select>
        </label>
        <button type="submit">Create Account</button>
      </form>
    </Card>
  );
}
