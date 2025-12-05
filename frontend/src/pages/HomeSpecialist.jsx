import { useEffect, useState } from "react";
import styled from "styled-components";
import { listPatients, addPatientByEmail } from "../services/specialistDash";

const Card = styled.section`
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1rem;
`;

const ModalBackdrop = styled.div`
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
`;

const Modal = styled.div`
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1rem 1.25rem;
  min-width: 280px;
  max-width: 400px;
`;

const ModalTitle = styled.h3`
  margin: 0 0 0.5rem 0;
`;

const ModalActions = styled.div`
  margin-top: 1rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
`;


export default function HomeSpecialist() {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // state for add-patient modal
  const [showAddModal, setShowAddModal] = useState(false);
  const [addEmail, setAddEmail] = useState("");
  const [addLoading, setAddLoading] = useState(false);
  const [addError, setAddError] = useState(null);
  const [addSuccess, setAddSuccess] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchPatients() {
      try {
        setLoading(true);
        setError(null);

        const data = await listPatients();
        if (cancelled) return;

        setPatients(data);
      } catch (err) {
        if (!cancelled) {
          setError(err.message || "Failed to load patients");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    fetchPatients();

    return () => {
      cancelled = true;
    };
  }, []);

  // HELPERS
  async function refreshPatients() {
    try {
      setLoading(true);
      setError(null);
      const data = await listPatients();
      setPatients(data);
    } catch (err) {
      setError(err.message || "Failed to load patients");
    } finally {
      setLoading(false);
    }
  }

    async function handleAddPatientSubmit(event) {
    event.preventDefault();

    const trimmedEmail = addEmail.trim();
    if (!trimmedEmail) {
      setAddError("Please enter an email address.");
      return;
    }

    setAddLoading(true);
    setAddError(null);
    setAddSuccess(null);

    try {
      const result = await addPatientByEmail(trimmedEmail);
      // result should be {"PatientAddSuccess": "..."} JSON
      setAddSuccess(
        result?.PatientAddSuccess || "Patient successfully added."
      );

      // Refresh the patients list
      await refreshPatients();

      // close the modal after success:
      setShowAddModal(false);
      setAddEmail("");
    } catch (err) {
      setAddError(err.message || "Failed to add patient");
    } finally {
      setAddLoading(false);
    }
  }

  return (
    <>
      <h2>Welcome, Specialist!</h2>
      <Card>
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}>
          <div>Add / Accept Patient</div>
          <button
            title="Add"
            onClick={() => {
              setShowAddModal(true);
              setAddError(null);
              setAddSuccess(null);
            }}>＋</button>
        </div>

        {loading && <p style={{ marginTop: "1rem" }}>Loading patients…</p>}

        {error && (
          <p style={{ marginTop: "1rem", color: "red" }}>
            Error: {error}
          </p>
        )}

        {!loading && !error && (
          <table style={{ marginTop: "1rem", width: "100%" }}>
            <thead>
              <tr>
                <th>Username</th>
                <th>Email</th>
                <th>Date of Birth</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {patients.length === 0 ? (
                <tr>
                  <td colSpan={4} style={{ textAlign: "center", padding: "0.5rem" }}>
                    No patients yet.
                  </td>
                </tr>
              ) : (
                patients.map((p) => (
                  <tr key={p.id}>
                    <td>{p.username}</td>
                    <td>{p.email}</td>
                    <td>
                      {p.date_of_birth
                        ? new Date(p.date_of_birth).toLocaleDateString()
                        : "N/A"}
                    </td>
                    <td style={{ display: "flex", gap: "0.5rem" }}>
                      <a href="/reports">View</a>
                      <a href="/assign">Assign</a>
                      <button>⋯</button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        )}
      </Card>

      {/* Modal popup for add patient */}
      {showAddModal && (
        <ModalBackdrop onClick={() => setShowAddModal(false)}>
          <Modal onClick={(e) => e.stopPropagation()}>
            <ModalTitle>Add Patient by Email</ModalTitle>
            <p style={{ marginTop: 0, marginBottom: "0.5rem" }}>
              Enter the patient&apos;s account email to link them to your panel.
            </p>

            <form onSubmit={handleAddPatientSubmit}>
              <input
                type="email"
                placeholder="patient@example.com"
                value={addEmail}
                onChange={(e) => setAddEmail(e.target.value)}
                style={{
                  width: "100%",
                  padding: "0.4rem 0.5rem",
                  marginTop: "0.25rem",
                  boxSizing: "border-box",
                }}
              />

              {addError && (
                <p style={{ marginTop: "0.5rem", color: "red" }}>{addError}</p>
              )}
              {addSuccess && (
                <p style={{ marginTop: "0.5rem", color: "green" }}>
                  {addSuccess}
                </p>
              )}

              <ModalActions>
                <button
                  type="button"
                  onClick={() => {
                    setShowAddModal(false);
                    setAddEmail("");
                    setAddError(null);
                    setAddSuccess(null);
                  }}
                  disabled={addLoading}
                >
                  Cancel
                </button>
                <button type="submit" disabled={addLoading}>
                  {addLoading ? "Adding…" : "Add Patient"}
                </button>
              </ModalActions>
            </form>
          </Modal>
        </ModalBackdrop>
      )}
    </>
  );
}
