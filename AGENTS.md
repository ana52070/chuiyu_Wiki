# Repository Guidelines

## Project Structure & Module Organization
- `blog/`, `guide/`, `projects/`: Markdown content for the VitePress site.
- `public/`: Static assets served as-is.
- `.vitepress/`: VitePress config and theme overrides (`config.mts`, `theme/`).
- Root scripts: Python and batch utilities like `upload_with_llm.py`, `update_index_with_llm.py`, and `run_upload_with_llm.bat`.
- Metadata files: `categories.md`, `tags.md`, `archives.md`, `index.md`.

## Build, Test, and Development Commands
- `npm install`: Install Node dependencies.
- `npm run docs:dev`: Start local VitePress dev server.
- `npm run docs:build`: Build static site output.
- `npm run docs:preview`: Preview the built site locally.
- `python upload_with_llm.py`: Optional helper that generates commit messages and pushes changes (requires `.env`).

## Coding Style & Naming Conventions
- Content is Markdown with YAML frontmatter. Follow existing keys such as `title`, `date`, `categories`, `tags`, and `permalink`.
- Keep filenames consistent with existing content; Chinese titles are acceptable and already used.
- Use 2-space indentation in YAML frontmatter lists.
- Avoid nonessential formatting churn.

## Testing Guidelines
- There is no automated test suite; `npm test` is a placeholder and exits with an error.
- For validation, use `npm run docs:dev` or `npm run docs:build` to catch build-time issues.

## Commit & Pull Request Guidelines
- Recent commits commonly use `Auto update: YYYY-MM-DD HH:MM:SS` and some use a `fix:` prefix. Follow these patterns where appropriate.
- PRs should include a clear summary, the scope of content changes, and screenshots for visual/layout changes to the VitePress site.
- Link related issues if applicable.

## Security & Configuration Tips
- `.env` stores keys like `OPENROUTER_API_KEY` for automation scripts. Do not commit secrets.
- If using the upload automation, verify the generated commit message before pushing.

## Tips
Always respond in Chinese-simplified\n