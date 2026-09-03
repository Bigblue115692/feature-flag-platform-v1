import { useCallback, useState } from "react";

export default function useAsync(asyncFunction) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = useCallback(
    async (...args) => {
      setLoading(true);
      setError(null);
      try {
        return await asyncFunction(...args);
      } catch (err) {
        setError(err);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [asyncFunction],
  );

  return { execute, loading, error };
}
