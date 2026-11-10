# Portable installation

## Online preparation

Install Node.js 18+ (tested here with 24.3.0). In this directory:

```sh
npm ci --ignore-scripts --no-audit --no-fund
node scripts/doctor.mjs
```

Use the lockfile for reproducible versions. Copy the whole skill including `node_modules` to the offline computer. Keep dependency LICENSE files. `node_modules` is intentionally excluded from Git; the separately generated offline ZIP includes it.

## Offline computer

Requires a compatible local Node.js installation and the fonts used in the slides. Node.js itself and fonts are not bundled. Run `node scripts/doctor.mjs` in the copied directory. Example:

```sh
node scripts/build.mjs examples/demo.json my-demo.pptx
```

No network request is made by doctor or build when all assets are local. Opening and rendering requires PowerPoint or LibreOffice. Package inspection additionally uses Python 3 with standard library only. PowerPoint rendering uses Windows PowerShell and the locally installed PowerPoint COM automation interface; it does not install Office.

Offline generation means running prepared scripts and scenes. A remote AI service or image API still requires a network; to author via an offline Agent, separately supply a suitable local model and agent environment. `chatgpt-imagegen` is a separate skill, not included or invoked implicitly by this package.

If a local `.codex/skills/presentations-pptxgenjs` already exists, use a separate directory or back it up before replacing. Restart the agent session for skill discovery.
