import PageReferences from "@/features/references/components/PageReferences";
import AuthModal from "@/features/workspace/components/AuthModal";
import { useWorkspace } from "@/features/workspace/WorkspaceProvider";
import { Loading } from "@/shared/components/ui";
import LessonSearch from "./LessonSearch";
import { nav } from "./navigation";
import Sidebar from "./Sidebar";

import {
  ChevronRight,
  Menu,
  Moon,
  PanelLeftClose,
  Search,
  Sun,
  X,
} from "lucide-react";
import { Suspense, useEffect, useState } from "react";
import { Outlet, useLocation } from "react-router-dom";
export default function Layout() {
  const { user, online, ready, saveStatus, error, setError } = useWorkspace(),
    location = useLocation();
  const [theme, setTheme] = useState(
      () => document.documentElement.dataset.theme || "light",
    ),
    [authOpen, setAuthOpen] = useState(false),
    [searchOpen, setSearchOpen] = useState(false),
    [menuOpen, setMenuOpen] = useState(false);
  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    try {
      localStorage.setItem("quanta-theme", theme);
    } catch {}
  }, [theme]);
  useEffect(() => {
    const sync = () =>
      setTheme(document.documentElement.dataset.theme || "light");
    window.addEventListener("quanta-theme-change", sync);
    return () => window.removeEventListener("quanta-theme-change", sync);
  }, []);
  useEffect(() => {
    function handle(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setSearchOpen((v) => !v);
      }
    }
    document.addEventListener("keydown", handle);
    return () => document.removeEventListener("keydown", handle);
  }, []);
  useEffect(() => {
    setMenuOpen(false);
    window.scrollTo(0, 0);
  }, [location.pathname]);
  const current =
    nav.find((n) =>
      n.path === "/"
        ? location.pathname === "/"
        : location.pathname.startsWith(n.path),
    )?.label ||
    (location.pathname.startsWith("/learn")
      ? "Learning room"
      : location.pathname.startsWith("/exams")
        ? "Assessment room"
        : "Reference library");
  if (!ready) return <Loading label="Opening your workspace…" />;
  return (
    <div
      className={`app-shell ${location.pathname === "/simulator" ? "simulator-shell" : ""}`}
    >
      <a className="skip-link" href="#main-content">
        Skip to content
      </a>
      {menuOpen ? (
        <button
          className="sidebar-backdrop"
          aria-label="Close navigation"
          onClick={() => setMenuOpen(false)}
        />
      ) : null}
      <Sidebar
        open={menuOpen}
        onSearch={() => setSearchOpen(true)}
        onAccount={() => setAuthOpen(true)}
      />
      <div className="main-shell">
        <header className="topbar">
          <button
            className="icon-button mobile-menu"
            aria-label="Open navigation"
            onClick={() => setMenuOpen(true)}
          >
            <Menu size={20} />
          </button>
          <div className="breadcrumbs">
            <PanelLeftClose size={16} />
            <span className="breadcrumb-divider" />
            <span>Workspace</span>
            <ChevronRight size={13} />
            <strong>{current}</strong>
          </div>
          <div className="topbar-actions">
            <span
              className={`connection-status ${online ? "online" : ""}`}
              title={saveStatus}
            >
              <span />
              {online ? "Workspace ready" : "Local workspace"}
            </span>
            <button
              className="icon-button"
              aria-label="Search lessons"
              onClick={() => setSearchOpen(true)}
            >
              <Search size={18} />
            </button>
            <button
              className="icon-button"
              aria-label={
                theme === "light"
                  ? "Switch to dark theme"
                  : "Switch to light theme"
              }
              onClick={() => setTheme(theme === "light" ? "dark" : "light")}
            >
              {theme === "light" ? <Moon size={17} /> : <Sun size={17} />}
            </button>
            <div className="topbar-divider" />
            <button
              className="top-avatar"
              aria-label="Open account"
              onClick={() => setAuthOpen(true)}
            >
              {user?.name[0]?.toUpperCase() || "G"}
            </button>
          </div>
        </header>
        <main id="main-content" tabIndex={-1}>
          {error ? (
            <div className="global-alert" role="alert">
              <span>{error}</span>
              <button
                className="icon-button"
                aria-label="Dismiss notification"
                onClick={() => setError("")}
              >
                <X size={16} />
              </button>
            </div>
          ) : null}
          <Suspense fallback={<Loading />}>
            <Outlet key={user?.id || "guest"} />
          </Suspense>
        </main>
        <PageReferences />
      </div>
      <AuthModal open={authOpen} onOpenChange={setAuthOpen} />
      <LessonSearch open={searchOpen} onOpenChange={setSearchOpen} />
    </div>
  );
}
