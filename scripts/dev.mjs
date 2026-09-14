import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { createServer } from "node:net";
import { fileURLToPath } from "node:url";
import { resolve } from "node:path";
import { loadEnvFile } from "node:process";
const root = fileURLToPath(new URL("..", import.meta.url));
process.chdir(root);
if (existsSync(resolve(root, ".env"))) loadEnvFile(resolve(root, ".env"));
const python =
  process.platform === "win32"
    ? "backend/.venv/Scripts/python.exe"
    : "backend/.venv/bin/python";
if (!existsSync(python)) {
  console.error("Run npm run setup first to install the API environment.");
  process.exit(1);
}
async function available(start, explicit) {
  for (let port = start; port < start + 30; port++) {
    const free = await new Promise((resolve) => {
      const server = createServer();
      server.once("error", () => resolve(false));
      server.listen(port, "127.0.0.1", () => server.close(() => resolve(true)));
    });
    if (free) return port;
    if (explicit) throw new Error(`Requested port ${port} is already in use.`);
  }
  throw new Error("No development port available.");
}
const apiPort = await available(
  Number(process.env.API_PORT || 8000),
  !!process.env.API_PORT,
);
const webPort = await available(
  Number(process.env.VITE_PORT || 5173),
  !!process.env.VITE_PORT,
);
const env = {
  ...process.env,
  API_TARGET: `http://127.0.0.1:${apiPort}`,
  ALLOWED_ORIGINS: [
    ...new Set([
      ...(process.env.ALLOWED_ORIGINS || "").split(",").filter(Boolean),
      `http://127.0.0.1:${webPort}`,
      `http://localhost:${webPort}`,
    ]),
  ].join(","),
};
const api = spawn(
  python,
  [
    "-m",
    "uvicorn",
    "quanta.main:app",
    "--app-dir",
    "backend",
    "--reload",
    "--reload-dir",
    "backend/quanta",
    "--reload-dir",
    "content/catalog",
    "--reload-include",
    "*.json",
    "--host",
    "127.0.0.1",
    "--port",
    String(apiPort),
  ],
  { stdio: "inherit", env },
);
let closing = false,
  web;
function close(code = 0) {
  if (closing) return;
  closing = true;
  api.kill("SIGTERM");
  web?.kill("SIGTERM");
  setTimeout(() => process.exit(code), 500);
}
for (const signal of ["SIGINT", "SIGTERM"]) process.on(signal, () => close());
api.on("exit", (code) => {
  if (!closing) close(code || 0);
});
api.on("error", (error) => {
  console.error(error.message);
  close(1);
});
console.log("Starting Quanta API…");
let healthy = false;
for (let attempt = 0; attempt < 120 && !closing; attempt++) {
  try {
    const response = await fetch(`${env.API_TARGET}/api/v1/health`, {
      signal: AbortSignal.timeout(1000),
    });
    if (response.ok) {
      healthy = true;
      break;
    }
  } catch {}
  await new Promise((resolve) => setTimeout(resolve, 500));
}
if (!healthy) {
  console.error("API did not become ready. Check the error above.");
  close(1);
} else if (!closing) {
  web = spawn(
    "node",
    [
      resolve(root, "node_modules/vite/bin/vite.js"),
      "--host",
      "127.0.0.1",
      "--port",
      String(webPort),
      "--strictPort",
    ],
    { stdio: "inherit", env, cwd: resolve(root, "frontend") },
  );
  web.on("exit", (code) => {
    if (!closing) close(code || 0);
  });
  web.on("error", (error) => {
    console.error(error.message);
    close(1);
  });
  console.log(
    `Quanta: http://127.0.0.1:${webPort} · API: ${env.API_TARGET}/docs`,
  );
}
