import * as Dialog from "@radix-ui/react-dialog";
import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {
  ArrowUp,
  BookOpen,
  Code2,
  Download,
  Lightbulb,
  LoaderCircle,
  Monitor,
  Plus,
  Sparkles,
  Square,
  X,
} from "lucide-react";
import type { Lesson, Track } from "@/features/learning/model/types";
import { useWorkspace } from "@/features/workspace/WorkspaceProvider";
import { api } from "@/shared/api/client";
import { conversationContext, readChat } from "../model";
import type {
  AssistantMode,
  AssistantReply,
  ChatMessage,
  Platform,
} from "../model";
import AssistantFiles from "./AssistantFiles";
import "../assistant.css";

const modes = [
  {
    id: "hint",
    label: "Help me understand",
    icon: Lightbulb,
    prompt:
      "I'm stuck on this topic. Explain the key idea with a simple example and give me one small step to try.",
  },
  {
    id: "environment",
    label: "Set up my environment",
    icon: Monitor,
    prompt:
      "Create the starter files and setup instructions I need to practice this course locally. Include dependencies, run commands, and a small check that it works.",
  },
  {
    id: "code",
    label: "Help me write code",
    icon: Code2,
    prompt:
      "Help me with the current lesson code. If there is an error, explain and fix it; otherwise build a small example for the lesson. Explain how to test it.",
  },
] as const;

export default function CourseAssistant(props: {
  course: Track;
  lesson?: Lesson;
  executionError?: string;
  onApply?: (code: string) => void;
}) {
  const { user } = useWorkspace();
  return (
    <Assistant
      key={`${user?.id ?? "guest"}:${props.lesson?.id ?? props.course.id}`}
      {...props}
    />
  );
}

function Assistant({
  course,
  lesson,
  executionError,
  onApply,
}: {
  course: Track;
  lesson?: Lesson;
  executionError?: string;
  onApply?: (code: string) => void;
}) {
  const { state, user } = useWorkspace();
  const storageKey = `quanta-assistant:v1:${user?.id ?? "guest"}:${lesson?.id ?? course.id}`;
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState(() => readChat(storageKey));
  const [input, setInput] = useState("");
  const [mode, setMode] = useState<AssistantMode>("hint");
  const [platform, setPlatform] = useState<Platform>(() =>
    /Win/i.test(navigator.platform)
      ? "windows"
      : /Linux/i.test(navigator.platform)
        ? "linux"
        : "macos",
  );
  const [includeCode, setIncludeCode] = useState(true);
  const [connection, setConnection] = useState<
    "loading" | "ready" | "disabled" | "error"
  >("loading");
  const [connectionVersion, setConnectionVersion] = useState(0);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [storageError, setStorageError] = useState(false);
  const [notice, setNotice] = useState("");
  const pending = useRef<{
    controller: AbortController;
    id: string;
    message: string;
  } | null>(null);
  const bottom = useRef<HTMLDivElement>(null);
  const textarea = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (!open) return;
    const controller = new AbortController();
    setConnection("loading");
    api<{ enabled: boolean }>("/assistant/status", {
      signal: AbortSignal.any([controller.signal, AbortSignal.timeout(10000)]),
    })
      .then((result) => {
        if (!controller.signal.aborted)
          setConnection(result.enabled ? "ready" : "disabled");
      })
      .catch(() => {
        if (!controller.signal.aborted) setConnection("error");
      });
    return () => controller.abort();
  }, [open, connectionVersion]);
  useEffect(
    () => () => {
      pending.current?.controller.abort();
      pending.current = null;
    },
    [],
  );
  useEffect(() => {
    try {
      if (messages.length)
        sessionStorage.setItem(storageKey, JSON.stringify(messages.slice(-12)));
      else sessionStorage.removeItem(storageKey);
      setStorageError(false);
    } catch {
      setStorageError(true);
    }
  }, [messages, storageKey]);
  useEffect(() => {
    if (open) bottom.current?.scrollIntoView({ block: "nearest" });
  }, [messages, busy, open]);

  function stop() {
    const request = pending.current;
    if (!request) return;
    pending.current = null;
    request.controller.abort();
    setMessages((current) => current.filter((item) => item.id !== request.id));
    setInput(request.message);
    setBusy(false);
    setNotice(
      "Response stopped. Your question is ready to edit or send again.",
    );
  }
  function changeOpen(value: boolean) {
    if (!value) stop();
    setOpen(value);
  }
  async function send(message: string, selectedMode = mode) {
    if (!message.trim() || pending.current || connection !== "ready") return;
    const controller = new AbortController();
    const timeout = AbortSignal.timeout(95000);
    const id = crypto.randomUUID();
    pending.current = { controller, id, message };
    setMode(selectedMode);
    setBusy(true);
    setError("");
    setNotice("");
    setInput("");
    const next: ChatMessage[] = [
      ...messages,
      { id, role: "user", content: message.trim(), files: [] },
    ];
    setMessages(next);
    try {
      const answer = await api<AssistantReply>("/assistant/chat", {
        method: "POST",
        signal: AbortSignal.any([controller.signal, timeout]),
        body: JSON.stringify({
          course_id: course.id,
          lesson_id: lesson?.id ?? null,
          message: message.trim(),
          mode: selectedMode,
          platform,
          code:
            includeCode && lesson
              ? (state.drafts[lesson.id] ?? lesson.code).slice(0, 20000)
              : null,
          error:
            includeCode && lesson
              ? executionError?.slice(0, 4000) || null
              : null,
          history: conversationContext(messages, includeCode),
        }),
      });
      if (pending.current?.controller !== controller) return;
      setMessages(
        [
          ...next,
          {
            id: crypto.randomUUID(),
            role: "assistant" as const,
            content: answer.message,
            files: answer.files,
          },
        ].slice(-12),
      );
    } catch (e) {
      if (pending.current?.controller !== controller) return;
      setMessages(messages);
      setInput(message);
      setError(
        timeout.aborted
          ? "The assistant took too long. Try a smaller question."
          : (e as Error).message,
      );
    } finally {
      if (pending.current?.controller === controller) {
        pending.current = null;
        setBusy(false);
        textarea.current?.focus();
      }
    }
  }

  return (
    <Dialog.Root open={open} onOpenChange={changeOpen}>
      <Dialog.Trigger className="button secondary small assistant-trigger">
        <Sparkles size={15} /> Ask AI assistant
      </Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="assistant-overlay" />
        <Dialog.Content
          className="assistant-panel"
          onOpenAutoFocus={(event) => {
            event.preventDefault();
            textarea.current?.focus();
          }}
        >
          <div className="assistant-heading">
            <span className="assistant-mark">
              <Sparkles size={21} />
            </span>
            <div>
              <Dialog.Title>Course assistant</Dialog.Title>
              <Dialog.Description>
                A little guidance. Your next breakthrough.
              </Dialog.Description>
            </div>
            <button
              className="icon-button"
              aria-label="Start a new assistant chat"
              title="New chat"
              disabled={busy || !messages.length}
              onClick={() => {
                setMessages([]);
                setInput("");
                setError("");
                setNotice("");
                textarea.current?.focus();
              }}
            >
              <Plus size={19} />
            </button>
            <Dialog.Close
              className="icon-button"
              aria-label="Close AI assistant"
            >
              <X size={19} />
            </Dialog.Close>
          </div>
          <div className="assistant-context">
            <BookOpen size={15} />
            <div>
              <span>{course.title}</span>
              <strong>
                {lesson
                  ? `${lesson.id} · ${lesson.title}`
                  : "Course guidance & project setup"}
              </strong>
            </div>
          </div>
          <div
            className="assistant-thread"
            role="log"
            aria-label="Assistant conversation"
            aria-live="polite"
            aria-busy={busy}
          >
            {messages.length === 0 ? (
              <div className="assistant-welcome">
                <span className="eyebrow">LEARN WITH A LITTLE HELP</span>
                <h3>Let’s work through it.</h3>
                <p>
                  Unpack a tricky idea, get your tools ready, or turn a lesson
                  into working code.
                </p>
                <div className="assistant-starters">
                  {modes.map(({ id, icon: Icon, label, prompt }) => (
                    <button
                      key={id}
                      disabled={connection !== "ready"}
                      onClick={() => void send(prompt, id)}
                    >
                      <Icon size={18} />
                      <span>{label}</span>
                      <ArrowUp size={15} />
                    </button>
                  ))}
                </div>
                {course.resources?.length ? (
                  <details className="assistant-resources">
                    <summary>Course project downloads</summary>
                    {course.resources.map((resource) => (
                      <a key={resource.url} href={resource.url} download>
                        <Download size={13} />
                        {resource.title}
                      </a>
                    ))}
                  </details>
                ) : null}
              </div>
            ) : (
              messages.map((message) => (
                <div
                  className={`assistant-message ${message.role}`}
                  key={message.id}
                >
                  <span className="assistant-speaker">
                    {message.role === "user" ? (
                      "You"
                    ) : (
                      <>
                        <Sparkles size={12} /> Quanta assistant
                      </>
                    )}
                  </span>
                  {message.role === "user" ? (
                    <p className="assistant-user-text">{message.content}</p>
                  ) : (
                    <>
                      <div className="assistant-markdown">
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          components={{
                            img: () => null,
                            a: ({ children, href }) => (
                              <a href={href} target="_blank" rel="noreferrer">
                                {children}
                              </a>
                            ),
                          }}
                        >
                          {message.content}
                        </ReactMarkdown>
                      </div>
                      {message.files.length ? (
                        <AssistantFiles
                          files={message.files}
                          language={
                            lesson
                              ? (lesson.codeLanguage ?? "python")
                              : undefined
                          }
                          onApply={
                            onApply
                              ? (code) => {
                                  onApply(code);
                                  setNotice(
                                    "Code added to your lesson editor. Close the assistant to review it.",
                                  );
                                }
                              : undefined
                          }
                        />
                      ) : null}
                    </>
                  )}
                </div>
              ))
            )}
            {busy ? (
              <div className="assistant-thinking" role="status">
                <LoaderCircle size={15} className="spin" />{" "}
                {mode === "environment"
                  ? "Preparing your project files…"
                  : "Working through your question…"}
              </div>
            ) : null}
            <div ref={bottom} />
          </div>
          <div className="assistant-composer">
            {connection !== "ready" ? (
              <div className="assistant-connection" role="status">
                <p>
                  {connection === "loading"
                    ? "Connecting to the assistant…"
                    : connection === "disabled"
                      ? "The AI assistant isn’t connected yet. Your course templates and downloads are ready to use."
                      : "The assistant could not connect. Check your connection and try again."}
                </p>
                {connection !== "loading" ? (
                  <button
                    className="text-link"
                    onClick={() => setConnectionVersion((v) => v + 1)}
                  >
                    Check connection again
                  </button>
                ) : null}
              </div>
            ) : null}
            {error ? (
              <p className="error-message" role="alert">
                {error} Your question has been kept below.
              </p>
            ) : null}
            {notice ? (
              <p className="assistant-notice" role="status">
                {notice}
              </p>
            ) : null}
            <form
              onSubmit={(event) => {
                event.preventDefault();
                void send(input);
              }}
            >
              <div className="assistant-options">
                <label>
                  Help with
                  <select
                    aria-label="Assistant help mode"
                    value={mode}
                    disabled={busy}
                    onChange={(event) =>
                      setMode(event.target.value as AssistantMode)
                    }
                  >
                    <option value="hint">Understanding</option>
                    <option value="environment">Environment setup</option>
                    <option value="code">Writing code</option>
                  </select>
                </label>
                {mode === "environment" ? (
                  <label>
                    Your computer
                    <select
                      aria-label="Environment operating system"
                      value={platform}
                      disabled={busy}
                      onChange={(event) =>
                        setPlatform(event.target.value as Platform)
                      }
                    >
                      <option value="macos">macOS</option>
                      <option value="windows">Windows</option>
                      <option value="linux">Linux</option>
                    </select>
                  </label>
                ) : null}
              </div>
              <div className="assistant-input-wrap">
                <textarea
                  ref={textarea}
                  aria-label="Message the course assistant"
                  placeholder="What are you stuck on? Paste an error or describe what you want to build…"
                  value={input}
                  maxLength={4000}
                  rows={3}
                  disabled={busy}
                  onChange={(event) => setInput(event.target.value)}
                  onKeyDown={(event) => {
                    if (
                      event.key === "Enter" &&
                      !event.shiftKey &&
                      !event.nativeEvent.isComposing
                    ) {
                      event.preventDefault();
                      void send(input);
                    }
                  }}
                />
                {busy ? (
                  <button
                    key="stop"
                    type="button"
                    className="assistant-send"
                    aria-label="Stop assistant response"
                    onClick={(event) => {
                      event.preventDefault();
                      stop();
                    }}
                  >
                    <Square size={16} />
                  </button>
                ) : (
                  <button
                    key="send"
                    type="submit"
                    className="assistant-send"
                    aria-label="Send assistant message"
                    disabled={!input.trim() || connection !== "ready"}
                  >
                    <ArrowUp size={18} />
                  </button>
                )}
              </div>
              {lesson ? (
                <label className="assistant-share">
                  <input
                    type="checkbox"
                    checked={includeCode}
                    disabled={busy}
                    onChange={(event) => setIncludeCode(event.target.checked)}
                  />{" "}
                  Include editor code & last run error
                </label>
              ) : null}
              <p className="assistant-fine-print">
                Your message, recent chat, lesson
                {includeCode && lesson ? ", and included code" : ""} are sent
                through OpenRouter. Keep secrets out of chat.{" "}
                {storageError
                  ? "Chat could not be saved in this tab."
                  : "Recent chat stays in this browser tab."}
              </p>
            </form>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
