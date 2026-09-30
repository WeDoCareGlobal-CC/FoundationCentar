# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Prometheus metrics endpoint (`/metrics`) with HTTP request counters, latency histograms, and skill execution tracking
- Comprehensive test suite with pytest (targeting ≥80% coverage)
- Python lockfile (`requirements.lock`) for reproducible builds
- Non-root user in Dockerfile for security hardening
- Base image digest pinning in Dockerfile
- Security scanning in CI (bandit, safety for Python; npm audit for Node)
- Multi-stage Docker build with proper caching

### Changed
- Updated CI workflow to include security scanning and coverage enforcement
- Updated CONTRIBUTING.md to be FoundationCentar-specific

### Security
- Added non-root user (UID 1000) in Dockerfile
- Pinned base image digests
- Added security audit steps in CI

## [1.0.0] - 2026-09-30

### Added
- Initial FoundationCentar release: One-Click Agent Factory OS
- Hierarchical 10-agent orchestration (Brain → Chiefs → Workers)
- Model registry with NVIDIA NIM + vLLM fallbacks
- CEO Control Plane with one-click actions & approval gates
- Profit mission activation, worker campaigns, revenue ranking
- Unified identity (Google → GitHub/ORCID/Zenodo OAuth)
- Local AI bridge (bounded delegation)
- Research/release pipeline (GitHub → Zenodo DOI)
- Multi-stage Docker (frontend + backend + Python + nginx)
- Three.js PWA for agent visualization
- Skill synthesis from execution traces

### Infrastructure
- GitHub Actions CI/CD (validate, docker-build, release)
- Zenodo deposition on release
- Supervisor-managed nginx + uvicorn in production

---

**Full Changelog**: https://github.com/we-do-care-global/FoundationCentar/commits/main