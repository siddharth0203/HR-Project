import React, { useEffect, useState } from "react";
import api from "../api";
import CandidateForm from "./CandidateForm";
import '../App.css';
function CandidateList() {
  const [candidates, setCandidates] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState(null);

  // Fetch candidates on load
  useEffect(() => {
    fetchCandidates();
  }, []);

  const fetchCandidates = async () => {
    try {
      const res = await api.get("/candidates");
      setCandidates(res.data);
    } catch (err) {
      console.error("Error fetching candidates:", err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/candidates/${id}`);
      fetchCandidates();
    } catch (err) {
      console.error("Error deleting candidate:", err);
    }
  };

  return (
    <div>
      {/* Show Add/Edit Form */}
      <CandidateForm
        candidate={selectedCandidate}
        refresh={fetchCandidates}
        clearSelection={() => setSelectedCandidate(null)}
      />
      <h3>Candidate List</h3>
      <table border="1" cellPadding="8" style={{ marginTop: "20px" }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Status</th>
            <th>Resume Link</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {candidates.map((c) => (
            <tr key={c.id}>
              <td>{c.id}</td>
              <td>{c.name}</td>
              <td>{c.email}</td>
              <td>{c.phone_number}</td>
              <td>
                <span
                  style={{
                    color: c.current_status === "Active" ? "green" : "red",
                    fontWeight: "bold",
                  }}
                >
                  {c.current_status}
                </span>
              </td>
              <td>
                <a href={c.resume_link} target="_blank" rel="noreferrer">
                  {c.resume_link}
                </a>
              </td>
              <td>
                <button onClick={() => setSelectedCandidate(c)}>Edit</button>
                <button onClick={() => handleDelete(c.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default CandidateList;
