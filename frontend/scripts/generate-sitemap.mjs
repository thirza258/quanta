import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const candidateCurriculumPaths = [
  path.resolve(__dirname, "../../content/catalog/curriculum.json"),
  path.resolve(__dirname, "../content/catalog/curriculum.json"),
  path.resolve(process.cwd(), "content/catalog/curriculum.json"),
  path.resolve(process.cwd(), "../content/catalog/curriculum.json"),
];

const curriculumPath = candidateCurriculumPaths.find((p) => fs.existsSync(p));
if (!curriculumPath) {
  console.error("Could not find curriculum.json in any expected path.");
  process.exit(1);
}

const rawCatalog = fs.readFileSync(curriculumPath, "utf-8");
const tracks = JSON.parse(rawCatalog);

const rawBaseUrl = process.env.SITE_URL || "https://quant.nevatal.id";
const baseUrl = rawBaseUrl.replace(/\/+$/, "");
const lastmod = new Date().toISOString().slice(0, 10);

const urls = [
  { loc: `${baseUrl}/`, changefreq: "weekly", priority: "1.0" },
  { loc: `${baseUrl}/curriculum`, changefreq: "weekly", priority: "0.9" },
  { loc: `${baseUrl}/simulator`, changefreq: "weekly", priority: "0.8" },
  { loc: `${baseUrl}/lab`, changefreq: "weekly", priority: "0.8" },
  { loc: `${baseUrl}/notebook`, changefreq: "monthly", priority: "0.7" },
  { loc: `${baseUrl}/experiments`, changefreq: "monthly", priority: "0.7" },
  { loc: `${baseUrl}/library`, changefreq: "monthly", priority: "0.7" },
  { loc: `${baseUrl}/resources`, changefreq: "monthly", priority: "0.7" },
  { loc: `${baseUrl}/methodology`, changefreq: "monthly", priority: "0.7" },
  { loc: `${baseUrl}/privacy`, changefreq: "monthly", priority: "0.5" },
  { loc: `${baseUrl}/terms`, changefreq: "monthly", priority: "0.5" },
];

for (const track of tracks) {
  if (track.id) {
    urls.push({
      loc: `${baseUrl}/curriculum/${encodeURIComponent(track.id)}`,
      changefreq: "weekly",
      priority: "0.8",
    });
  }

  for (const mod of track.modules || []) {
    if (mod.id) {
      urls.push({
        loc: `${baseUrl}/learn/${encodeURIComponent(mod.id)}`,
        changefreq: "monthly",
        priority: "0.6",
      });
    }
  }

  for (const exam of track.exams || []) {
    if (exam.id) {
      urls.push({
        loc: `${baseUrl}/exams/${encodeURIComponent(exam.id)}`,
        changefreq: "monthly",
        priority: "0.5",
      });
    }
  }
}

function xmlEscape(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/'/g, "&apos;")
    .replace(/"/g, "&quot;")
    .replace(/>/g, "&gt;")
    .replace(/</g, "&lt;");
}

const xmlLines = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
];

for (const entry of urls) {
  xmlLines.push("  <url>");
  xmlLines.push(`    <loc>${xmlEscape(entry.loc)}</loc>`);
  xmlLines.push(`    <lastmod>${lastmod}</lastmod>`);
  xmlLines.push(`    <changefreq>${entry.changefreq}</changefreq>`);
  xmlLines.push(`    <priority>${entry.priority}</priority>`);
  xmlLines.push("  </url>");
}

xmlLines.push("</urlset>\n");

const xmlContent = xmlLines.join("\n");

const candidateOutDirs = [
  path.resolve(__dirname, "../public"),
  path.resolve(process.cwd(), "frontend/public"),
  path.resolve(process.cwd(), "public"),
];

let targetDir = candidateOutDirs.find((d) => fs.existsSync(d));
if (!targetDir) {
  targetDir = path.resolve(__dirname, "../public");
  fs.mkdirSync(targetDir, { recursive: true });
}

const targetFile = path.join(targetDir, "sitemap.xml");
fs.writeFileSync(targetFile, xmlContent, "utf-8");

console.log(
  `Generated ${urls.length} URLs in sitemap for ${baseUrl} -> ${targetFile}`,
);
