import styled from "styled-components";
// This is a placeholder component for the game playing interface
// Unity integration will be implemented here in the future


const Canvas = styled.div`
  height: 65vh;
  border-radius: 16px;
  border: 1px solid var(--border);
  background: linear-gradient(180deg, #d6f0ff, #d0c7ff 60%, #f2d7ff);
  display: grid;
  place-items: center;
  font-weight: 600;
  letter-spacing: 0.5px;
`;

export default function Play() {
  return (
    <>
      <h2>Game Player</h2>
      <Canvas>Game canvas placeholder</Canvas>
    </>
  );
}
