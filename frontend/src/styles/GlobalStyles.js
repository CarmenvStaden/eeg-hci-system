import { createGlobalStyle } from "styled-components";

const GlobalStyles = createGlobalStyle`
  :root {
    --brand: #2a8cff;
    --brand-2: #0b63ce;
    --bg: #f6f8fb;
    --card: #ffffff;
    --text: #0f172a;
    --muted: #64748b;
    --border: #e5e7eb;
    --success: #10b981;
    --warning: #f59e0b;
  }

  * { box-sizing: border-box; }
  html, body, #root { height: 100%; }
  body {
    margin: 0;
    font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
    color: var(--text);
    background: var(--bg);
  }

  a { color: var(--brand); text-decoration: none; }
  a:hover { text-decoration: underline; }

  button {
    cursor: pointer;
    border: 1px solid var(--border);
    background: var(--brand);
    color: white;
    padding: 0.55rem 0.9rem;
    border-radius: 10px;
  }

  input, select {
    border: 1px solid var(--border);
    padding: 0.5rem 0.6rem;
    border-radius: 8px;
    background: white;
  }

  table {
    width: 100%;
    border-collapse: collapse;
  }
  th, td {
    padding: 10px;
    border-bottom: 1px solid var(--border);
    text-align: left;
    font-size: 0.95rem;
  }
  th { color: var(--muted); font-weight: 600; }
`;

export default GlobalStyles;
