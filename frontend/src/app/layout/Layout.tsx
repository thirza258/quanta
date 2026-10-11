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
  PanelLeftOpen,
  Search,
  Sun,
  X,
} from "lucide-react";
import {
  Suspense,
  useEffect,
  useRef,
  useState,
  useSyncExternalStore,
} from "react";
import { Outlet, useLocation } from "react-router-dom";

const mobileQuery = "(max-width: 760px)";
function subscribeMobile(notify: () => void) {
  const media = window.matchMedia(mobileQuery);
  media.addEventListener("change", notify);
  return () => media.removeEventListener("change", notify);
}

export default function Layout() {
  const { user, online, ready, saveStatus, error, setError } = useWorkspace(),
    location = useLocation();
  const [theme, setTheme] = useState(
      () => document.documentElement.dataset.theme || "light",
    ),
    [authOpen, setAuthOpen] = useState(false),
    [searchOpen, setSearchOpen] = useState(false),
    [menuOpen, setMenuOpen] = useState(false),
    [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const menuButton = useRef<HTMLButtonElement>(null);
  const mobile = useSyncExternalStore(
    subscribeMobile,
    () => window.matchMedia(mobileQuery).matches,
    () => false,
  );
  const mobileMenuOpen = mobile && menuOpen;
  const sidebarOpen = !mobile || menuOpen;
  const isSimulator = location.pathname === "/simulator";
  const sidebarCompact = !mobile && sidebarCollapsed && !isSimulator;
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
  useEffect(() => {
    setMenuOpen(false);
  }, [mobile]);
  useEffect(() => {
    if (!mobileMenuOpen || authOpen || searchOpen) return;
    const sidebar = document.getElementById("workspace-sidebar");
    const overflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    sidebar?.querySelector<HTMLButtonElement>(".sidebar-close")?.focus();

    function handle(event: KeyboardEvent) {
      if (event.defaultPrevented) return;
      if (event.key === "Escape") {
        event.preventDefault();
        setMenuOpen(false);
      } else if (event.key === "Tab") {
        const controls = sidebar?.querySelectorAll<HTMLElement>(
          "a[href], button:not([disabled])",
        );
        const first = controls?.[0];
        const last = controls?.[controls.length - 1];
        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last?.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first?.focus();
        }
      }
    }
    document.addEventListener("keydown", handle);
    return () => {
      document.body.style.overflow = overflow;
      document.removeEventListener("keydown", handle);
      menuButton.current?.focus();
    };
  }, [mobileMenuOpen, authOpen, searchOpen]);
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
        : location.pathname.startsWith("/resources")
          ? "Learning resources"
          : "Reference library");
  if (!ready) return <Loading label="Opening your workspace…" />;
  return (
    <div
      className={`app-shell ${sidebarCompact ? "sidebar-collapsed" : ""} ${isSimulator ? "simulator-shell" : ""}`}
    >
      <a className="skip-link" href="#main-content">
        Skip to content
      </a>
      {mobileMenuOpen ? (
        <button
          className="sidebar-backdrop"
          aria-label="Dismiss navigation"
          onClick={() => setMenuOpen(false)}
        />
      ) : null}
      <Sidebar
        open={sidebarOpen}
        collapsed={sidebarCompact}
        onClose={() => setMenuOpen(false)}
        onSearch={() => setSearchOpen(true)}
        onAccount={() => setAuthOpen(true)}
      />
      <div className="main-shell" inert={mobileMenuOpen}>
        <header className="topbar">
          <button
            ref={menuButton}
            className="icon-button mobile-menu"
            aria-label="Open navigation"
            aria-controls="workspace-sidebar"
            aria-expanded={mobileMenuOpen}
            onClick={() => setMenuOpen((open) => !open)}
          >
            <Menu size={20} />
          </button>
          <div className="breadcrumbs">
            <button
              className="icon-button desktop-menu"
              aria-label={
                sidebarCollapsed ? "Expand sidebar" : "Collapse sidebar"
              }
              title={sidebarCollapsed ? "Expand sidebar" : "Collapse sidebar"}
              aria-controls="workspace-sidebar"
              aria-expanded={!sidebarCollapsed}
              onClick={() => setSidebarCollapsed((collapsed) => !collapsed)}
            >
              {sidebarCollapsed ? (
                <PanelLeftOpen size={16} />
              ) : (
                <PanelLeftClose size={16} />
              )}
            </button>
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
