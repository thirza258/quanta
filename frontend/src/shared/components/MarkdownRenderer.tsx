import type { ComponentProps, ReactNode } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";

/**
 * Preprocesses markdown text so that currency amounts like `$100,000`, `($1 by default)`,
 * `$148.50`, etc. are escaped to `\$` while preserving legitimate LaTeX math formulas:
 * - Display math: `$$...$$`
 * - Inline math: `$c$`, `$s$`, `$\sigma$`, `$\pi$`, `$f = \frac{...}{...}$`
 * - Math starting with numbers: `$5\text{ bps}$`, `$101.0303 \times 1.0005 \approx \$101.0808$`
 * - Lone numeric values in math: `$0.05$`, `$100$`
 * Also preserves code fences and inline code.
 */
export function normalizeMarkdownMath(text: string): string {
  if (!text) return text;

  // Protect code blocks (```...```), inline code (`...`), and display math ($$...$$)
  const segments: { isProtected: boolean; text: string }[] = [];
  let lastIndex = 0;
  const protectRegex = /(```[\s\S]*?```|`[^`\n]*`|\$\$[\s\S]*?\$\$)/g;
  let match: RegExpExecArray | null;

  while ((match = protectRegex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      segments.push({
        isProtected: false,
        text: text.slice(lastIndex, match.index),
      });
    }
    segments.push({ isProtected: true, text: match[0] });
    lastIndex = protectRegex.lastIndex;
  }
  if (lastIndex < text.length) {
    segments.push({ isProtected: false, text: text.slice(lastIndex) });
  }

  return segments
    .map((seg) => {
      if (seg.isProtected) return seg.text;

      // 1. Fix unescaped % and unicode dashes inside inline math $...$
      let processed = seg.text.replace(
        /(?<!\\)\$([^$\n]+?)(?<!\\)\$/g,
        (_m, mathContent: string) => {
          let fixed = mathContent.replace(/–/g, "-").replace(/—/g, " - ");
          fixed = fixed.replace(/(?<!\\)%/g, "\\%");
          return "$" + fixed + "$";
        },
      );

      // 2. Escape currency dollar signs (e.g. $100,000, ($1 by default), $148.50, $2.80)
      processed = processed.replace(
        /(?<!\\)\$(?!\$)([0-9][0-9,]*(?:\.[0-9]+)?(?:[kKmMbB]|(?:\s*(?:million|billion|trillion|thousand)))?)/g,
        (fullMatch, numPart, offset: number, fullStr: string) => {
          const rest = fullStr.slice(offset + fullMatch.length);

          // If immediately followed by $, it is math like $100$ or $0.05$
          if (rest.startsWith("$")) {
            return fullMatch;
          }

          // Check if there is a closing $ on the same line
          const nextNewline = rest.indexOf("\n");
          const lineRest =
            nextNewline === -1 ? rest : rest.slice(0, nextNewline);

          const dollarIndices: number[] = [];
          const dollarRegex = /(?<!\\)\$/g;
          let dMatch: RegExpExecArray | null;
          while ((dMatch = dollarRegex.exec(lineRest)) !== null) {
            dollarIndices.push(dMatch.index);
          }

          if (dollarIndices.length === 0) {
            // No closing $ on this line -> definitely currency
            return "\\$" + numPart;
          }

          // If the very next $ is immediately followed by a digit (e.g. $148 - $146 or $100 to $200):
          // then the next $ is also currency, not a closing math delimiter!
          const firstNextDollarIdx = dollarIndices[0];
          const afterNextDollar = lineRest.slice(firstNextDollarIdx + 1);
          if (/^[0-9]/.test(afterNextDollar)) {
            return "\\$" + numPart;
          }

          // Check content between here and the closing $
          const between = lineRest.slice(0, firstNextDollarIdx);
          const hasMathCommand = /\\[a-zA-Z]+/.test(between);
          const hasMathSymbol = /[=<>^_+\-]/.test(between);
          const hasEnglishWords = /[a-zA-Z]{3,}/.test(
            between.replace(/\\[a-zA-Z]+/g, ""),
          );

          if (!hasMathCommand && !hasMathSymbol) {
            return "\\$" + numPart;
          }
          if (hasEnglishWords && !hasMathCommand) {
            return "\\$" + numPart;
          }

          return fullMatch;
        },
      );

      return processed;
    })
    .join("");
}

export interface MarkdownRendererProps {
  content: string;
  className?: string;
  inline?: boolean;
  components?: ComponentProps<typeof ReactMarkdown>["components"];
}

export default function MarkdownRenderer({
  content,
  className,
  inline = false,
  components,
}: MarkdownRendererProps) {
  const normalized = normalizeMarkdownMath(content);

  const defaultComponents: ComponentProps<typeof ReactMarkdown>["components"] =
    {
      table: ({ children }: { children?: ReactNode }) => (
        <div
          className="prose-table"
          role="region"
          aria-label="Lesson table"
          tabIndex={0}
        >
          <table>{children}</table>
        </div>
      ),
      a: ({ children, href }: { children?: ReactNode; href?: string }) => {
        const isExternal =
          href?.startsWith("http://") || href?.startsWith("https://");
        return (
          <a
            href={href}
            target={isExternal ? "_blank" : undefined}
            rel={isExternal ? "noopener noreferrer" : undefined}
          >
            {children}
          </a>
        );
      },
      ...(inline
        ? {
            p: ({ children }: { children?: ReactNode }) => <>{children}</>,
          }
        : {}),
      ...components,
    };

  const rendered = (
    <ReactMarkdown
      remarkPlugins={[remarkMath, remarkGfm]}
      rehypePlugins={[[rehypeKatex, { strict: false, throwOnError: false }]]}
      components={defaultComponents}
    >
      {normalized}
    </ReactMarkdown>
  );

  if (className) {
    return inline ? (
      <span className={className}>{rendered}</span>
    ) : (
      <div className={className}>{rendered}</div>
    );
  }

  return rendered;
}
