//services/specialistDash.js
import { authFetch } from "./http";


// ---------- FETCH PATIENTS (LIST) ----------

export async function listPatients() {
  const res = await authFetch("/api/dashboards/patients/");
  if (!res.ok) {
    throw new Error(`Failed to fetch patients: HTTP ${res.status}`);
  }
  return res.json();
}

// ---------- ADD PATIENTS ----------

// Helper: lookup user ID by email using current string-returning API
async function lookupUserIdByEmail(email) {
  const res = await authFetch('/api/accounts/users/lookup/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ target_email: email }), // must match serializer
  });

  if (!res.ok) {
    const raw = await res.text();
    throw new Error(`Email lookup failed (HTTP ${res.status}): ${raw}`);
  }

  const raw = await res.text(); // e.g. "\"Found user: 4\"" or "Found user: 4"
  let text = raw;

  // If it's JSON like `"Found user: 4"`, parse it to strip the quotes
  try {
    const parsed = JSON.parse(raw);
    if (typeof parsed === 'string') {
      text = parsed; // "Found user: 4"
    }
  } catch {
    // not JSON, just use raw as-is
  }

  // TODO: improve the API to return JSON
  // Grab the first sequence of digits anywhere in the string
  const match = text.match(/(\d+)/);
  if (!match) {
    throw new Error(`Could not parse user id from response: ${JSON.stringify(text)}`);
  }

  const id = Number(match[1]);
  if (Number.isNaN(id)) {
    throw new Error(`Parsed id is not a number: "${match[1]}"`);
  }

  return id;
}

// add patient by email
export async function addPatientByEmail(email) {
  // Get the patient's user ID from the email
  const patientId = await lookupUserIdByEmail(email);

  // Call your PatientsCreateList.post endpoint with that ID
  const res = await authFetch('/api/dashboards/patients/add/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    // key must match what PatientAddSerializer expects
    body: JSON.stringify({ patient_user_id: patientId }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Add patient failed (HTTP ${res.status}): ${text}`);
  }

  // view returns JSON: {"PatientAddSuccess": "..."}
  const data = await res.json();
  return data;
}


