import { emptyWorkspace, normalize } from "@/features/workspace/model/state";
import type { WorkspaceState } from "@/features/workspace/model/types";
export function storageKey(id?: string) {
  return `quanta-workspace:v1:${id || "guest"}`;
}
export function read(id?: string): WorkspaceState {
  try {
    return normalize(
      JSON.parse(localStorage.getItem(storageKey(id)) || "null"),
    );
  } catch {
    return emptyWorkspace();
  }
}
export function readSync(
  id: string,
): { version: number; pending: boolean } | null {
  try {
    return JSON.parse(localStorage.getItem(`${storageKey(id)}:sync`) || "null");
  } catch {
    return null;
  }
}
