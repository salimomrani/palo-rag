# Implementation Plan: Markdown Rendering in Chat

## Tech Stack

- **Framework**: Angular 21, standalone components, signals, OnPush
- **Markdown library**: `ngx-markdown@21.1.0` (already installed)
- **Indentation**: 2 spaces

## Files to Modify

| File | Change |
|------|--------|
| `frontend/src/app/app.config.ts` | Add `provideMarkdown()` to providers |
| `frontend/src/app/components/chat/chat.ts` | Import `MarkdownComponent`, add to `imports[]` |
| `frontend/src/app/components/chat/chat.html` | Replace `{{ msg.content }}` with `<markdown>` for assistant only |
| `frontend/src/app/components/chat/chat.scss` | Style markdown output (code blocks, lists, headings) |

## Architecture

- `provideMarkdown()` registered globally in `app.config.ts` (required by ngx-markdown)
- `MarkdownComponent` imported in `Chat` standalone component
- Template: `@if (msg.role === 'assistant')` → `<markdown [data]="msg.content">` | `@else` → `{{ msg.content }}`
- CSS scoped under `.message.assistant markdown` to avoid bleed-through

## No new files, no backend changes, no new npm installs.
