import { NavLink, useNavigate } from "react-router-dom";
import { Bar, Inner, Tabs, Right } from "./Navbar.styles";

export default function Navbar() {
  const navigate = useNavigate();
  const userType = sessionStorage.getItem("mm_userType"); // mock auth
  const homePath = userType === "specialist" ? "/home/specialist" : "/home/patient";

  const goHome = () => {
    if (userType === "patient") navigate("/home/patient");
    else if (userType === "specialist") navigate("/home/specialist");
    else navigate("/login");
  };

  const logout = () => {
    sessionStorage.removeItem("mm_userType");
    navigate("/login");
  };

  return (
    <Bar>
      <Inner>
        <a onClick={goHome} style={{ fontWeight: 700, cursor: "pointer" }}>
          MindMetrics
        </a>

        <Tabs>
        <NavLink
            to={homePath}
            className={({ isActive }) => (isActive ? "active" : "")}
        >
            Home
        </NavLink>
        <NavLink to="/games" className={({ isActive }) => (isActive ? "active" : "")}>
            Games
        </NavLink>
        <NavLink to="/reports" className={({ isActive }) => (isActive ? "active" : "")}>
            Reports
        </NavLink>
        </Tabs>

        <Right>
          <button onClick={logout}>Logout</button>
        </Right>
      </Inner>
    </Bar>
  );
}
