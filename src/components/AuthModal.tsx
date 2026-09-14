import { useState } from "react";
import { ArrowRight, Download, LoaderCircle, LogOut } from "lucide-react";
import { Modal } from "./ui";
import { useWorkspace } from "../lib/workspace";
import { lessons } from "../lib/catalog";
import { download } from "../lib/api";
export default function AuthModal({
  open,
  onOpenChange,
}: {
  open: boolean;
  onOpenChange: (v: boolean) => void;
}) {
  const {
      authenticate,
      user,
      state,
      saveStatus,
      signOut,
      retrySync,
      useAccountCopy,
    } = useWorkspace(),
    [mode, setMode] = useState<"login" | "register">("register"),
    [name, setName] = useState(""),
    [email, setEmail] = useState(""),
    [password, setPassword] = useState(""),
    [error, setError] = useState(""),
    [busy, setBusy] = useState(false),
    [replaceLocal, setReplaceLocal] = useState(false);
  if (user && replaceLocal)
    return (
      <Modal
        open={open}
        onOpenChange={(value) => {
          setReplaceLocal(false);
          onOpenChange(value);
        }}
        title="Replace local edits?"
        description="This loads the latest account copy and replaces unsynced edits on this device. Export your current workspace first if you need to keep those edits."
      >
        <div className="dialog-actions" style={{ flexWrap: "wrap" }}>
          <button
            className="button secondary"
            onClick={() => download("quanta-workspace-recovery.json", state)}
          >
            Export local copy
          </button>
          <button
            className="button secondary"
            onClick={() => setReplaceLocal(false)}
          >
            Keep local edits
          </button>
          <button
            className="button primary"
            disabled={busy}
            onClick={async () => {
              setBusy(true);
              try {
                await useAccountCopy();
                setReplaceLocal(false);
                onOpenChange(false);
              } catch (err) {
                setError((err as Error).message);
              } finally {
                setBusy(false);
              }
            }}
          >
            Use account copy
          </button>
        </div>
        {error ? (
          <p className="error-message" role="alert">
            {error}
          </p>
        ) : null}
      </Modal>
    );
  if (user)
    return (
      <Modal
        open={open}
        onOpenChange={onOpenChange}
        title="Your research workspace"
        description={`${user.name} · ${user.email}`}
      >
        <p className="inline-notice">{saveStatus}</p>
        <div className="valuation-metrics">
          <div>
            <span>Completed modules</span>
            <strong>
              {state.completed.length} / {lessons.length}
            </strong>
          </div>
          <div>
            <span>Saved experiments</span>
            <strong>{state.experiments.length}</strong>
          </div>
          <div>
            <span>Research notes</span>
            <strong>{state.notes.length}</strong>
          </div>
        </div>
        <div
          className="dialog-actions"
          style={{ marginTop: 24, flexWrap: "wrap" }}
        >
          <button
            className="button secondary"
            onClick={() => download("quanta-workspace.json", state)}
          >
            <Download size={15} />
            Export workspace
          </button>
          {saveStatus.includes("paused") ? (
            <>
              <button
                className="button secondary"
                onClick={() => void retrySync()}
              >
                Retry sync
              </button>
              <button
                className="button secondary"
                onClick={() => setReplaceLocal(true)}
              >
                Resolve sync conflict
              </button>
            </>
          ) : null}
          <button
            className="button primary"
            disabled={busy}
            onClick={async () => {
              setBusy(true);
              try {
                await signOut();
                onOpenChange(false);
              } catch (err) {
                setError((err as Error).message);
              } finally {
                setBusy(false);
              }
            }}
          >
            <LogOut size={15} />
            Sign out
          </button>
        </div>
        {error ? (
          <p className="error-message" role="alert">
            {error}
          </p>
        ) : null}
      </Modal>
    );
  return (
    <Modal
      open={open}
      onOpenChange={onOpenChange}
      title={
        mode === "register" ? "Make room for deeper learning." : "Welcome back."
      }
      description="Save your progress, notes, and experiments to your Quanta account."
    >
      <div className="segmented">
        <button
          className={mode === "register" ? "active" : ""}
          onClick={() => {
            setMode("register");
            setError("");
          }}
        >
          Create account
        </button>
        <button
          className={mode === "login" ? "active" : ""}
          onClick={() => {
            setMode("login");
            setError("");
          }}
        >
          Sign in
        </button>
      </div>
      <form
        onSubmit={async (e) => {
          e.preventDefault();
          setBusy(true);
          setError("");
          try {
            await authenticate(mode, {
              name: name || "Researcher",
              email,
              password,
            });
            onOpenChange(false);
          } catch (err) {
            setError((err as Error).message);
          } finally {
            setBusy(false);
          }
        }}
      >
        {mode === "register" ? (
          <label className="field">
            Your name
            <input
              autoComplete="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              maxLength={60}
              placeholder="Alex Morgan"
            />
          </label>
        ) : null}
        <label className="field">
          Email address
          <input
            type="email"
            autoComplete="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder="you@example.com"
          />
        </label>
        <label className="field">
          Password
          <input
            type="password"
            autoComplete={
              mode === "register" ? "new-password" : "current-password"
            }
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={10}
            maxLength={128}
            placeholder="At least 10 characters"
          />
        </label>
        {error ? (
          <p className="error-message" role="alert">
            {error}
          </p>
        ) : null}
        <button className="button primary full-width" disabled={busy}>
          {busy ? <LoaderCircle className="spin" size={16} /> : null}
          {mode === "register" ? "Create your workspace" : "Sign in"}
          <ArrowRight size={16} />
        </button>
      </form>
      <p className="fine-print">
        Your guest workspace stays on this device. A new account also receives a
        copy of your current work.
      </p>
    </Modal>
  );
}
