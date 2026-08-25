import { useEffect, useMemo, useState } from "react";
import { api } from "./api";
import type { Environment, EvaluationResponse, FeatureFlag, Project } from "./types";

export default function App() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [environments, setEnvironments] = useState<Environment[]>([]);
  const [flags, setFlags] = useState<FeatureFlag[]>([]);
  const [projectId, setProjectId] = useState<number | null>(null);
  const [environmentId, setEnvironmentId] = useState<number | null>(null);
  const [error, setError] = useState("");
  const [evaluation, setEvaluation] = useState<EvaluationResponse | null>(null);

  const project = useMemo(() => projects.find(p => p.id === projectId), [projects, projectId]);
  const environment = useMemo(() => environments.find(e => e.id === environmentId), [environments, environmentId]);

  useEffect(() => {
    api.projects().then(items => {
      setProjects(items);
      if (items[0]) setProjectId(items[0].id);
    }).catch(e => setError(e.message));
  }, []);

  useEffect(() => {
    if (!projectId) return;
    api.environments(projectId).then(items => {
      setEnvironments(items);
      if (items[0]) setEnvironmentId(items[0].id);
    }).catch(e => setError(e.message));
  }, [projectId]);

  async function refreshFlags(envId = environmentId) {
    if (!envId) return;
    try {
      setFlags(await api.flags(envId));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load flags");
    }
  }

  useEffect(() => {
    refreshFlags();
  }, [environmentId]);

  async function toggle(flag: FeatureFlag) {
    await api.updateFlag(flag.id, { enabled: !flag.enabled });
    await refreshFlags();
  }

  async function setRollout(flag: FeatureFlag, rollout: number) {
    await api.updateFlag(flag.id, { rollout_percentage: rollout });
    await refreshFlags();
  }

  async function createFlag() {
    if (!environmentId) return;
    const key = prompt("Flag key, e.g. dark_mode");
    if (!key) return;
    const name = prompt("Flag name", key) ?? key;

    await api.createFlag(environmentId, {
      key,
      name,
      description: "",
      enabled: false,
      premium_only: false,
      rollout_percentage: 10,
      targeting_rules: []
    });
    await refreshFlags();
  }

  async function evaluate(flag: FeatureFlag) {
    if (!project || !environment) return;

    setEvaluation(await api.evaluate({
      project_key: project.key,
      environment_key: environment.key,
      flag_key: flag.key,
      user: {
        id: "user-107",
        premium: true,
        attributes: { country: "US" }
      }
    }));
  }

  return (
    <div className="appShell">
      <aside>
        <div className="brand">Flagship</div>
        <p className="muted">Progressive delivery</p>

        <label>
          Project
          <select value={projectId ?? ""} onChange={e => setProjectId(Number(e.target.value))}>
            {projects.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
          </select>
        </label>

        <label>
          Environment
          <select value={environmentId ?? ""} onChange={e => setEnvironmentId(Number(e.target.value))}>
            {environments.map(env => <option key={env.id} value={env.id}>{env.name}</option>)}
          </select>
        </label>
      </aside>

      <main>
        <header>
          <div>
            <span className="eyebrow">Feature management</span>
            <h1>{project?.name ?? "Feature Flag Platform"}</h1>
            <p>{environment?.name ?? "Choose an environment"}</p>
          </div>
          <button onClick={createFlag}>+ New flag</button>
        </header>

        {error && <div className="error">{error}</div>}

        <section className="grid">
          {flags.map(flag => (
            <article className="card" key={flag.id}>
              <div className="cardTop">
                <div>
                  <h2>{flag.name}</h2>
                  <code>{flag.key}</code>
                </div>
                <button className={flag.enabled ? "toggle on" : "toggle"} onClick={() => toggle(flag)}>
                  {flag.enabled ? "ON" : "OFF"}
                </button>
              </div>

              <p>{flag.description || "No description."}</p>

              <div className="badges">
                <span>{flag.premium_only ? "Premium only" : "All users"}</span>
                <span>v{flag.version}</span>
              </div>

              <label>
                Rollout: {flag.rollout_percentage}%
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={flag.rollout_percentage}
                  onChange={e => setRollout(flag, Number(e.target.value))}
                />
              </label>

              <button className="secondary" onClick={() => evaluate(flag)}>
                Evaluate user-107
              </button>
            </article>
          ))}
        </section>

        <section className="evaluation">
          <span className="eyebrow">Evaluation playground</span>
          <h2>Latest decision</h2>
          {evaluation ? (
            <pre>{JSON.stringify(evaluation, null, 2)}</pre>
          ) : (
            <p className="muted">Click “Evaluate user-107” on a flag.</p>
          )}
        </section>
      </main>
    </div>
  );
}
