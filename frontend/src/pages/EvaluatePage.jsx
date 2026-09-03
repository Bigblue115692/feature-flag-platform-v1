import React, { useState } from "react";
import { api } from "../api/client";

const initialRequest = {
  project_key: "checkout",
  environment_key: "production",
  flag_key: "new_checkout",
  user: {
    id: "user-107",
    premium: true,
    country: "US",
    plan: "pro",
  },
};

export default function EvaluatePage() {
  const [requestText, setRequestText] = useState(
    JSON.stringify(initialRequest, null, 2),
  );
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function evaluate(event) {
    event.preventDefault();
    setError(null);

    try {
      const payload = JSON.parse(requestText);
      const response = await api.evaluate(payload);
      setResult(response);
    } catch (err) {
      setError(err);
    }
  }

  return (
    <section>
      <div className="page-header">
        <div>
          <h1>Evaluation Playground</h1>
          <p>Ask the backend whether a user receives a feature.</p>
        </div>
      </div>

      <div className="two-column">
        <form className="card" onSubmit={evaluate}>
          <label>
            Evaluation request
            <textarea
              className="code-area"
              value={requestText}
              onChange={(event) => setRequestText(event.target.value)}
            />
          </label>
          <button type="submit">Evaluate</button>
        </form>

        <div className="card">
          <h3>Result</h3>

          {error && (
            <pre className="error-panel">
              {JSON.stringify(error.payload || error.message, null, 2)}
            </pre>
          )}

          {!error && !result && (
            <p className="muted">Submit an evaluation request.</p>
          )}

          {result && (
            <pre className="result-panel">
              {JSON.stringify(result, null, 2)}
            </pre>
          )}
        </div>
      </div>
    </section>
  );
}
