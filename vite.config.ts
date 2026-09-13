import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
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
