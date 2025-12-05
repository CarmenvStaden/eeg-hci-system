import { Routes, Route, Navigate } from "react-router-dom";
import GlobalStyles from "./styles/GlobalStyles";
import AppLayout from "./layout/AppLayout";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import HomePatient from "./pages/HomePatient";
import HomeSpecialist from "./pages/HomeSpecialist";
import Assign from "./pages/Assign";
import Reports from "./pages/Reports";
import Games from "./pages/Games";
//import Play from "./pages/Play";
import NotFound from "./pages/NotFound";
import GamePage from "./pages/GamePage.jsx";

export default function App() {
  return (
    <>
      <GlobalStyles />
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        {/* App pages with shared navbar/layout */}
        <Route element={<AppLayout />}>
          <Route path="/home/patient" element={<HomePatient />} />
          <Route path="/home/specialist" element={<HomeSpecialist />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/assign" element={<Assign />} />
          <Route path="/games" element={<Games />} />
          <Route path="/play" element={<GamePage/>} />
        </Route>

        <Route path="*" element={<NotFound />} />
      </Routes>
    </>
  );
}
