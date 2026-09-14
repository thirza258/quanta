import { useWorkspace } from "@/features/workspace/WorkspaceProvider";

import {
  ArrowUpRight,
  ChevronRight,
  CircleHelp,
  Library,
  LogOut,
  Search,
} from "lucide-react";
import { useSyncExternalStore } from "react";
import { NavLink } from "react-router-dom";
import { nav } from "./navigation";
const mobileQuery = "(max-width: 760px)";
function subscribeMobile(notify: () => void) {
  const media = window.matchMedia(mobileQuery);
  media.addEventListener("change", notify);
  return () => media.removeEventListener("change", notify);
}
export default function Sidebar({
  open,
  onSearch,
  onAccount,
}: {
  open: boolean;
  onSearch: () => void;
  onAccount: () => void;
}) {
  const { state, user, signOut, setError } = useWorkspace();
  const mobile = useSyncExternalStore(
    subscribeMobile,
    () => window.matchMedia(mobileQuery).matches,
    () => false,
  );
  return (
    <aside
      className={`sidebar ${open ? "open" : ""}`}
      aria-label="Workspace sidebar"
      inert={mobile && !open}
    >
      <NavLink to="/" className="brand" aria-label="Quanta home">
        <img src="/favicon.svg" alt="" />
        <span>
          quanta<span className="brand-dot">.</span>
        </span>
      </NavLink>
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
        <button className="quick-search" onClick={onSearch}>
          <Search size={15} />
          Find a lesson<kbd>⌘ K</kbd>
        </button>
        <div className="profile-row">
          <button className="profile-button" onClick={onAccount}>
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
