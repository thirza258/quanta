import { useEffect, useState } from "react";
import { api, ApiError } from "@/shared/api/client";
import type { Certificate } from "./types";

export function useCertificates(userId?: string) {
  const [certificates, setCertificates] = useState<Certificate[]>([]);
  const [loading, setLoading] = useState(!!userId);
  const [error, setError] = useState("");
  const [retry, setRetry] = useState(0);
  useEffect(() => {
    let active = true;
    setCertificates([]);
    setError("");
    setLoading(!!userId);
    if (userId) {
      api<{ certificates: Certificate[] }>("/certificates")
        .then((data) => {
          if (active) setCertificates(data.certificates);
        })
        .catch(() => {
          if (active)
            setError(
              "Your certificates could not be loaded. Please try again.",
            );
        })
        .finally(() => {
          if (active) setLoading(false);
        });
    }
    return () => {
      active = false;
    };
  }, [userId, retry]);
  return {
    certificates,
    loading,
    error,
    retry: () => setRetry((value) => value + 1),
  };
}

export function useVerification(id: string) {
  const [certificate, setCertificate] = useState<Certificate>();
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);
  const [error, setError] = useState("");
  const [retry, setRetry] = useState(0);
  useEffect(() => {
    let active = true;
    setCertificate(undefined);
    setLoading(true);
    setNotFound(false);
    setError("");
    api<{ status: "valid"; certificate: Certificate }>(
      `/certificates/${encodeURIComponent(id)}/verify`,
    )
      .then((data) => {
        if (active) setCertificate(data.certificate);
      })
      .catch((err: unknown) => {
        if (!active) return;
        if (err instanceof ApiError && err.status === 404) setNotFound(true);
        else
          setError(
            "Verification is temporarily unavailable. Please try again.",
          );
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [id, retry]);
  return {
    certificate,
    loading,
    notFound,
    error,
    retry: () => setRetry((value) => value + 1),
  };
}
