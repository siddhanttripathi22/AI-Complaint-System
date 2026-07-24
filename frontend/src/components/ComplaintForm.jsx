import { useDispatch, useSelector } from "react-redux";
import { updateField, resetForm, saveComplaint } from "../store/complaintSlice";

// A small reusable input wired to Redux.
function Field({ label, name, type = "text", placeholder }) {
  const dispatch = useDispatch();
  const value = useSelector((s) => s.complaint.fields[name]);

  return (
    <div className="field">
      <label>{label}</label>
      <input
        type={type}
        value={value || ""}
        placeholder={placeholder || "Awaiting AI extraction..."}
        onChange={(e) => dispatch(updateField({ name, value: e.target.value }))}
      />
    </div>
  );
}

// A dropdown version for severity / priority.
function SelectField({ label, name, options }) {
  const dispatch = useDispatch();
  const value = useSelector((s) => s.complaint.fields[name]);

  return (
    <div className="field">
      <label>{label}</label>
      <select
        value={value || ""}
        onChange={(e) => dispatch(updateField({ name, value: e.target.value }))}
      >
        <option value="">Awaiting AI extraction...</option>
        {options.map((o) => (
          <option key={o} value={o}>{o}</option>
        ))}
      </select>
    </div>
  );
}

export default function ComplaintForm() {
  const dispatch = useDispatch();
  const { fields, ai, status, saved } = useSelector((s) => s.complaint);

  // The status badge reflects where the complaint is in the workflow.
  const extracted = Boolean(ai.summary);
  let badgeText = "Pending Triage";
  let badgeClass = "badge";
  if (saved) {
    badgeText = "Committed";
    badgeClass = "badge badge-green";
  } else if (extracted) {
    badgeText = "Ready to Commit";
    badgeClass = "badge badge-green";
  }

  return (
    <div className="panel">
      <div className="panel-title">
        <h2>Log Customer Complaint</h2>
        <span className={badgeClass}>{badgeText}</span>
      </div>
      <div className="panel-subtitle">API &amp; FDF Quality Assurance Module</div>

      <div className="section-label">1. Origin &amp; Customer Details</div>
      <div className="grid-2">
        <Field label="Complaint Source" name="complaint_source" />
        <Field label="Customer Name" name="customer_name" />
      </div>

      <div className="section-label">2. Product &amp; Batch Identification</div>
      <div className="grid-2">
        <Field label="Product Name" name="product_name" />
        <Field label="Product Strength / Grade" name="product_strength" />
        <Field label="Batch / Lot Number" name="batch_number" />
        <Field label="Manufacturing Date" name="manufacturing_date" />
        <Field label="Expiry Date" name="expiry_date" />
        <Field label="Quantity Affected" name="quantity_affected" />
      </div>

      <div className="section-label">3. Complaint Details</div>
      <div className="grid-2">
        <Field label="Complaint Type" name="complaint_type" />
        <Field label="Complaint Date" name="complaint_date" />
      </div>
      <div className="field">
        <label>Detailed Complaint Description</label>
        <textarea
          value={fields.description || ""}
          placeholder="Awaiting AI extraction..."
          onChange={(e) =>
            dispatch(updateField({ name: "description", value: e.target.value }))
          }
        />
      </div>

      <div className="section-label">4. Initial Assessment &amp; Priority</div>
      <div className="grid-2">
        <SelectField
          label="Initial Severity"
          name="initial_severity"
          options={["Critical", "Major", "Minor"]}
        />
        <SelectField
          label="Priority"
          name="priority"
          options={["High", "Medium", "Low"]}
        />
      </div>

      <div className="actions">
        <button className="btn-ghost" onClick={() => dispatch(resetForm())}>
          Reset Form
        </button>
        <button
          className="btn-primary"
          disabled={status === "saving"}
          onClick={() => dispatch(saveComplaint(fields))}
        >
          {status === "saving" ? "Saving..." : saved ? "Saved ✓" : "Save Complaint"}
        </button>
      </div>
    </div>
  );
}