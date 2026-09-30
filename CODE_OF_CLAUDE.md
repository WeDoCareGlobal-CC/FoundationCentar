# CODE_OF_CLAUDE.md

This file defines the conventions and expectations for AI-assisted coding in FoundationCentar.

## AI Agent Conventions

### When AI agents (Claude, Codex, etc.) work on this repository:

1. **Follow the existing patterns** — Read existing code before writing new code. Match the style, structure, and conventions already present.

2. **Write tests first** — Every new feature or bug fix must include tests. Target ≥80% coverage.

3. **Run the full CI locally before pushing** — Execute:
   ```bash
   ruff check src/
   mypy src/ --ignore-missing-imports
   python -m pytest tests/ -v --cov=src --cov-fail-under=80
   cd frontend && npm run lint && npm run typecheck && npm run build
   cd backend && npx tsc --noEmit
   ```

4. **Update documentation** — If you change behavior, update:
   - `CHANGELOG.md` (under `[Unreleased]`)
   - Relevant docstrings and README sections
   - API docs (OpenAPI/Swagger auto-generated from FastAPI)

5. **Use conventional commits** — Prefix commits with:
   - `feat:` new feature
   - `fix:` bug fix
   - `docs:` documentation only
   - `refactor:` code change that neither fixes a bug nor adds a feature
   - `test:` adding or modifying tests
   - `chore:` maintenance (deps, config, etc.)

6. **Security first** — Never commit secrets. Use environment variables for configuration. Run security scans (bandit, safety, npm audit) before merging.

7. **Docker best practices** — When modifying Dockerfile:
   - Use specific base image digests (not tags)
   - Run as non-root user
   - Multi-stage builds for smaller images
   - No secrets in images

8. **Observability** — Add metrics for new endpoints. Use the existing Prometheus counters/histograms in `src/telemetry.py`.

9. **Skills system** — New skills must:
   - Be placed in `src/skills/<domain>/`
   - Have input validation (Pydantic models)
   - Return structured output with execution time
   - Be registered in the domain's `__init__.py`
   - Include tests

10. **No silent failures** — All errors must be logged and surfaced appropriately. Use structured logging.

## Code Review Checklist for AI Contributions

- [ ] Tests added and passing (≥80% coverage)
- [ ] Linting passes (ruff, ESLint)
- [ ] Type checking passes (mypy, tsc)
- [ ] Security scans pass (bandit, safety, npm audit)
- [ ] CHANGELOG.md updated
- [ ] Documentation updated
- [ ] No hardcoded secrets
- [ ] Dockerfile follows best practices
- [ ] Metrics added for new endpoints
- [ ] Conventional commit messages

## Prohibited Patterns

- ❌ `print()` for logging (use `logging` module)
- ❌ Bare `except:` clauses
- ❌ Hardcoded paths, URLs, or credentials
- ❌ Skipping tests to "make CI pass"
- ❌ Adding dependencies without updating lockfiles
- ❌ Modifying generated files (OpenAPI specs, etc.)
- ❌ Committing directly to `main` (use PRs)

## Escalation

If an AI agent encounters ambiguity or conflicting requirements:
1. Stop and ask the human maintainer
2. Document the question in the PR description
3. Do not guess — clarify first

---

**ORCID**: 0009-0009-8515-2727 (Emir Perla)
**Maintainer**: We Do Care Global