import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
export default defineConfig({
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
      "@content": fileURLToPath(new URL("../content", import.meta.url)),
    },
  },
  plugins: [react(), tailwindcss()],
  server: {
    fs: {
      allow: [".", "../content/catalog", "../node_modules"].map((directory) =>
        fileURLToPath(new URL(directory, import.meta.url)),
      ),
    },
    proxy: { "/api": process.env.API_TARGET || "http://127.0.0.1:8000" },
  },
  preview: {
    proxy: { "/api": process.env.API_TARGET || "http://127.0.0.1:8000" },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          math: ["katex", "react-markdown", "remark-math", "rehype-katex"],
          charts: ["lightweight-charts", "recharts"],
        },
      },
    },
  },
});
