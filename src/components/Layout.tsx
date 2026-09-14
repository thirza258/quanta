import { Suspense, useEffect, useState } from "react";
import { NavLink, Outlet, useLocation, useNavigate } from "react-router-dom";
import {
  ArrowUpRight,
  BookOpen,
  ChevronRight,
  Command,
  FlaskConical,
  FolderOpen,
  LayoutDashboard,
  Library,
  LogOut,
  Menu,
  Moon,
  PanelLeftClose,
  Search,
  Sun,
  X,
  FileText,
  CircleHelp,
  ChartNoAxesCombined,
} from "lucide-react";
import { useWorkspace } from "../lib/workspace";
import { lessons, lessonTrack, tracks } from "../lib/catalog";
import { Loading, Modal } from "./ui";
import AuthModal from "./AuthModal";
import PageReferences from "./PageReferences";
const nav = [
  { path: "/", label: "Overview", icon: LayoutDashboard },
  { path: "/curriculum", label: "Curriculum", icon: BookOpen },
  { path: "/lab", label: "Strategy lab", icon: FlaskConical },
  { path: "/simulator", label: "Trading simulator", icon: ChartNoAxesCombined },
  { path: "/experiments", label: "Saved experiments", icon: FolderOpen },
  { path: "/notebook", label: "My notebook", icon: FileText },
];
export default function Layout() {
  const { state, user, online, ready, saveStatus, error, setError, signOut } =
      useWorkspace(),
    location = useLocation(),
    navigate = useNavigate();
  const [theme, setTheme] = useState(
      () => document.documentElement.dataset.theme || "light",
    ),
    [authOpen, setAuthOpen] = useState(false),
    [searchOpen, setSearchOpen] = useState(false),
    [query, setQuery] = useState(""),
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
  const filtered = lessons.filter((l) =>
    `${l.title} ${l.subtitle} ${lessonTrack(l.id)?.title}`
      .toLowerCase()
      .includes(query.toLowerCase()),
  );
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
      <aside className={`sidebar ${menuOpen ? "open" : ""}`}>
        <NavLink to="/" className="brand" aria-label="Quanta home">
          <img src="/favicon.svg" alt="" />
          <span>
            quanta<span className="brand-dot">.</span>
          </span>
        </NavLink>
        <div className="workspace-label">
          <span className="workspace-square">Q</span>
          <div>
            Personal workspace<small>Investment research & learning</small>
          </div>
        </div>
        <div className="nav-section-label">WORKSPACE</div>
        <nav aria-label="Main navigation">
          {nav.map(({ path, label, icon: Icon }) => (
            <NavLink
              to={path}
              key={path}
              end={path === "/"}
              className={({ isActive }) =>
                `nav-item ${isActive ? "active" : ""}`
              }
            >
              <Icon size={18} strokeWidth={1.7} />
              <span>{label}</span>
              {path === "/experiments" && state.experiments.length > 0 ? (
                <small className="nav-count">{state.experiments.length}</small>
              ) : null}
            </NavLink>
          ))}
        </nav>
        <div className="nav-section-label resources-label">RESOURCES</div>
        <NavLink to="/library" className="nav-item">
          <Library size={18} strokeWidth={1.7} />
          Reference library
          <ArrowUpRight className="trailing-icon" size={14} />
        </NavLink>
        <NavLink to="/methodology" className="nav-item">
          <CircleHelp size={18} strokeWidth={1.7} />
          How Quanta works
        </NavLink>
        <div className="sidebar-bottom">
          <div className="learning-note">
            <div className="little-rule" />
            <p>
              Understand the principle.
              <br />
              Test the assumption.
            </p>
            <span>THE QUANTA APPROACH</span>
          </div>
          <button className="quick-search" onClick={() => setSearchOpen(true)}>
            <Search size={15} />
            Find a lesson<kbd>⌘ K</kbd>
          </button>
          <div className="profile-row">
            <button
              className="profile-button"
              onClick={() => setAuthOpen(true)}
            >
              <span className="avatar">
                {user ? user.name.slice(0, 2).toUpperCase() : "G"}
              </span>
              <span>
                {user?.name || "Guest researcher"}
                <small>{user ? "Personal account" : "Local workspace"}</small>
              </span>
            </button>
            {user ? (
              <button
                className="icon-button"
                aria-label="Sign out"
                onClick={() => signOut().catch((e) => setError(e.message))}
              >
                <LogOut size={16} />
              </button>
            ) : (
              <button
                className="profile-arrow icon-button"
                aria-label="Create account"
                onClick={() => setAuthOpen(true)}
              >
                <ChevronRight size={17} />
              </button>
            )}
          </div>
        </div>
      </aside>
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
      <Modal
        open={searchOpen}
        onOpenChange={setSearchOpen}
        title="Find your next idea"
        description={`Search all ${lessons.length} lessons across ${tracks.length} courses.`}
        wide
      >
        <label className="search-input">
          <Search size={20} />
          <input
            autoFocus
            placeholder="Try margin of safety, regression, or AMMs…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <Command size={16} />
        </label>
        <div className="search-results">
          {filtered.length ? (
            filtered.slice(0, 12).map((l) => (
              <button
                key={l.id}
                onClick={() => {
                  setSearchOpen(false);
                  navigate(`/learn/${l.id}`);
                }}
              >
                <span className="mono muted">{l.id}</span>
                <span>
                  <strong>{l.title}</strong>
                  <small>{lessonTrack(l.id)?.title}</small>
                </span>
                <ChevronRight size={16} />
              </button>
            ))
          ) : (
            <p className="muted">
              No lessons match “{query}”. Try a broader topic.
            </p>
          )}
        </div>
      </Modal>
    </div>
  );
}
