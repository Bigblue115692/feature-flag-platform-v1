import baseScenario, { options as baseOptions } from "./evaluate.js";

export const options = {
  ...baseOptions,
  scenarios: {
    evaluation_load: {
      executor: "ramping-arrival-rate",
      startRate: 500,
      timeUnit: "1s",
      preAllocatedVUs: 1000,
      maxVUs: 5000,
      stages: [
        { target: 500, duration: "30s" },
        { target: 1500, duration: "30s" },
        { target: 3000, duration: "30s" },
        { target: 5000, duration: "30s" },
        { target: 7500, duration: "30s" },
        { target: 10000, duration: "30s" },
      ],
      gracefulStop: "10s",
    },
  },
};

export default baseScenario;
