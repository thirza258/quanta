import { useWorkspace } from "@/features/workspace/WorkspaceProvider";

import {
  ArrowUpRight,
  ChevronRight,
  CircleHelp,
  GraduationCap,
  Library,
  LogOut,
  Search,
  X,
} from "lucide-react";
import { NavLink } from "react-router-dom";
import { nav, navGroups } from "./navigation";
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
        <nav aria-label="Main navigation">
          {navGroups.map((group, index) => (
            <div
              key={group.id}
              role="group"
              aria-labelledby={`nav-group-${group.id}`}
            >
              <div
                className="nav-section-label"
                id={`nav-group-${group.id}`}
                style={index ? { marginTop: 22 } : undefined}
              >
                {group.label}
              </div>
              {nav
                .filter((item) => item.group === group.id)
                .map(({ path, label, icon: Icon }) => (
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
                      <small className="nav-count">
                        {state.experiments.length}
                      </small>
                    ) : null}
                  </NavLink>
                ))}
            </div>
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
          to="/resources"
          className="nav-item"
          aria-label="Learning resources"
          title={collapsed ? "Learning resources" : undefined}
          onClick={onClose}
        >
          <GraduationCap size={18} strokeWidth={1.7} />
          <span>Learning resources</span>
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
        {!collapsed && (
          <div style={{ padding: "0.5rem 0.25rem 0", fontSize: "0.75rem", color: "var(--text-muted, #888)", display: "flex", flexDirection: "column", gap: "0.25rem" }}>
            <div style={{ display: "flex", gap: "0.5rem" }}>
              <NavLink to="/privacy" onClick={onClose} style={{ color: "inherit", textDecoration: "none" }}>Privacy</NavLink>
              <span>•</span>
              <NavLink to="/terms" onClick={onClose} style={{ color: "inherit", textDecoration: "none" }}>Terms</NavLink>
              <span>•</span>
              <span>Self-Hosted</span>
            </div>
            <div style={{ fontSize: "0.6875rem", color: "var(--text-muted, #777)" }}>
              This project is under nevatal.id for educational purposes.
            </div>
          </div>
        )}
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
