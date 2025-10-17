import { Outlet } from "react-router-dom";
import Navbar from "../components/Navbar/Navbar/Navbar";
import { Shell, Content } from "./AppLayout.styles";

export default function AppLayout() {
  return (
    <Shell>
      <Navbar />
      <Content>
        <Outlet />
      </Content>
    </Shell>
  );
}
