import React, { useMemo, useState } from "react";

export default function FlagCard({ flag, onUpdate, onDelete }) {
  const [rollout, setRollout] = useState(flag.rollout_percentage);

  const statusLabel = flag.enabled ? "Enabled" : "Disabled";
  const rolloutLabel = useMemo(
    () => `${rollout}% rollout`,
    [rollout],
  );

  async function toggleEnabled() {
    await onUpdate(flag.id, {
      enabled: !flag.enabled,
    });
  }

  async function saveRollout() {
    const value = Math.max(0, Math.min(100, Number(rollout)));
    setRollout(value);
    await onUpdate(flag.id, {
      rollout_percentage: value,
    });
  }

  async function togglePremium() {
    await onUpdate(flag.id, {
      premium_only: !flag.premium_only,
    });
  }

  return (
    <article className="card">
      <div className="card-header">
        <div>
          <h3>{flag.name}</h3>
          <code>{flag.key}</code>
        </div>
        <span className={`pill ${flag.enabled ? "pill-on" : "pill-off"}`}>
          {statusLabel}
        </span>
      </div>

      <p className="muted">{flag.description || "No description"}</p>

      <div className="meta-grid">
        <div>
          <span className="label">Project</span>
          <span>{flag.project_key}</span>
        </div>
        <div>
          <span className="label">Environment</span>
          <span>{flag.environment_key}</span>
        </div>
        <div>
          <span className="label">Version</span>
          <span>{flag.version}</span>
        </div>
        <div>
          <span className="label">Premium only</span>
          <span>{flag.premium_only ? "Yes" : "No"}</span>
        </div>
      </div>

      <div className="control-group">
        <label>
          <span>{rolloutLabel}</span>
          <input
            type="range"
            min="0"
            max="100"
            value={rollout}
            onChange={(event) => setRollout(event.target.value)}
          />
        </label>
        <button onClick={saveRollout}>Save rollout</button>
      </div>

      <div className="button-row">
        <button onClick={toggleEnabled}>
          {flag.enabled ? "Disable" : "Enable"}
        </button>
        <button onClick={togglePremium}>
          {flag.premium_only ? "Allow all users" : "Premium only"}
        </button>
        <button className="danger" onClick={() => onDelete(flag.id)}>
          Delete
        </button>
      </div>
    </article>
  );
}
