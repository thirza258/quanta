import { useWorkspace } from "@/features/workspace/WorkspaceProvider";

import {
  ArrowUpRight,
  ChevronRight,
  CircleHelp,
  Library,
  LogOut,
  Search,
  X,
} from "lucide-react";
import { NavLink } from "react-router-dom";
import { nav } from "./navigation";
export default function Sidebar({
  open,
  collapsed,
  onClose,
  onSearch,
  onAccount,
}: {
  open: boolean;
  collapsed: boolean;
  onClose: () => void;
  onSearch: () => void;
  onAccount: () => void;
}) {
  const { state, user, signOut, setError } = useWorkspace();
  return (
    <aside
      id="workspace-sidebar"
      className={`sidebar ${open ? "open" : ""} ${collapsed ? "collapsed" : ""}`}
      aria-label="Workspace sidebar"
      inert={!open}
    >
      <div className="sidebar-header">
        <NavLink
          to="/"
          className="brand"
          aria-label="Quanta home"
          onClick={onClose}
        >
          <img src="/favicon.svg" alt="" />
          <span>
            quanta<span className="brand-dot">.</span>
          </span>
        </NavLink>
        <button
          className="icon-button sidebar-close"
          aria-label="Close navigation"
          onClick={onClose}
        >
          <X size={18} />
        </button>
      </div>
      <div className="sidebar-scroll">
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
              aria-label={label}
              title={collapsed ? label : undefined}
              end={path === "/"}
              onClick={onClose}
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
        <NavLink
          to="/library"
          className="nav-item"
          aria-label="Reference library"
          title={collapsed ? "Reference library" : undefined}
          onClick={onClose}
        >
          <Library size={18} strokeWidth={1.7} />
          <span>Reference library</span>
          <ArrowUpRight className="trailing-icon" size={14} />
        </NavLink>
        <NavLink
          to="/methodology"
          className="nav-item"
          aria-label="How Quanta works"
          title={collapsed ? "How Quanta works" : undefined}
          onClick={onClose}
        >
          <CircleHelp size={18} strokeWidth={1.7} />
          <span>How Quanta works</span>
        </NavLink>
        <div className="learning-note">
          <div className="little-rule" />
          <p>
            Understand the principle.
            <br />
            Test the assumption.
          </p>
          <span>THE QUANTA APPROACH</span>
        </div>
      </div>
      <div className="sidebar-bottom">
        <button
          className="quick-search"
          aria-label="Find a lesson"
          title={collapsed ? "Find a lesson" : undefined}
          onClick={onSearch}
        >
          <Search size={15} />
          <span>Find a lesson</span>
          <kbd>⌘ K</kbd>
        </button>
        <div className="profile-row">
          <button
            className="profile-button"
            aria-label={collapsed ? "Open workspace account" : undefined}
            title={collapsed ? user?.name || "Guest researcher" : undefined}
            onClick={onAccount}
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
              title={collapsed ? "Sign out" : undefined}
              onClick={() => signOut().catch((e) => setError(e.message))}
            >
              <LogOut size={16} />
            </button>
          ) : (
            <button
              className="profile-arrow icon-button"
              aria-label="Create account"
              onClick={onAccount}
            >
              <ChevronRight size={17} />
            </button>
          )}
        </div>
      </div>
    </aside>
  );
}
