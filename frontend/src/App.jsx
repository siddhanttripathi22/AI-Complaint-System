import ComplaintForm from "./components/ComplaintForm";
import AIAssistant from "./components/AIAssistant";

export default function App() {
  return (
    <>
      <header className="app-header">
        <h1>AI Customer Complaint Management</h1>
        <p>Pharmaceutical Quality Management System — API &amp; FDF</p>
      </header>

      <main className="layout">
        <ComplaintForm />
        <AIAssistant />
      </main>
    </>
  );
}
