import { ApiError, api } from "@/shared/api/client";

export async function simApi<T>(
  path: string,
  method = "GET",
  body?: unknown,
): Promise<T> {
  try {
    return await api<T>("/simulator" + path, {
      method,
      ...(body !== undefined ? { body: JSON.stringify(body) } : {}),
    });
  } catch (error) {
    if (error instanceof ApiError && error.status === 0)
      throw new ApiError(
        "Connection lost. Your confirmed trades are saved. Reconnect to recover before retrying.",
        0,
      );
    throw error;
  }
}
