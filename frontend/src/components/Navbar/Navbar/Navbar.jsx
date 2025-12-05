import { NavLink, useNavigate } from "react-router-dom";
import { Bar, Inner, Tabs, Right } from "./Navbar.styles";

const PATIENT_LINKS = [
  { to: "/home/patient", label: "Home" },
  { to: "/reports", label: "Reports" },
];

const SPECIALIST_LINKS = [
  { to: "/home/specialist", label: "Home" },
  { to: "/assign", label: "Games" },
  { to: "/reports", label: "Reports" },
];

export default function Navbar() {
  const navigate = useNavigate();
  const userType = sessionStorage.getItem("mm_userType"); // mock auth

  const homePath =
    userType === "specialist" ? "/home/specialist" : "/home/patient";

  const goHome = () => {
    if (userType === "patient") navigate("/home/patient");
    else if (userType === "specialist") navigate("/home/specialist");
    else navigate("/login");
  };

  const logout = () => {
    sessionStorage.removeItem("mm_userType");
    navigate("/login");
  };

  const links =
    userType === "specialist"
      ? SPECIALIST_LINKS
      : PATIENT_LINKS; // default to patient set if anything else

  return (
    <Bar>
      <Inner>
        <a onClick={goHome} style={{ fontWeight: 700, cursor: "pointer" }}>
          MindMetrics
        </a>

        <Tabs>
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) => (isActive ? "active" : "")}
            >
              {link.label}
            </NavLink>
          ))}
        </Tabs>

        <Right>
          <button onClick={logout}>Logout</button>
        </Right>
      </Inner>
    </Bar>
  );
}
