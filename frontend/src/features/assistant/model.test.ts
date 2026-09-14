import { describe, expect, it } from "vitest";
import { canApply, conversationContext } from "./model";
import type { AssistantFile, ChatMessage } from "./model";

const file: AssistantFile = {
  path: "main.py",
  language: "python",
  content: "print(2)",
  target: "lesson",
};

describe("assistant context and editor boundary", () => {
  it("keeps recent messages and files within API limits", () => {
    const messages: ChatMessage[] = Array.from({ length: 20 }, (_, i) => ({
      id: String(i),
      role: i % 2 ? "assistant" : "user",
      content: `message ${i} ${"x".repeat(12000)}`,
      files: [file],
    }));
    const history = conversationContext(messages, true);
    expect(history.length).toBeLessThanOrEqual(10);
    expect(
      history.reduce((sum, item) => sum + item.content.length, 0),
    ).toBeLessThanOrEqual(60000);
    expect(history.every((item) => item.content.length <= 16000)).toBe(true);
    expect(history.at(-1)?.content).toContain("message 19");
    expect(history.at(-1)?.content).toContain("print(2)");
  });
  it("omits previously generated files when code sharing is off", () => {
    const history = conversationContext(
      [{ id: "a", role: "assistant", content: "Try this", files: [file] }],
      false,
    );
    expect(history).toEqual([{ role: "assistant", content: "Try this" }]);
  });
  it("only offers complete files for the current lesson language", () => {
    expect(canApply(file, "python")).toBe(true);
    expect(canApply(file, "c")).toBe(false);
    expect(canApply(file)).toBe(false);
    expect(canApply({ ...file, target: "local" }, "python")).toBe(false);
    expect(canApply({ ...file, path: "requirements.txt" }, "python")).toBe(
      false,
    );
  });
});
