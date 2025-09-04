import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [cvResponse, setCvResponse] = useState("");
  const [emailData, setEmailData] = useState({ recipient: "", subject: "", body: "" });
  const [emailResponse, setEmailResponse] = useState("");
  const [loadingCV, setLoadingCV] = useState(false);
  const [loadingEmail, setLoadingEmail] = useState(false);

  const API_BASE = "http://193.203.163.116:8001";

  const askCV = async () => {
    if (!question.trim()) return setCvResponse("Please enter a question.");
    setLoadingCV(true);
    setCvResponse("");
    try {
      const res = await axios.post(`${API_BASE}/query_resume`, { question });
      console.log("Backend response:", res.data);
      setCvResponse(typeof res.data.answer === "object"
        ? JSON.stringify(res.data.answer, null, 2)
        : res.data.answer
      );
    } catch (err) {
      console.error(err);
      setCvResponse("Error: " + (err.response?.data?.error || err.message));
    } finally {
      setLoadingCV(false);
    }
  };

  const sendEmail = async () => {
    if (!emailData.recipient || !emailData.subject || !emailData.body) {
      return setEmailResponse("Please fill all email fields.");
    }
    setLoadingEmail(true);
    setEmailResponse("");
    try {
      const res = await axios.post(`${API_BASE}/send_email`, emailData);
      console.log("Email response:", res.data);
      setEmailResponse(res.data.message);
    } catch (err) {
      console.error(err);
      setEmailResponse("Error: " + (err.response?.data?.error || err.message));
    } finally {
      setLoadingEmail(false);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>MCP CV Chat & Email</h1>

      <section style={{ marginBottom: "2rem" }}>
        <h2>Ask about your CV</h2>
        <input
          type="text"
          placeholder="e.g., What is my present job?"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          style={{ width: "300px", marginRight: "10px" }}
        />
        <button onClick={askCV} disabled={loadingCV}>
          {loadingCV ? "Loading..." : "Ask"}
        </button>
        <pre style={{ whiteSpace: "pre-wrap" }}>{cvResponse}</pre>
      </section>

      <section>
        <h2>Send Email</h2>
        <input
          type="text"
          placeholder="Recipient"
          value={emailData.recipient}
          onChange={(e) => setEmailData({ ...emailData, recipient: e.target.value })}
          style={{ width: "300px", marginRight: "10px", marginBottom: "5px" }}
        />
        <input
          type="text"
          placeholder="Subject"
          value={emailData.subject}
          onChange={(e) => setEmailData({ ...emailData, subject: e.target.value })}
          style={{ width: "300px", marginRight: "10px", marginBottom: "5px" }}
        />
        <input
          type="text"
          placeholder="Body"
          value={emailData.body}
          onChange={(e) => setEmailData({ ...emailData, body: e.target.value })}
          style={{ width: "300px", marginRight: "10px", marginBottom: "5px" }}
        />
        <button onClick={sendEmail} disabled={loadingEmail}>
          {loadingEmail ? "Sending..." : "Send"}
        </button>
        <pre style={{ whiteSpace: "pre-wrap" }}>{emailResponse}</pre>
      </section>
    </div>
  );
}

//frontend