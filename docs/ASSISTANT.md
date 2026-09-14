# Course AI assistant

The assistant is available on every course overview and lesson through **Ask AI assistant**. It helps explain the current material, troubleshoot learner code, and create starter projects with setup instructions.

## Configuration

The FastAPI backend uses the official `openai` Python package, configured with OpenRouter's `https://openrouter.ai/api/v1` endpoint. It calls `client.chat.completions.create`, not a direct OpenAI endpoint.

Add the following to the repository's `.env` (copy `.env.example` only if you do not already have a `.env`):

```dotenv
OPENROUTER_API_KEY=your-openrouter-key
OPENROUTER_MODEL=openai/gpt-4.1-mini
```

`OPENROUTER_MODEL` can be changed to an OpenRouter model slug supporting JSON Schema structured outputs. The default is `openai/gpt-4.1-mini`. Provider routing requires support for the requested parameters; unsupported models produce an actionable connection error instead of unstructured files. See [OpenRouter's OpenAI SDK configuration](https://openrouter.ai/docs/quickstart#using-the-openai-sdk) and [structured outputs documentation](https://openrouter.ai/docs/guides/features/structured-outputs).

Local installation:

```sh
backend/.venv/bin/python -m pip install -r backend/requirements.txt
npm run dev
```

The development launcher loads the root `.env` without overriding exported variables. Restart it after changing credentials or models. Separate-terminal API users can export the variables before `npm run dev:api`, or launch Uvicorn with `--env-file .env` from the repository root. Docker Compose passes the variables only to the API service:

```sh
docker compose up --build -d
```

Do not put credentials in `VITE_` variables or paste them into the assistant. A direct OpenAI key (`OPENAI_API_KEY`) is deliberately not used. No key is required for the rest of Quanta. The assistant's unavailable state preserves course downloads and any question the learner has typed.

## Learning and code workflow

- **Understanding** starts with a hint, a small example, and a next step grounded in the course. Learners can ask follow-up questions in the same chat.
- **Environment setup** generates up to six text files, typically a README, dependency/build files, and source. Select macOS, Windows, or Linux before sending. The assistant also receives available authored project guides so setup instructions can match the actual course.
- **Writing code** receives the selected lesson, its objective, content, template, references, and optionally the current editor draft and last Python execution error. It can explain a failure and return a complete proposed worksheet.
- Expand a generated file to review it, copy or download it individually, or download all files in a ZIP that preserves relative directories.
- Python/C files marked for the matching lesson can be applied to the editor. This saves a draft and opens split view. **Undo code replacement** restores the preceding draft until further edits make that undo stale. Applying code never runs it automatically.

The assistant creates file contents and instructions. It does not install software on a learner's computer or execute generated commands. Guided Python keeps its existing limits; local projects are downloaded and run separately. C lessons keep their local compile/download workflow. Generated code is not automatically verified by the assistant.

## Context and persistence

The UI sends the message, selected course/lesson IDs, help mode, operating system, and recent chat to Quanta's API. The backend loads course context from the canonical catalog and available project guides. It does not fetch model-supplied URLs or accept client-supplied system messages.

The **Include editor code & last run error** control omits the draft, execution error, and generated file bodies from subsequent requests when switched off. Text explicitly typed into chat remains part of the recent conversation. Turning the control off does not retract context already sent.

OpenRouter and its selected model provider process the submitted context according to their settings and policies. The app stores the latest 12 chat messages in browser tab session storage, scoped to the account/guest and course or lesson. Chats are not part of account workspace sync. Closing the drawer keeps completed messages; navigation or account changes cancel pending UI requests and isolate conversations. Starting a new chat clears the current stored conversation. Stopping a response restores the question; upstream inference may already be running and incur usage.

## API and limits

| Route | Behavior |
| --- | --- |
| `GET /api/v1/assistant/status` | Reports only whether an OpenRouter key is configured; makes no paid request. |
| `POST /api/v1/assistant/chat` | Returns `{message, files}`; messages support Markdown, each file has `path`, `language`, `content`, and `target`. |
| `POST /api/v1/assistant/bundle` | Packages validated text files into `quanta-project.zip`, under a `quanta-project/` directory; never executes or writes them to disk. |

Chat permits 10 requests per minute and 40 per hour per user (or guest IP), plus 60 per hour per source IP. Downloads permit 30 per minute. Existing origin checks and Redis-backed request limits apply. AI usage is charged to the configured OpenRouter account.

Inputs are bounded to 4,000 characters per question, 20,000 for editor code, 4,000 for the error, and ten history messages totaling 60,000 characters. Output is capped at 8,192 tokens and six files, with at most 20,000 characters per file and 80,000 total file characters. Absolute paths, traversal, conflicting paths, and Windows reserved names are rejected. Local project files and mismatched source languages cannot be applied to a lesson editor.

The provider request has an 85-second deadline and no automatic SDK retries. The frontend timeout and production proxy allow time for that deadline. Provider errors are mapped to readable messages without exposing provider response bodies, and assistant responses use `Cache-Control: no-store`. A truncated or invalid generated response never becomes a downloadable artifact.

## Verification

```sh
backend/.venv/bin/python -m pytest backend/tests/test_assistant.py -q
npm test
npm run build
TEST_URL=http://127.0.0.1:5173 npm run test:e2e -- assistant.spec.ts
```

Backend tests run the real OpenAI SDK against a mocked HTTP transport to verify the OpenRouter URL, authorization, schema, context, error handling, path validation, ZIP contents, and rate limits without paid inference. Browser tests mock AI replies while exercising actual course pages, editor persistence, undo, error sharing, downloads through the API, cancellation, lesson isolation, and mobile controls. A live model call additionally requires a funded OpenRouter key.
