export default function GamePage() {
  return (
    <div style={{ width: "100vw", height: "100vh", margin: 0, padding: 0 }}>
      <iframe
        src="/game/index.html"
        title="Unity Game"
        style={{ width: "100%", height: "100%", border: "none" }}
      />
    </div>
  );
}
