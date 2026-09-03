import React, { useEffect, useState } from "react";
import { api } from "../api/client";

export default function AuditPage() {
  const [events, setEvents] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.listAuditEvents()
      .then(setEvents)
      .catch(setError);
  }, []);

  return (
    <section>
      <div className="page-header">
        <div>
          <h1>Audit Log</h1>
          <p>See flag changes and evaluations recorded by the backend.</p>
        </div>
      </div>

      {error && <div className="error-panel">{error.message}</div>}

      <div className="card table-wrap">
        <table>
          <thead>
            <tr>
              <th>Time</th>
              <th>Action</th>
              <th>Entity</th>
              <th>Actor</th>
              <th>Request ID</th>
            </tr>
          </thead>
          <tbody>
            {events.map((event) => (
              <tr key={event.id}>
                <td>{new Date(event.created_at).toLocaleString()}</td>
                <td>{event.action}</td>
                <td>
                  {event.entity_type}:{event.entity_id}
                </td>
                <td>{event.actor || "—"}</td>
                <td>
                  <code>{event.request_id || "—"}</code>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
