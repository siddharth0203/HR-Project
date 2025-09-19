import React, { useEffect, useState } from "react";
import api from "../api";
import "../App.css";
function CandidateForm({ candidate, refresh, clearSelection }) {
  const [form, setForm] = useState({
    id: "",
    name: "",
    email: "",
    phone_number: "",
    current_status: "",
    resume_link: "",
  });

  useEffect(() => {
    if (candidate) {
      setForm(candidate);
    } else {
      setForm({
        id: "",
        name: "",
        email: "",
        phone_number: "",
        current_status: "",
        resume_link: "",
      });
    }
  }, [candidate]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

 const handleSubmit = async (e) => {
    e.preventDefault();

    try {
        if (candidate) {
        // Update
        await api.put(`/candidates/${candidate.id}`, form);
        } else {
        // Add new
        await api.post("/candidates", form);
        }

        refresh();
        clearSelection();

        // ✅ Reset form only when adding new candidate
        if (!candidate) {
        setForm({
            id: "",
            name: "",
            email: "",
            phone_number: "",
            current_status: "",
            resume_link: "",
        });
        }
    } catch (err) {
        console.error("Error saving candidate:", err);
    }
    };


  return (
    <form onSubmit={handleSubmit}>
      <h3>{candidate ? "Edit Candidate" : "Add Candidate"}</h3>
      <input
        type="number"
        name="id"
        placeholder="ID"
        value={form.id}
        onChange={handleChange}
        required
        disabled={!!candidate}
      />
      <input
        type="text"
        name="name"
        placeholder="Name"
        value={form.name}
        onChange={handleChange}
        required
      />
      <input
        type="text"
        name="email"
        placeholder="Email"
        value={form.email}
        onChange={handleChange}
        required
      />
      <input
        type="tel"
        name="phone_number"
        placeholder="Phone Number"
        value={form.phone_number}
        onChange={handleChange}
        required
      />
      <select
        name="current_status"
        value={form.current_status}
        onChange={handleChange}
        required
      >
        <option value="">-- Select Status --</option>
        <option value="Active">Active</option>
        <option value="Inactive">Inactive</option>
      </select>
      <input
        type="text"
        name="resume_link"
        placeholder="Resume Link"
        value={form.resume_link}
        onChange={handleChange}
        required
      />

      <button type="submit">{candidate ? "Update" : "Add"}</button>
    </form>
  );
}

export default CandidateForm;
