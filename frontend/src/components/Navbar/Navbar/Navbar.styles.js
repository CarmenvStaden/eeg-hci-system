import styled from "styled-components";

export const Bar = styled.header`
  background: var(--card);
  border-bottom: 1px solid var(--border);
`;

export const Inner = styled.div`
  max-width: 1100px;
  margin: 0 auto;
  padding: 0.8rem 1rem;
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: space-between;
`;

export const Tabs = styled.nav`
  display: flex;
  gap: 0.8rem;

  a {
    padding: 0.45rem 0.7rem;
    border-radius: 8px;
    text-decoration: none;
  }
  a.active {
    background: var(--brand);
    color: white;
  }
`;

export const Right = styled.div`
  display: flex;
  gap: 0.6rem;
  align-items: center;
`;
