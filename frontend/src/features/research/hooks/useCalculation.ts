import { post } from "@/shared/api/client";
import { useEffect, useState } from "react";
export function useCalculation<T>(path: string, input: unknown) {
  const [result, setResult] = useState<T | null>(null),
    [error, setError] = useState(""),
    [busy, setBusy] = useState(true);
  const key = JSON.stringify(input);
  useEffect(() => {
    let active = true;
    setBusy(true);
    const timer = setTimeout(() => {
      post<T>(path, JSON.parse(key))
        .then((value) => {
          if (active) {
            setResult(value);
            setError("");
          }
        })
        .catch((e) => {
          if (active) setError(e.message);
        })
        .finally(() => {
          if (active) setBusy(false);
        });
    }, 250);
    return () => {
      active = false;
      clearTimeout(timer);
    };
  }, [path, key]);
  return { result, error, busy };
}
