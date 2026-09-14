import {
  lessons,
  lessonTrack,
  tracks,
} from "@/features/learning/model/catalog";
import { Modal } from "@/shared/components/ui";

import { ChevronRight, Command, Search } from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
export default function LessonSearch({
  open,
  onOpenChange,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}) {
  const [query, setQuery] = useState("");
  const navigate = useNavigate();
  const filtered = lessons.filter((l) =>
    `${l.title} ${l.subtitle} ${lessonTrack(l.id)?.title}`
      .toLowerCase()
      .includes(query.toLowerCase()),
  );

  return (
    <Modal
      open={open}
      onOpenChange={onOpenChange}
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
                onOpenChange(false);
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
  );
}
