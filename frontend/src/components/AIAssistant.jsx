import { useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { extractFromText, extractFromFile, askQuestion } from "../store/complaintSlice";

export default function AIAssistant() {
  const dispatch = useDispatch();
  const { ai, chat, chatLoading, status, error } = useSelector((s) => s.complaint);
  const [pasted, setPasted] = useState("");
  const [question, setQuestion] = useState("");
  const fileInput = useRef(null);

  // Enable the chat only after a complaint has been extracted.
  const hasComplaint = Boolean(ai.summary);

  const send = () => {
    if (question.trim().length < 2) return;
    dispatch(askQuestion(question.trim()));
    setQuestion("");
  };

  const busy = status === "extracting";

  return (
    <div className="panel">
      <div className="panel-title">
        <h2>AI Complaint Intake Assistant</h2>
        <span className="badge" style={{ background: "#eef3ff", color: "#2f6bff" }}>
          BETA
        </span>
      </div>

   
      <div className="dropzone" onClick={() => fileInput.current.click()}>
        Drag &amp; 
        <br />
        or <strong>click to browse</strong>
        <input
          ref={fileInput}
          type="file"
          accept=".pdf,.docx,.txt,.eml"
          hidden
          onChange={(e) => {
            if (e.target.files[0]) dispatch(extractFromFile(e.target.files[0]));
          }}
        />
      </div>
      <p className="format-hint">
        Supported formats: PDF, DOCX, TXT, EML &nbsp;•&nbsp; Max file size: 10MB
      </p>

      <div className="divider">— OR —</div>


      <textarea
        className="paste-area"
        placeholder="Paste complaint text / email here..."
        value={pasted}
        onChange={(e) => setPasted(e.target.value)}
      />
      <button
        className="btn-primary"
        style={{ width: "100%", marginTop: 10 }}
        disabled={busy || pasted.trim().length < 10}
        onClick={() => dispatch(extractFromText(pasted))}
      >
        {busy ? "Analyzing..." : "Extract Details"}
      </button>

   
      {busy && (
        <>
          <div className="progress"><span /></div>
          <p style={{ color: "#6b7688", fontSize: 12, marginTop: 8 }}>
            Analyzing document and extracting key details...
          </p>
        </>
      )}

      {error && (
        <div className="insight risk" style={{ marginTop: 14 }}>
          {error}
        </div>
      )}

   
      {!busy && !ai.summary && !error && (
        <div className="assistant-box">
          Upload a complaint document or paste text above. I'll read it and
          fill in the form on the left for you.
        </div>
      )}

  
      {ai.summary && (
        <div className="insight summary">
          <span className="insight-title">Complaint Summary</span>
          {ai.summary}
        </div>
      )}
      {ai.risk && (
        <div className="insight risk">
          <span className="insight-title">AI Risk Assessment</span>
          {ai.risk}
        </div>
      )}
      {ai.completenessNote && (
        <div className={`insight ${ai.missingFields.length ? "missing" : "ok"}`}>
          <span className="insight-title">Completeness Check</span>
          {ai.completenessNote}
        </div>
      )}

    
      {hasComplaint && (
        <div className="chat">
          <div className="chat-label">Ask about this complaint</div>

          <div className="chat-messages">
            {chat.map((m, i) => (
              <div key={i} className={`bubble ${m.role}`}>{m.text}</div>
            ))}
            {chatLoading && <div className="bubble ai">Thinking...</div>}
          </div>

          <div className="chat-input">
            <input
              value={question}
              placeholder="Ask me anything about this complaint..."
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && send()}
            />
            <button className="btn-primary" onClick={send} disabled={chatLoading}>
              Send
            </button>
          </div>
        </div>
      )}

      <p className="disclaimer">
    
      </p>
    </div>
  );
}
