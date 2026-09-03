
import React, { useMemo, useState } from "react";

const initialState = {
  environment: "",
  name: "",
  key: "",
  description: "",
  enabled: false,
  rollout_percentage: 0,
  premium_only: false,
  default_value: true,
  off_value: false,
};

export default function CreateFlagForm({ environments, onCreate }) {
  const [form, setForm] = useState(initialState);

  const canSubmit = useMemo(() => {
    return form.environment && form.name.trim() && form.key.trim();
  }, [form]);

  function update(name, value) {
    setForm((current) => ({
      ...current,
      [name]: value,
    }));
  }

  async function submit(event) {
    event.preventDefault();
    if (!canSubmit) {
      return;
    }

    await onCreate({
      ...form,
      environment: Number(form.environment),
      rollout_percentage: Number(form.rollout_percentage),
    });

    setForm(initialState);
  }

  return (
    <form className="card create-form" onSubmit={submit}>
      <h3>Create feature flag</h3>

      <label>
        Environment
        <select
          value={form.environment}
          onChange={(event) => update("environment", event.target.value)}
        >
          <option value="">Select environment</option>
          {environments.map((environment) => (
            <option key={environment.id} value={environment.id}>
              {environment.project_key}/{environment.key}
            </option>
          ))}
        </select>
      </label>

      <label>
        Name
        <input
          value={form.name}
          onChange={(event) => update("name", event.target.value)}
          placeholder="New Checkout"
        />
      </label>

      <label>
        Key
        <input
          value={form.key}
          onChange={(event) => update("key", event.target.value)}
          placeholder="new_checkout"
        />
      </label>

      <label>
        Description
        <textarea
          value={form.description}
          onChange={(event) => update("description", event.target.value)}
          placeholder="What does this feature control?"
        />
      </label>

      <label>
        Rollout percentage
        <input
          type="number"
          min="0"
          max="100"
          value={form.rollout_percentage}
          onChange={(event) => update("rollout_percentage", event.target.value)}
        />
      </label>

      <label className="checkbox-row">
        <input
          type="checkbox"
          checked={form.enabled}
          onChange={(event) => update("enabled", event.target.checked)}
        />
        Enabled
      </label>

      <label className="checkbox-row">
        <input
          type="checkbox"
          checked={form.premium_only}
          onChange={(event) => update("premium_only", event.target.checked)}
        />
        Premium only
      </label>

      <button type="submit" disabled={!canSubmit}>
        Create flag
      </button>
    </form>
  );
}
