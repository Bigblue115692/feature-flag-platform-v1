export type Project = {
  id: number;
  key: string;
  name: string;
  description: string;
  created_at: string;
};

export type Environment = {
  id: number;
  project_id: number;
  key: string;
  name: string;
  created_at: string;
};

export type FeatureFlag = {
  id: number;
  environment_id: number;
  key: string;
  name: string;
  description: string;
  enabled: boolean;
  premium_only: boolean;
  rollout_percentage: number;
  targeting_rules: Array<{attribute: string; operator: string; value: unknown}>;
  version: number;
  created_at: string;
  updated_at: string;
};

export type EvaluationResponse = {
  flag_key: string;
  enabled: boolean;
  reason: string;
  bucket: number | null;
  rollout_percentage: number | null;
};
