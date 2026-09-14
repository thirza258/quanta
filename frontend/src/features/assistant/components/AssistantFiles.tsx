import { useState } from "react";
import { Check, Copy, Download, FileCode2, Undo2 } from "lucide-react";
import type { AssistantFile } from "../model";
import { canApply } from "../model";
import { download } from "@/shared/lib/download";

export default function AssistantFiles({
  files,
  language,
  onApply,
}: {
  files: AssistantFile[];
  language?: "python" | "c";
  onApply?: (code: string) => void;
}) {
  const [copied, setCopied] = useState("");
  const [error, setError] = useState("");
  const [downloading, setDownloading] = useState(false);
  async function copy(file: AssistantFile) {
    try {
      await navigator.clipboard.writeText(file.content);
      setCopied(file.path);
      setError("");
    } catch {
      setError(
        "Copy is unavailable. Download the file or select its contents below.",
      );
    }
  }
  async function downloadBundle() {
    setDownloading(true);
    setError("");
    try {
      const response = await fetch("/api/v1/assistant/bundle", {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ files }),
        signal: AbortSignal.timeout(20000),
      });
      if (!response.ok)
        throw new Error(
          "The project download failed. Try again or download files individually.",
        );
      const url = URL.createObjectURL(await response.blob());
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = "quanta-project.zip";
      anchor.click();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setDownloading(false);
    }
  }
  return (
    <div className="assistant-files">
      <div className="assistant-file-heading">
        <strong>
          {files.length} {files.length === 1 ? "file" : "files"} to review
        </strong>
        <button
          className="text-link"
          disabled={downloading}
          onClick={() => void downloadBundle()}
        >
          <Download size={14} />{" "}
          {downloading ? "Preparing…" : "Download project ZIP"}
        </button>
      </div>
      {files.map((file) => (
        <details className="assistant-file" key={file.path}>
          <summary>
            <FileCode2 size={15} />
            <span>{file.path}</span>
            <small>
              {file.target === "local" ? "Local project" : "Lesson code"}
            </small>
          </summary>
          <pre>
            <code>{file.content}</code>
          </pre>
          <div className="assistant-file-actions">
            <button
              className="button secondary small"
              onClick={() => void copy(file)}
            >
              {copied === file.path ? <Check size={13} /> : <Copy size={13} />}
              {copied === file.path ? "Copied" : "Copy"}
            </button>
            <button
              className="button secondary small"
              onClick={() =>
                download(
                  file.path.split("/").at(-1)!,
                  file.content,
                  "text/plain;charset=utf-8",
                )
              }
            >
              <Download size={13} /> Download file
            </button>
            {onApply && canApply(file, language) ? (
              <button
                className="button primary small"
                onClick={() => onApply(file.content)}
              >
                <Undo2 size={13} /> Use in lesson editor
              </button>
            ) : null}
          </div>
        </details>
      ))}
      <p className="assistant-fine-print">
        Review generated files before running them. Local project files run on
        your computer.
      </p>
      {error ? (
        <p role="alert" className="error-message">
          {error}
        </p>
      ) : null}
    </div>
  );
}
