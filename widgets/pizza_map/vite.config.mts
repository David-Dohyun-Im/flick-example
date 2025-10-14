import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  build: {
    lib: {
      entry: "./index.jsx",
      formats: ["es"],
      fileName: "pizza-map",
    },
    outDir: "../../assets",
    rollupOptions: {
      external: ["react", "react-dom"],
    },
  },
});

