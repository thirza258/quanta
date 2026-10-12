import { tracks } from "@/features/learning/model/catalog";
import {
  kindLabels,
  learningResources,
  levelLabels,
  tierLabels,
  topicLabels,
} from "@/features/references/model/resources";
import { describe, expect, it } from "vitest";

describe("learning resources", () => {
  it("lists unique, secure official links", () => {
    const urls = learningResources.map((resource) => resource.url);
    const ids = learningResources.map((resource) => resource.id);
    expect(new Set(urls).size).toBe(urls.length);
    expect(new Set(ids).size).toBe(ids.length);
    for (const resource of learningResources) {
      expect(new URL(resource.url).protocol).toBe("https:");
      expect(resource.title.length).toBeGreaterThan(3);
      expect(resource.creator.trim()).not.toBe("");
      expect(resource.description.length).toBeGreaterThan(40);
      expect(resource.access.trim()).not.toBe("");
    }
  });

  it("covers every cost level with valid labels and topics", () => {
    for (const tier of Object.keys(tierLabels)) {
      expect(
        learningResources.filter((resource) => resource.tier === tier).length,
      ).toBeGreaterThanOrEqual(5);
    }
    for (const resource of learningResources) {
      expect(kindLabels[resource.kind]).toBeTruthy();
      expect(levelLabels[resource.level]).toBeTruthy();
      expect(resource.topics.length).toBeGreaterThan(0);
      for (const topic of resource.topics)
        expect(topicLabels[topic]).toBeTruthy();
    }
    const usedTopics = new Set(learningResources.flatMap((r) => r.topics));
    expect(usedTopics).toEqual(new Set(Object.keys(topicLabels)));
  });

  it("links resources only to courses that exist", () => {
    const courseIds = new Set(tracks.map((track) => track.id));
    for (const resource of learningResources)
      for (const id of resource.courses) expect(courseIds).toContain(id);
    // Every course has somewhere to go next.
    const linked = new Set(learningResources.flatMap((r) => r.courses));
    for (const track of tracks) expect(linked).toContain(track.id);
  });
});
