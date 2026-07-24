import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import api from "../api/client";

const emptyFields = {
  complaint_source: "",
  customer_name: "",
  product_name: "",
  product_strength: "",
  batch_number: "",
  manufacturing_date: "",
  expiry_date: "",
  quantity_affected: "",
  complaint_type: "",
  complaint_date: "",
  description: "",
  initial_severity: "",
  priority: "",
};

// --- Async actions (call the API) ---

// Send pasted text to the AI and get back filled fields.
export const extractFromText = createAsyncThunk(
  "complaint/extractFromText",
  async (text) => {
    const res = await api.post("/complaints/extract", { text });
    return res.data;
  }
);

// Upload a file and get back filled fields.
export const extractFromFile = createAsyncThunk(
  "complaint/extractFromFile",
  async (file) => {
    const form = new FormData();
    form.append("file", file);
    const res = await api.post("/complaints/extract-file", form);
    return res.data;
  }
);

// Save the current form to the database.
export const saveComplaint = createAsyncThunk(
  "complaint/saveComplaint",
  async (fields) => {
    const res = await api.post("/complaints", fields);
    return res.data;
  }
);

// Ask a follow-up question about the current complaint.
// We send the extracted fields + summary as context so the AI can answer.
export const askQuestion = createAsyncThunk(
  "complaint/askQuestion",
  async (question, { getState }) => {
    const { fields, ai } = getState().complaint;
    const context = JSON.stringify(fields) + "\nSummary: " + ai.summary;
    const res = await api.post("/complaints/ask", { question, context });
    return { question, answer: res.data.answer };
  }
);

// Helper: merge the AI's response into the form + AI panel.
function applyExtraction(state, data) {
  // Only overwrite a field if the AI actually found a value for it.
  Object.entries(data.fields || {}).forEach(([key, value]) => {
    if (value) state.fields[key] = value;
  });
  state.ai.summary = data.ai_summary || "";
  state.ai.risk = data.ai_risk || "";
  state.ai.missingFields = data.missing_fields || [];
  state.ai.completenessNote = data.completeness_note || "";
  state.status = "idle";
}

const complaintSlice = createSlice({
  name: "complaint",
  initialState: {
    fields: { ...emptyFields },
    ai: { summary: "", risk: "", missingFields: [], completenessNote: "" },
    chat: [],       // [{ role: "user" | "ai", text }]
    chatLoading: false,
    status: "idle", // idle | extracting | saving
    saved: false,
    error: null,
  },
  reducers: {
    // Called whenever the user types into a form field.
    updateField(state, action) {
      const { name, value } = action.payload;
      state.fields[name] = value;
    },
    resetForm(state) {
      state.fields = { ...emptyFields };
      state.ai = { summary: "", risk: "", missingFields: [], completenessNote: "" };
      state.chat = [];
      state.saved = false;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // extraction (text or file share the same pending/success handling)
      .addCase(extractFromText.pending, (state) => {
        state.status = "extracting";
        state.error = null;
      })
      .addCase(extractFromText.fulfilled, (state, action) => {
        applyExtraction(state, action.payload);
      })
      .addCase(extractFromText.rejected, (state, action) => {
        state.status = "idle";
        state.error = action.error.message;
      })
      .addCase(extractFromFile.pending, (state) => {
        state.status = "extracting";
        state.error = null;
      })
      .addCase(extractFromFile.fulfilled, (state, action) => {
        applyExtraction(state, action.payload);
      })
      .addCase(extractFromFile.rejected, (state, action) => {
        state.status = "idle";
        state.error = action.error.message;
      })
      // saving
      .addCase(saveComplaint.pending, (state) => {
        state.status = "saving";
      })
      .addCase(saveComplaint.fulfilled, (state) => {
        state.status = "idle";
        state.saved = true;
      })
      // chat Q&A
      .addCase(askQuestion.pending, (state, action) => {
        state.chatLoading = true;
        // show the user's question immediately
        state.chat.push({ role: "user", text: action.meta.arg });
      })
      .addCase(askQuestion.fulfilled, (state, action) => {
        state.chatLoading = false;
        state.chat.push({ role: "ai", text: action.payload.answer });
      })
      .addCase(askQuestion.rejected, (state) => {
        state.chatLoading = false;
        state.chat.push({ role: "ai", text: "Sorry, I couldn't answer that. Please try again." });
      });
  },
});

export const { updateField, resetForm } = complaintSlice.actions;
export default complaintSlice.reducer;
