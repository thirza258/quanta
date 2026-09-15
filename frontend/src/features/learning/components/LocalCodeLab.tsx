import type { Lesson } from "@/features/learning/model/types";
import { useWorkspace } from "@/features/workspace/WorkspaceProvider";
import CodeEditor from "@/shared/components/CodeEditor";
import { download } from "@/shared/lib/download";
import { Code2, Download, RotateCcw } from "lucide-react";

export default function LocalCodeLab({ lesson }: { lesson: Lesson }) {
  const { state, update } = useWorkspace();
  const code = state.drafts[lesson.id] ?? lesson.code;
  const filename = `lesson-${lesson.id.replace(".", "-")}`;
  return (
    <section className="local-code-lab" aria-label="Local C laboratory">
      <div className="local-code-heading">
        <Code2 size={20} />
        <div>
          <h2>C laboratory</h2>
          <p>Edit here. Compile and run on your computer.</p>
        </div>
      </div>
      <div className="local-code-editor">
        <CodeEditor
          code={code}
          language="c"
          onChange={(draft) =>
            update((s) => ({
              ...s,
              drafts: { ...s.drafts, [lesson.id]: draft },
            }))
          }
        />
      </div>
      <div className="local-code-actions">
        <button
          className="button primary small"
          onClick={() => download(`${filename}.c`, code, "text/x-csrc")}
        >
          <Download size={15} /> Download C source
        </button>
        <button
          className="button secondary small"
          disabled={code === lesson.code}
          onClick={() =>
            update((s) => ({
              ...s,
              drafts: { ...s.drafts, [lesson.id]: lesson.code },
            }))
          }
        >
          <RotateCcw size={14} /> Reset template
        </button>
      </div>
      <p className="local-code-save">
        Edits save to your workspace. Download again after making changes.
      </p>
      <h3>Compile and run</h3>
      <p>
        In a terminal, open the folder containing your downloaded file. Use a
        C17 compiler on macOS, Linux, or Windows through WSL.
      </p>
      <pre aria-label="C compile commands">
        <code>{`cc -std=c17 -Wall -Wextra -Werror -O2 ${filename}.c -o ${filename}\n./${filename}`}</code>
      </pre>
      {lesson.expectedOutput ? (
        <details>
          <summary>Expected output from the original template</summary>
          <pre>{lesson.expectedOutput}</pre>
        </details>
      ) : null}
      <h3>Full C & HPC project</h3>
      <p>
        Build the serial and POSIX-thread backtests, run correctness and
        sanitizer checks, then compare repeated timings and every result row.
      </p>
      <a
        className="text-link"
        href="/course-assets/c-hpc-trading/c-hpc-bot-lab.zip"
        download
      >
        <Download size={15} /> Download C/HPC bot lab
      </a>
      <pre>
        <code>{"make\nmake test\nmake sanitize\n./quanta-bot 4 200000"}</code>
      </pre>
      <p>
        <a href="/course-assets/c-hpc-trading/README.md" download>
          Build guide
        </a>{" "}
        ·{" "}
        <a href="/course-assets/c-hpc-trading/performance-notebook.md" download>
          Performance notebook and rubric
        </a>
      </p>
    </section>
  );
}
