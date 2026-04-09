---
id: artifacts-readme
type: meta
created: 2026-04-08
---

# Wiki Artifacts — Image Descriptions

This folder contains text descriptions of images sent via Telegram or other gateways.

## Convention

When an image is received:
1. Vision model analyzes the image
2. Description is saved as `YYYY-MM-DD-NN-description.md`
3. Description includes: what's in the image, relevant text/labels, context from conversation
4. Original image reference (file path or Telegram media ID) is noted in frontmatter

## File Format

```
---
id: artifact-YYYY-MM-DD-NN
type: artifact
created: YYYY-MM-DD
source: telegram | cli | file
image_ref: <file path or media ID>
context: <brief note on why this image was sent>
---

# [Short Title]

## Description
[Full vision model description]

## Key Elements
- Element 1
- Element 2

## Notes
[Any contextual notes from the conversation]
```

## Index

| Date | File | Description |
|------|------|-------------|
| — | — | *No artifacts yet* |
