import Editor, { loader } from "@monaco-editor/react";
import * as monaco from "monaco-editor/esm/vs/editor/editor.api";
import "monaco-editor/esm/vs/basic-languages/python/python.contribution";
import EditorWorker from "monaco-editor/esm/vs/editor/editor.worker?worker";
import { useEffect, useState } from "react";
(
  self as unknown as { MonacoEnvironment: { getWorker: () => Worker } }
).MonacoEnvironment = { getWorker: () => new EditorWorker() };
loader.config({ monaco });
export default function CodeEditor({
  code,
  onChange,
  onRun,
}: {
  code: string;
  onChange: (code: string) => void;
  onRun: () => void;
}) {
  const [dark, setDark] = useState(
    document.documentElement.dataset.theme === "dark",
  );
  useEffect(() => {
    const observer = new MutationObserver(() =>
      setDark(document.documentElement.dataset.theme === "dark"),
    );
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["data-theme"],
    });
    return () => observer.disconnect();
  }, []);
  return (
    <Editor
      height="290px"
      language="python"
      value={code}
      onChange={(value) => onChange(value || "")}
      theme={dark ? "vs-dark" : "vs"}
      loading={<div className="loading-state">Loading Python editor…</div>}
      options={{
        fontSize: 12,
        fontFamily: "JetBrains Mono, monospace",
        minimap: { enabled: false },
        padding: { top: 18, bottom: 14 },
        scrollBeyondLastLine: false,
        lineNumbersMinChars: 3,
        wordWrap: "on",
        tabSize: 4,
        automaticLayout: true,
        overviewRulerLanes: 0,
        hideCursorInOverviewRuler: true,
        renderLineHighlight: "none",
        ariaLabel: "Python strategy editor",
      }}
      onMount={(editor) => {
        editor.addAction({
          id: "quanta-run",
          label: "Run experiment",
          keybindings: [monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter],
          run: onRun,
        });
      }}
    />
  );
}
