export type AssistantFile = {
  path: string;
  language: string;
  content: string;
  target: "lesson" | "local";
};
export type AssistantReply = { message: string; files: AssistantFile[] };
export type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  files: AssistantFile[];
};
export type AssistantMode = "hint" | "environment" | "code";
export type Platform = "macos" | "windows" | "linux";

export function readChat(key: string): ChatMessage[] {
  try {
    const raw = sessionStorage.getItem(key);
    if (!raw || raw.length > 1200000) return [];
    const messages: unknown = JSON.parse(raw);
    if (!Array.isArray(messages)) return [];
    return messages
      .slice(-12)
      .filter(
        (m): m is ChatMessage =>
          !!m &&
          typeof m.id === "string" &&
          (m.role === "user" || m.role === "assistant") &&
          typeof m.content === "string" &&
          m.content.length <= 12000 &&
          Array.isArray(m.files) &&
          m.files.length <= 6 &&
          m.files.every(
            (f: AssistantFile) =>
              f &&
              typeof f.path === "string" &&
              typeof f.language === "string" &&
              typeof f.content === "string" &&
              f.content.length <= 20000 &&
              (f.target === "lesson" || f.target === "local"),
          ),
      );
  } catch {
    return [];
  }
}

export function conversationContext(
  messages: ChatMessage[],
  includeCode: boolean,
) {
  const history = [];
  let remaining = 60000;
  for (const message of messages.slice(-10).reverse()) {
    const files =
      includeCode && message.files.length
        ? `\nPreviously generated files: ${JSON.stringify(message.files)}`
        : "";
    const content = (message.content + files).slice(
      0,
      Math.min(16000, remaining),
    );
    if (!content) break;
    history.unshift({ role: message.role, content });
    remaining -= content.length;
  }
  return history;
}

export function canApply(file: AssistantFile, language?: "python" | "c") {
  return (
    !!language &&
    file.target === "lesson" &&
    file.language === language &&
    file.path.endsWith(language === "c" ? ".c" : ".py")
  );
}
