import { describe, expect, it } from "vitest";
import React from "react";
import ReactDOMServer from "react-dom/server";
import MarkdownRenderer, { normalizeMarkdownMath } from "./MarkdownRenderer";

describe("normalizeMarkdownMath", () => {
  it("normalizes the user reported sentence without breaking inline math or currency", () => {
    const input =
      "Here $c$ is the flat commission per order ($1 by default), $s$ is slippage in basis points (2 bps default), $\\sigma$ is the bid-ask spread in basis points (2 bps default), and $\\pi$ is the volume participation cap (0.01 or 1% default). One basis point (bps) equals 0.01% (1/10,000). Every new run creates a fresh $100,000 account; it never resets your existing account in place. Earlier runs are safely preserved in your run history for review and CSV export.";

    const output = normalizeMarkdownMath(input);

    // Math symbols remain unescaped
    expect(output).toContain("$c$");
    expect(output).toContain("$s$");
    expect(output).toContain("$\\sigma$");
    expect(output).toContain("$\\pi$");

    // Currency values are escaped so remark-math does not treat them as math opening delimiters
    expect(output).toContain("(\\$1 by default)");
    expect(output).toContain("fresh \\$100,000 account");
  });

  it("escapes currency in calculations with arithmetic operators", () => {
    const line1 =
      "1. Spread and slippage drag: 10 × ($148.54 − $148.46) = $0.80.";
    const line2 = "2. Commission drag: 2 × $1.00 = $2.00.";

    expect(normalizeMarkdownMath(line1)).toBe(
      "1. Spread and slippage drag: 10 × (\\$148.54 − \\$148.46) = \\$0.80.",
    );
    expect(normalizeMarkdownMath(line2)).toBe(
      "2. Commission drag: 2 × \\$1.00 = \\$2.00.",
    );
  });

  it("preserves math expressions that start with numbers", () => {
    const math1 = "Accounting for the $5\\text{ bps}$ commission";
    const math2 =
      "total cash outlay per share is $101.0303 \\times 1.0005 \\approx \\$101.0808$.";
    const math3 = "Value of $0.05$ or $100$ shares";

    expect(normalizeMarkdownMath(math1)).toBe(math1);
    // The leading $101 stays math; only the inner \$, which would close the span,
    // becomes \text{\textdollar}.
    expect(normalizeMarkdownMath(math2)).toBe(
      "total cash outlay per share is $101.0303 \\times 1.0005 \\approx \\text{\\textdollar}101.0808$.",
    );
    expect(normalizeMarkdownMath(math3)).toBe(math3);
  });

  it("preserves display math and code blocks without escaping inside them", () => {
    const code = "```python\nprice = 100\n$$x$$\n```\n$$P = \\frac{1}{2}$$";
    // Nothing inside the code fence changes; the one-line equation only gets its
    // fences on their own lines, which is what makes it render as display math.
    expect(normalizeMarkdownMath(code)).toBe(
      "```python\nprice = 100\n$$x$$\n```\n$$\nP = \\frac{1}{2}\n$$",
    );
  });
});

describe("MarkdownRenderer", () => {
  it("renders math with KaTeX and currency as plain text", () => {
    const text =
      "Here $c$ is the flat commission per order ($1 by default), $s$ is slippage in basis points (2 bps default), $\\sigma$ is the bid-ask spread in basis points (2 bps default), and $\\pi$ is the volume participation cap (0.01 or 1% default). Every new run creates a fresh $100,000 account.";

    const html = ReactDOMServer.renderToStaticMarkup(
      React.createElement(MarkdownRenderer, { content: text }),
    );

    // KaTeX elements should be present
    expect(html).toContain('class="katex"');
    expect(html).toContain('encoding="application/x-tex">c</annotation>');
    expect(html).toContain('encoding="application/x-tex">s</annotation>');
    expect(html).toContain('encoding="application/x-tex">\\sigma</annotation>');
    expect(html).toContain('encoding="application/x-tex">\\pi</annotation>');

    // Text content should contain literal $1 and $100,000
    expect(html).toContain("($1 by default)");
    expect(html).toContain("$100,000 account");
  });

  it("renders escaped dollars and escaped percent signs inside inline math", () => {
    // Lesson text writes prices as $\$15.00$ and percentages as $2.4\%$. The first
    // used to close the math span at the inner "$"; the second had its opening "$"
    // mistaken for a price. Both left a KaTeX parse error on the page.
    const text =
      "A long position of $\\$15.00$ and a short of $-\\$18.00$ in $y$. Store $0.024$ for $2.4\\%$, not $2.4$.";

    const html = ReactDOMServer.renderToStaticMarkup(
      React.createElement(MarkdownRenderer, { content: text }),
    );

    expect(html).not.toContain("katex-error");
    expect(html).toContain(
      'encoding="application/x-tex">\\text{\\textdollar}15.00</annotation>',
    );
    expect(html).toContain(
      'encoding="application/x-tex">-\\text{\\textdollar}18.00</annotation>',
    );
    expect(html).toContain('encoding="application/x-tex">2.4\\%</annotation>');
    expect(html).toContain('encoding="application/x-tex">0.024</annotation>');
  });

  it("renders a one-line $$...$$ equation as display math", () => {
    const text =
      "A return.\n\n$$R = \\frac{\\text{end} - \\text{start}}{\\text{start}}$$\n\nInline $x$ stays inline.";
    const html = ReactDOMServer.renderToStaticMarkup(
      React.createElement(MarkdownRenderer, { content: text }),
    );
    expect(html.match(/class="katex-display"/g)).toHaveLength(1);
    expect(html).not.toContain("katex-error");
  });

  it("supports inline mode without wrapping in <p>", () => {
    const html = ReactDOMServer.renderToStaticMarkup(
      React.createElement(MarkdownRenderer, {
        content: "What is $\\sigma$?",
        inline: true,
      }),
    );
    expect(html.startsWith("<p>")).toBe(false);
    expect(html).toContain('class="katex"');
    expect(html).toContain('encoding="application/x-tex">\\sigma</annotation>');
  });
});
