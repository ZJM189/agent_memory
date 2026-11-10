---
name: presentations-pptxgenjs
description: Create editable PPTX files with public PptxGenJS, including rebuilding reference slide images as separate text, chart, table, shape and image elements. Use for portable or offline PowerPoint authoring without the Codex artifact runtime.
---

# Editable PowerPoint with PptxGenJS

Use this skill's PptxGenJS installation. It does not use `@oai/artifact-tool` or a proprietary Codex runtime. Offline generation requires Node.js and this directory's installed dependencies; AI authoring and image generation require their own available models or services.

## Set up

Run `node <skill-dir>/scripts/doctor.mjs`. If dependencies are absent and network access is available, run `npm ci --ignore-scripts --no-audit --no-fund` in the skill directory. For an offline machine, copy the prepared whole directory including `node_modules`; do not run npm there. See [portable installation](references/portable.md).

## Author and rebuild

1. Read the user's material, inspect each reference image, and transcribe all content. Preserve the requested count, layout, data, font treatment and exact wording. For reference reconstruction, use pixel coordinates scaled into slide inches: `xIn = xPx / imageWidth * slideWidthIn`; same for y, width and height. Do not silently stretch or redesign a reference.
2. Write a UTF-8 JSON scene in the user's workspace following [scene format](references/scene.md). Objects are ordered back to front. Text must be in editable text boxes; tables, charts and requested editable diagrams must be native PPT objects. Use source-cropped PNG only for icons, illustrations, gradients or textures. Do not put a complete reference screenshot under editable text: original glyphs will remain underneath. Remove the old text, preserving its background, before reusing a raster region. If the user permits a raster-only region, disclose it.
3. Keep all image assets next to the scene with relative paths. Image generation is optional: when the user requests `chatgpt-imagegen`, use that separate skill and its local config. Never copy provider keys into this skill, JSON scenes, output, repository or offline bundle. Confirm the resulting image exists and inspect it before deriving a deck from it. Do not claim a generated image is editable.
4. Run `node <skill-dir>/scripts/build.mjs <scene.json> <new-output.pptx>`. The output and scene are user artifacts, not files to place inside the installed skill. Existing outputs are rejected; choose a revision filename.
5. Run `python <skill-dir>/scripts/inspect_pptx.py <output.pptx>` to check package integrity, slide count, object types, chart values, and embedded workbooks. The report does not validate visual fidelity or text clipping.
6. Render with PowerPoint on Windows using `scripts/render.ps1`, or with an installed LibreOffice and a PDF rasterizer. Inspect every page against the reference. Check small labels, line breaks, all edges, chart axes and the full text inventory; repair and render again. If no renderer is available, state that visual verification is incomplete. Do not claim pixel-identical reconstruction merely because structural checks pass.

## Practical layout rules

Use the reference's slide proportions. Default new decks to 16:9, 13.3333 × 7.5 inches. PptxGenJS text sizes are points, coordinates are inches, colors are RGB hex without `#`. Set an installed font explicitly. Reserve height for descenders and Chinese punctuation; do not rely solely on automatic shrink fitting. Avoid negative coordinates and out-of-slide objects. Use explicit data rather than rasterized chart labels. Maintain the reference style ahead of generic design preferences.

The bundled example is a source for a single demonstration slide, not a required template. For complex charts, custom connectors, rich text and features outside the JSON builder, write a `.cjs` script using `require('<skill-dir>/node_modules/pptxgenjs')` and consult the installed package's README and `types/index.d.ts`. Do not invent API options. PptxGenJS creates new decks; it does not provide full-fidelity arbitrary PPTX import/editing. Rebuild needed elements and explain that limitation when editing existing decks.

## Deliver

Return the final PPTX and preview. If the user requested separated assets, also package the scene and images. Distinguish editable objects from raster assets, report meaningful limitations, and keep intermediate diagnostics private unless requested. Preserve dependency licenses when distributing this skill. See [README](README.md) for installation and offline boundaries.
