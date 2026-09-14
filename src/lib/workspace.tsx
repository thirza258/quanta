import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
} from "react";
import type { ReactNode } from "react";
import { api, post } from "./api";
import type { User, WorkspaceState } from "./types";

export const emptyWorkspace = (): WorkspaceState => ({
  completed: [],
  lastLesson: "0.1",
  drafts: {},
  notes: [],
  experiments: [],
  submissions: {},
  examDrafts: {},
  examAttempts: {},
  runs: 0,
});
export function normalize(raw: Partial<WorkspaceState> | null): WorkspaceState {
  const base = emptyWorkspace();
  if (!raw || typeof raw !== "object") return base;
  return {
    completed: Array.isArray(raw.completed)
      ? raw.completed.filter((x) => typeof x === "string")
      : [],
    lastLesson: typeof raw.lastLesson === "string" ? raw.lastLesson : "0.1",
    drafts: raw.drafts && typeof raw.drafts === "object" ? raw.drafts : {},
    notes: Array.isArray(raw.notes) ? raw.notes : [],
    experiments: Array.isArray(raw.experiments) ? raw.experiments : [],
    submissions:
      raw.submissions && typeof raw.submissions === "object"
        ? raw.submissions
        : {},
    runs: typeof raw.runs === "number" ? raw.runs : 0,
    examDrafts:
      raw.examDrafts &&
      typeof raw.examDrafts === "object" &&
      !Array.isArray(raw.examDrafts)
        ? raw.examDrafts
        : {},
    examAttempts:
      raw.examAttempts &&
      typeof raw.examAttempts === "object" &&
      !Array.isArray(raw.examAttempts)
        ? Object.fromEntries(
            Object.entries(raw.examAttempts).filter(([, attempts]) =>
              Array.isArray(attempts),
            ),
          )
        : {},
  };
}
function storageKey(id?: string) {
  return `quanta-workspace:v1:${id || "guest"}`;
}
function read(id?: string): WorkspaceState {
  try {
    return normalize(
      JSON.parse(localStorage.getItem(storageKey(id)) || "null"),
    );
  } catch {
    return emptyWorkspace();
  }
}
function readSync(id: string): { version: number; pending: boolean } | null {
  try {
    return JSON.parse(localStorage.getItem(`${storageKey(id)}:sync`) || "null");
  } catch {
    return null;
  }
}
type WorkspaceContextType = {
  state: WorkspaceState;
  update: (fn: (old: WorkspaceState) => WorkspaceState) => void;
  user: User | null;
  ready: boolean;
  online: boolean;
  saveStatus: string;
  error: string;
  setError: (message: string) => void;
  authenticate: (
    mode: "login" | "register",
    data: { email: string; password: string; name: string },
  ) => Promise<void>;
  signOut: () => Promise<void>;
  retrySync: () => Promise<void>;
  useAccountCopy: () => Promise<void>;
};
const Context = createContext<WorkspaceContextType | null>(null);
export function WorkspaceProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState(read),
    [user, setUser] = useState<User | null>(null),
    [ready, setReady] = useState(false),
    [online, setOnline] = useState(false),
    [error, setError] = useState(""),
    [saveStatus, setSaveStatus] = useState("Saved on this device");
  const current = useRef(state),
    account = useRef<User | null>(null),
    revision = useRef(0),
    dirty = useRef(false),
    saving = useRef<Promise<void> | null>(null),
    blocked = useRef(false);
  const activate = useCallback(
    async (next: User | null, mergeGuest = false) => {
      const remote = next
        ? await api<{ state: Partial<WorkspaceState>; version: number }>(
            "/workspace",
          )
        : null;
      let nextState = remote ? normalize(remote.state) : read();
      if (remote && remote.version === 0 && mergeGuest) nextState = read();
      const cachedSync = next ? readSync(next.id) : null;
      const hasPending = !!cachedSync?.pending;
      const conflict = hasPending && cachedSync.version !== remote?.version;
      if (hasPending && next) nextState = read(next.id);
      account.current = next;
      revision.current = hasPending ? cachedSync.version : remote?.version || 0;
      current.current = nextState;
      dirty.current = mergeGuest || hasPending;
      blocked.current = conflict;
      setUser(next);
      setState(nextState);
      setError(
        conflict
          ? "Your account changed in another session. Your unsynced local work has been restored. Export it from your account before resolving the conflict."
          : "",
      );
      setSaveStatus(
        conflict
          ? "Local changes · sync paused"
          : hasPending
            ? "Restored local changes"
            : next
              ? "Synced to your account"
              : "Saved on this device",
      );
    },
    [],
  );
  useEffect(() => {
    let active = true;
    api<User | null>("/auth/me")
      .then(async (value) => {
        if (active) {
          await activate(value);
          if (active) setOnline(true);
        }
      })
      .catch(() => {
        if (active) setOnline(false);
      })
      .finally(() => {
        if (active) setReady(true);
      });
    return () => {
      active = false;
    };
  }, [activate]);
  const flush = useCallback(async () => {
    if (saving.current) return saving.current;
    if (!account.current || !dirty.current || blocked.current) return;
    const task = (async () => {
      while (dirty.current && account.current && !blocked.current) {
        const snapshot = current.current;
        dirty.current = false;
        setSaveStatus("Saving…");
        try {
          const res = await api<{ version: number }>("/workspace", {
            method: "PUT",
            body: JSON.stringify({
              state: snapshot,
              version: revision.current,
            }),
          });
          revision.current = res.version;
          localStorage.setItem(
            `${storageKey(account.current?.id)}:sync`,
            JSON.stringify({ version: res.version, pending: dirty.current }),
          );
          setSaveStatus("Synced to your account");
          setOnline(true);
        } catch (err) {
          dirty.current = true;
          blocked.current = true;
          setError(
            (err as Error).message + " Your edits remain saved on this device.",
          );
          setSaveStatus("Local changes · sync paused");
          break;
        }
      }
    })();
    saving.current = task;
    try {
      await task;
    } finally {
      saving.current = null;
    }
  }, []);
  useEffect(() => {
    if (!ready) return;
    try {
      localStorage.setItem(storageKey(user?.id), JSON.stringify(state));
      if (user)
        localStorage.setItem(
          `${storageKey(user.id)}:sync`,
          JSON.stringify({
            version: revision.current,
            pending: dirty.current || !!saving.current,
          }),
        );
    } catch {
      setError(
        "Device storage is full. Export your notebook or experiments before closing this page.",
      );
    }
    const timer = setTimeout(() => void flush(), 500);
    return () => clearTimeout(timer);
  }, [state, user, ready, flush]);
  const update = useCallback((fn: (old: WorkspaceState) => WorkspaceState) => {
    const next = fn(current.current);
    if (next === current.current) return;
    current.current = next;
    dirty.current = true;
    // Persist the mutation synchronously so immediate navigation/sign-out cannot
    // overwrite the guest workspace or lose a draft before React's effect runs.
    try {
      localStorage.setItem(
        storageKey(account.current?.id),
        JSON.stringify(next),
      );
      if (account.current)
        localStorage.setItem(
          `${storageKey(account.current.id)}:sync`,
          JSON.stringify({ version: revision.current, pending: true }),
        );
    } catch {
      setError(
        "Device storage is full. Export your work before closing this page.",
      );
    }
    setState(next);
  }, []);
  const authenticate = async (
    mode: "login" | "register",
    data: { email: string; password: string; name: string },
  ) => {
    await flush();
    const next = await post<User>(`/auth/${mode}`, data);
    await activate(next, mode === "register");
    setOnline(true);
  };
  const signOut = async () => {
    await flush();
    await post("/auth/logout", {});
    await activate(null);
  };
  const retrySync = async () => {
    blocked.current = false;
    setError("");
    await flush();
  };
  const useAccountCopy = async () => {
    if (!account.current) return;
    await saving.current;
    const remote = await api<{
      state: Partial<WorkspaceState>;
      version: number;
    }>("/workspace");
    const next = normalize(remote.state);
    revision.current = remote.version;
    dirty.current = false;
    blocked.current = false;
    current.current = next;
    setState(next);
    setError("");
    setSaveStatus("Synced to your account");
  };
  return (
    <Context.Provider
      value={{
        state,
        update,
        user,
        ready,
        online,
        saveStatus,
        error,
        setError,
        authenticate,
        signOut,
        retrySync,
        useAccountCopy,
      }}
    >
      {children}
    </Context.Provider>
  );
}
export function useWorkspace() {
  const value = useContext(Context);
  if (!value) throw new Error("WorkspaceProvider missing");
  return value;
}
