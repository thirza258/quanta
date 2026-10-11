import { tracks } from "@/features/learning/model/catalog";
import {
  kindLabels,
  learningResources,
  levelLabels,
  RESOURCES_CHECKED,
  tierDescriptions,
  tierLabels,
  topicLabels,
  type LearningResource,
  type ResourceKind,
  type ResourceTier,
  type ResourceTopic,
} from "@/features/references/model/resources";
import { ExternalLink } from "@/shared/components/ui";
import {
  Award,
  BookOpen,
  Database,
  FileCode2,
  GraduationCap,
  LayoutDashboard,
  Library,
  Search,
  X,
  type LucideIcon,
} from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";

const tiers: ResourceTier[] = ["free", "freemium", "paid"];
const kindIcons: Record<ResourceKind, LucideIcon> = {
  book: BookOpen,
  course: GraduationCap,
  documentation: FileCode2,
  data: Database,
  research: Library,
  platform: LayoutDashboard,
  program: Award,
};
const courseTitles = new Map(tracks.map((track) => [track.id, track.title]));

function matches(resource: LearningResource, query: string) {
  const text = [
    resource.title,
    resource.creator,
    resource.description,
    resource.access,
    kindLabels[resource.kind],
    ...resource.topics.map((topic) => topicLabels[topic]),
  ]
    .join(" ")
    .toLowerCase();
  return text.includes(query);
}

export default function Resources() {
  const [tier, setTier] = useState<ResourceTier | "all">("all");
  const [topic, setTopic] = useState<ResourceTopic | "all">("all");
  const [query, setQuery] = useState("");
  const needle = query.trim().toLowerCase();
  const visible = learningResources.filter(
    (resource) =>
      (tier === "all" || resource.tier === tier) &&
      (topic === "all" || resource.topics.includes(topic)) &&
      (!needle || matches(resource, needle)),
  );
  return (
    <div className="page resources-page">
      <div className="page-eyebrow">KEEP LEARNING</div>
      <h1>Learning resources</h1>
      <p className="page-subtitle">
        Books, courses, data and tools for going further in quantitative
        finance, arranged from free to paid. Each card says which Quanta courses
        it extends.
      </p>
      <div className="catalog-toolbar resources-toolbar">
        <div className="tabs" role="group" aria-label="Filter by cost">
          {(["all", ...tiers] as const).map((value) => (
            <button
              key={value}
              className={tier === value ? "active" : ""}
              aria-pressed={tier === value}
              onClick={() => setTier(value)}
            >
              {value === "all"
                ? "All"
                : value === "freemium"
                  ? "Free + paid"
                  : tierLabels[value]}
            </button>
          ))}
        </div>
        <div className="resources-filters">
          <label className="resources-topic">
            <select
              aria-label="Filter by topic"
              value={topic}
              onChange={(event) =>
                setTopic(event.target.value as ResourceTopic | "all")
              }
            >
              <option value="all">All topics</option>
              {(Object.keys(topicLabels) as ResourceTopic[]).map((value) => (
                <option key={value} value={value}>
                  {topicLabels[value]}
                </option>
              ))}
            </select>
          </label>
          <div className="search-input compact">
            <Search size={16} />
            <input
              aria-label="Search resources"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search resources…"
            />
            {query ? (
              <button
                className="icon-button"
                aria-label="Clear resource search"
                onClick={() => setQuery("")}
              >
                <X size={16} />
              </button>
            ) : null}
          </div>
        </div>
      </div>
      <p className="catalog-results" role="status">
        {visible.length} {visible.length === 1 ? "resource" : "resources"}
        {tier !== "all" ? ` · ${tierLabels[tier].toLowerCase()}` : ""}
        {topic !== "all" ? ` · ${topicLabels[topic]}` : ""}
        {needle ? ` matching “${query.trim()}”` : ""}
      </p>
      {tiers.map((value) => {
        const items = visible.filter((resource) => resource.tier === value);
        if (!items.length) return null;
        return (
          <section
            key={value}
            className="resource-tier-section"
            aria-labelledby={`resource-tier-${value}`}
          >
            <div className="resource-tier-heading">
              <h2 id={`resource-tier-${value}`}>
                {tierLabels[value]}
                <span className="resource-count">{items.length}</span>
              </h2>
              <p>{tierDescriptions[value]}</p>
            </div>
            <div className="reference-list">
              {items.map((resource) => (
                <ResourceCard key={resource.id} resource={resource} />
              ))}
            </div>
          </section>
        );
      })}
      {!visible.length ? (
        <div className="empty-state">
          <Search size={28} />
          <h3>No matching resources</h3>
          <p>Try another topic or show every cost level.</p>
          <button
            className="button secondary"
            onClick={() => {
              setTier("all");
              setTopic("all");
              setQuery("");
            }}
          >
            Show all resources
          </button>
        </div>
      ) : null}
      <p className="fine-print">
        Links and access terms were checked against each provider’s own page on{" "}
        {RESOURCES_CHECKED}. Prices and free tiers change, so confirm the
        current terms on the official page before paying. Quanta is not
        affiliated with these providers and receives nothing from them. For the
        sources cited inside lessons, see the{" "}
        <Link className="text-link" to="/library">
          reference library
        </Link>
        .
      </p>
    </div>
  );
}

function ResourceCard({ resource }: { resource: LearningResource }) {
  const Icon = kindIcons[resource.kind];
  const courses = resource.courses.filter((id) => courseTitles.has(id));
  return (
    <article className="reference-card resource-card">
      <span className="reference-icon">
        <Icon size={22} />
      </span>
      <div>
        <span className="eyebrow">
          {kindLabels[resource.kind]} · {levelLabels[resource.level]}
        </span>
        <h3>{resource.title}</h3>
        <span className="reference-author">{resource.creator}</span>
        <p>{resource.description}</p>
        <p className="resource-access">
          <span className={`resource-tier tier-${resource.tier}`}>
            {tierLabels[resource.tier]}
          </span>
          {resource.access}
        </p>
        <ul className="resource-topics" aria-label="Topics">
          {resource.topics.map((topic) => (
            <li key={topic}>{topicLabels[topic]}</li>
          ))}
        </ul>
        {courses.length ? (
          <p className="resource-courses">
            Extends{" "}
            {courses.map((id, index) => (
              <span key={id}>
                {index ? ", " : ""}
                <Link to={`/curriculum/${id}`}>{courseTitles.get(id)}</Link>
              </span>
            ))}
          </p>
        ) : null}
      </div>
      <ExternalLink href={resource.url}>Visit official page</ExternalLink>
    </article>
  );
}
