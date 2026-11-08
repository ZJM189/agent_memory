---
name: chatgpt-imagegen
description: Generate images through a user-configured OpenAI-compatible image API, including OToken and reference-image edits. Use when the user requests this configured third-party API or this skill.
---

# Configured image API

Use `scripts/imagegen.py` for image generation or reference-image edits through the configured provider. The provider receives the prompt and any reference images. Model availability, image sizes, and billing depend on that provider; the model ID does not establish the underlying model's identity.

1. Check `config.json` in this skill folder exists and contains `base_url`, `api_key`, and `model`. If absent, copy `config.example.json` to `config.json` and ask the user to fill it in locally. Never print the config or API key, include it in generated output, or commit it. Do not reuse keys from previous conversations.
2. Write each prompt as UTF-8 text in the user's workspace. Include exact requested text, format, style, and relevant reference roles. For slide sets, write one prompt per slide and use consistent reference images; check the final text and layout visually against the source, because image models may distort text.
3. Run the script with `--prompt-file`, `--output`, and optionally `--reference` for a reference image. Use the user's requested output location, or `output/imagegen/` in the workspace. Do not overwrite existing images without explicit approval. Review the generated image, and deliver its path. Do not claim editability for generated raster images.

Example (replace paths):

```sh
python <skill-dir>/scripts/imagegen.py --prompt-file slide.txt --reference style.png --output output/imagegen/slide-01.png
```

Without `--reference`, the script calls `images/generations`; with it, `images/edits` using multipart form data. It accepts common `b64_json`, `base64`, `b64`, `url`, and `image_url` response fields. See `config.example.json` for optional parameters. No automatic retry is performed: inspect errors before repeating a potentially billable request. Run `python <skill-dir>/scripts/imagegen.py --help` for options.
