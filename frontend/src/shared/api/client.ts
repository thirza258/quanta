export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
  ) {
    super(message);
  }
}
export async function api<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`/api/v1${path}`, {
      credentials: "same-origin",
      ...options,
      signal: options.signal || AbortSignal.timeout(20000),
      headers: { "Content-Type": "application/json", ...options.headers },
    });
  } catch {
    throw new ApiError(
      "The API is unavailable. Start the app with npm run dev or Docker Compose.",
      0,
    );
  }
  const raw = await response.text();
  let body: unknown;
  try {
    body = raw ? JSON.parse(raw) : null;
  } catch {
    throw new ApiError(
      "The API is unavailable. Check that the backend is running.",
      response.status,
    );
  }
  if (!response.ok) {
    const detail = (body as { detail?: unknown })?.detail;
    const message =
      typeof detail === "string"
        ? detail
        : Array.isArray(detail)
          ? detail
              .map((e) => `${e.loc?.slice(1).join(".")}: ${e.msg}`)
              .join("; ")
          : "The request could not be completed.";
    throw new ApiError(message, response.status);
  }
  return body as T;
}
export function post<T>(path: string, data: unknown) {
  return api<T>(path, { method: "POST", body: JSON.stringify(data) });
}
