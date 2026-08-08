# Monorepo cleanup, bug fixes, and execution

## Context

Two unrelated products in one tree: an **ML Platform** (FastAPI + SQLAlchemy async + PyTorch/SHAP, React/Vite web) and **CodeDock** (Spring Boot Docker-in-Docker code executor + Chrome MV3 side-panel extension). Every source file in both was read and audited (~80 issues catalogued).

Toolchain reality: Node 22.18, Python 3.13.7, Java 17 (pom needs 21), no Maven, no Docker. This drives the verification strategy: ML stack runs live on SQLite with optional ML deps; CodeDock API is fixed at source level and honestly reported as unverifiable here; extension must pass `npm run build`.

User-confirmed scope: full monorepo re-layout, fix both projects (ML first), SQLite + optional ML deps for execution.

## Phase 1 — Monorepo re-layout (`git mv` to preserve history)

```
├── apps/ml-web/            (was frontend/)
├── apps/codedock-ext/      (was CodeDock/chrome-extension/)
├── services/ml-api/        (was backend/)
├── services/codedock-api/  (was CodeDock/backend/)
├── infra/docker/           (was docker/ + CodeDock/docker/ content)
├── infra/db/               (was CodeDock/database/init.sql)
├── infra/compose/          (ml-platform.yml, codedock.yml)
├── docs/                   (architecture.md, ml-platform.md, codedock.md)
├── .github/workflows/ci.yml
├── Makefile  .editorconfig  README.md  .gitignore
```

Remove empty dirs: `frontend/src/hooks`, `frontend/src/utils`, `frontend/public`, `chrome-extension/public`, `chrome-extension/assets`. Make one commit of current state first as a restore point (tree is untracked, zero commits).

## Phase 2 — ML API (`services/ml-api`)

1. **Boot blocker:** `app/models/__init__.py:4` imports nonexistent `app.models.base`; `Base` lives in `app.core.database`. Fix import.
2. **Config:** drop `os.getenv` inside Settings; `DATABASE_URL` defaults to `sqlite+aiosqlite:///./ml_platform.db`; fix `env_file` path.
3. **get_db():** remove implicit `commit()` (autocommit per request).
4. **Lazy ML imports:** torch/shap/sklearn imported on demand; `503` with a clear message when unavailable (runs clean on base deps).
5. **Hoist 9 inline `HTTPException` imports**; typed `PredictRequest`/`ExplainRequest` schemas; `get_or_404` helper.
6. **Categorical collapse bug:** single-row `pd.get_dummies(drop_first=True)` collapses categories to 0 at inference. Persist training-time column layout; `reindex(fill_value=0)` at predict/explain.
7. **analyze_graph fabrication:** replace fake `accuracy * (0.5+0.5*(i%3)/3)` importances with real SHAP or `409` when unavailable.
8. **explain hardcoded `get_dataset(db, 1)`:** persist `dataset_id` on the model; pass through.
9. **SHAP scaling mismatch:** training fits `StandardScaler`, explain path never scales → explain an unseen distribution. Scale predict_fn inputs + background; add `.to(device)` in `predict_proba`.
10. **feature_names:** plumb real column names into explainability.
11. **Dataset path traversal:** sanitize upload filename, `400` on unparseable CSV instead of silently storing `row_count=0`.
12. **Dead code:** remove `training.py:115-116` unused counters, `plotting.py:196` `graph_data = []`.
13. **Requirements split:** `requirements/base.txt` (installs on 3.13: fastapi, uvicorn, sqlalchemy, aiosqlite, etc.) + `requirements/ml.txt` (torch, shap, transformers — lazy, optional).
14. **Tests:** `services/ml-api/tests/` — pytest + httpx ASGITransport + SQLite, covering predict/explain/get_or_404/upload sanitization.

## Phase 3 — ML web (`apps/ml-web`)

1. `PlotlyChart`: parse full `fig.to_json()` → `{data, layout}`, not bare array.
2. Dashboard predictions stat → wired to `/predictions/`.
3. Implement stubs: `ModelsPage` (list + create + train + delete), `ModelDetail` (predict + explain + graph), `PredictionsPage` (list).
4. `DatasetsPage`: surface upload errors, delete dataset, drop unused `fileRef`.
5. `api.js`: axios error interceptor + `fetchPredictions`/`deleteDataset`/`deleteModel`.
6. ESLint clean; `npm run build` passes.

## Phase 4 — CodeDock API (`services/codedock-api`, source-level only)

1. **Deadlock:** `DockerExecutionService` reads stdout/stderr *after* `waitFor()` — any output >64KB pipe buffer hangs until timeout. Drain concurrently during run (incl. compile phase).
2. **Stdin dead:** `input.txt` written but never piped. Add `-i` flag + `ProcessBuilder` stdin wiring; remove per-execution `input.txt` artifact.
3. **Compose context escape:** `dockerfile: ../docker/...` with `context: ./backend`. Fix to correct relative context or inline build.
4. **Dockerfile.backend:** multi-stage, copies built jar only; works with wrapper build.
5. **Java 17 target** with profile for 21 + Maven wrapper (no Maven on this machine — commit wrapper jar).
6. **application.properties:** env-interpolated DB creds (no hardcoded postgres/postgres).
7. **GlobalExceptionHandler:** raw `ex.getMessage()` leak + `Map.of` NPE on null message.
8. **Memory type drift:** `init.sql` BIGINT vs `Long` vs `Integer` — reconcile to one.
9. **init.sql:** remove redundant `CREATE DATABASE`/`\c` (POSTGRES_DB already creates it).
10. **getCompiler null-language NPE** → 400; `@Size` cap on code.
11. **Sandbox hardening:** `--network=none`, `--pids-limit`, read-only rootfs, `--cap-drop=ALL`; document residual host-socket risk.

## Phase 5 — CodeDock extension (`apps/codedock-ext`, buildable here)

1. `Editor.tsx` `React.FC` with no React import (TS2686); same in Stats/Toolbar/LanguageSelector/Console.
2. `@types/chrome` + `types: ["chrome"]` in tsconfig.
3. Copy `manifest.json` + `icons/` into `dist/` (static copy in vite config) — without it the built extension can't load in Chrome.
4. `VITE_CODEDOCK_API_URL` for api.ts baseURL.
5. Consolidate two storage layers; AbortController for run/stop (stop actually cancels).
6. `ExecutionResponse` fields nullable (API returns null).
7. typecheck/lint scripts; verify `npm run build` + `tsc` pass.

## Phase 6 — Docs + tooling

README (root), docs/architecture.md, per-project READMEs, Makefile targets (dev-api, dev-web, build-ext, test, lint), CI workflow (lint + test + build both frontends), .editorconfig, consolidated root .gitignore.

## Phase 7 — Execute & verify (live)

1. `python -m compileall` both backend trees.
2. `pip install requirements/base.txt` → boot uvicorn on SQLite.
3. Live curl: `/health`, CSV upload, dataset list, model create/train/list, predict (handled 503 w/o torch), delete.
4. `pytest`.
5. `npm run build` ml-web + codedock-ext; assert `dist/manifest.json` + icons exist.
6. Commit locally (re-layout + fixes, separate commits). No push.

## Caveats

- CodeDock Java service cannot be compiled (no Maven, Java 17 vs 21) or run (no Docker) here — fixed at source level, reported as unverified.
- Docker socket mount in codedock compose is inherent to the design (container-in-container); hardened but flagged.
