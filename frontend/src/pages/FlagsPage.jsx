import React, { useCallback, useEffect, useState } from "react";
import { api } from "../api/client";
import CreateFlagForm from "../components/CreateFlagForm";
import FlagCard from "../components/FlagCard";

export default function FlagsPage() {
  const [flags, setFlags] = useState([]);
  const [environments, setEnvironments] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const [flagData, environmentData] = await Promise.all([
        api.listFlags(),
        api.listEnvironments(),
      ]);
      setFlags(flagData);
      setEnvironments(environmentData);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  async function handleUpdate(id, patch) {
    const updated = await api.updateFlag(id, patch);
    setFlags((current) =>
      current.map((flag) => (flag.id === id ? updated : flag)),
    );
  }

  async function handleDelete(id) {
    await api.deleteFlag(id);
    setFlags((current) => current.filter((flag) => flag.id !== id));
  }

  async function handleCreate(data) {
    const created = await api.createFlag(data);
    setFlags((current) => [created, ...current]);
  }

  return (
    <section>
      <div className="page-header">
        <div>
          <h1>Feature Flags</h1>
          <p>Control delivery without redeploying application code.</p>
        </div>
        <button onClick={load}>Refresh</button>
      </div>

      {error && (
        <div className="error-panel">
          Could not load data: {error.message}
        </div>
      )}

      <div className="layout-grid">
        <div>
          {loading ? (
            <div className="card">Loading flags...</div>
          ) : (
            <div className="cards">
              {flags.map((flag) => (
                <FlagCard
                  key={flag.id}
                  flag={flag}
                  onUpdate={handleUpdate}
                  onDelete={handleDelete}
                />
              ))}
            </div>
          )}
        </div>

        <CreateFlagForm
          environments={environments}
          onCreate={handleCreate}
        />
      </div>
    </section>
  );
}
