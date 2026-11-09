import {
  Award,
  BookOpen,
  ChartNoAxesCombined,
  FileText,
  FlaskConical,
  FolderOpen,
  LayoutDashboard,
  Microscope,
  type LucideIcon,
} from "lucide-react";

export const navGroups = [
  { id: "workspace", label: "WORKSPACE" },
  { id: "learn", label: "LEARN" },
  { id: "research", label: "RESEARCH" },
  { id: "simulate", label: "SIMULATE" },
] as const;

export type NavGroup = (typeof navGroups)[number]["id"];
export type NavItem = {
  path: string;
  label: string;
  icon: LucideIcon;
  group: NavGroup;
};

// Flat and in sidebar order: the layout looks up the current page's label here.
export const nav: NavItem[] = [
  { path: "/", label: "Overview", icon: LayoutDashboard, group: "workspace" },
  { path: "/curriculum", label: "Curriculum", icon: BookOpen, group: "learn" },
  {
    path: "/certifications",
    label: "Certifications",
    icon: Award,
    group: "learn",
  },
  {
    path: "/research",
    label: "Experiment registry",
    icon: Microscope,
    group: "research",
  },
  {
    path: "/lab",
    label: "Strategy lab",
    icon: FlaskConical,
    group: "research",
  },
  {
    path: "/experiments",
    label: "Saved experiments",
    icon: FolderOpen,
    group: "research",
  },
  {
    path: "/notebook",
    label: "My notebook",
    icon: FileText,
    group: "research",
  },
  {
    path: "/simulator",
    label: "Trading simulator",
    icon: ChartNoAxesCombined,
    group: "simulate",
  },
];
