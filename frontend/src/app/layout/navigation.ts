import {
  Award,
  BookOpen,
  ChartNoAxesCombined,
  FileText,
  FlaskConical,
  FolderOpen,
  LayoutDashboard,
} from "lucide-react";
export const nav = [
  { path: "/", label: "Overview", icon: LayoutDashboard },
  { path: "/curriculum", label: "Curriculum", icon: BookOpen },
  { path: "/certifications", label: "Certifications", icon: Award },
  { path: "/lab", label: "Strategy lab", icon: FlaskConical },
  { path: "/simulator", label: "Trading simulator", icon: ChartNoAxesCombined },
  { path: "/experiments", label: "Saved experiments", icon: FolderOpen },
  { path: "/notebook", label: "My notebook", icon: FileText },
];
