# Atlantida OS — Autonomous Cloud AI Operating System

[![CI](https://github.com/emirperla96-lab/atlantida-os/actions/workflows/ci.yml/badge.svg)](https://github.com/emirperla96-lab/atlantida-os/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white&label=Container&color=2496ED)](https://hub.docker.com/r/emirperla96/atlantida-os)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![10-Agent Orchestration](https://img.shields.io/badge/10--Agent%20Orchestration-00C853?logo=robot&logoColor=white)
![76 Skills](https://img.shields.io/badge/76-Skills-8E24AA?logo=code&logoColor=white)

Atlantida OS is a production-grade, 24/7 autonomous cloud AI operating platform. It is engineered to orchestrate multi-agent workflows, featuring deterministic state machines and automated skill synthesis directly from execution traces.

## System Architecture

The system utilizes a hierarchical 10-agent orchestration collective executing 76 modular skills across 9 autonomous domains.

```mermaid
graph TD
    A[Brain Agent - Global Router] --> B[Chief Agents - Domain Leads]
    B --> C[Worker Agents - Skill Executors]
    C --> D[Deterministic State Machines]
    D --> E[Skill Synthesis & Execution Traces]
```

## Core Features

* **Hierarchical 10-Agent Collective:** (Brain → Chiefs → Workers) topology routing complex workflows across 9 business domains.
* **Automated Skill Synthesis:** Real-time A2A (Agent-to-Agent) message passing with deterministic state machines that convert execution traces into reusable, parameterized tools.
* **3D Neural Command Center:** Real-time interactive UI built with Three.js and deployed as a Progressive Web App (PWA) for visualizing multi-agent Directed Acyclic Graphs (DAGs).
* **Zero-Overhead Infrastructure:** Autonomous background daemon loops containerized via Docker and deployed on Fly.io, designed for continuous uptime with minimal cloud footprint.

## Quickstart

```bash
# Clone the repository
git clone https://github.com/emirperla96-lab/atlantida-os.git
cd atlantida-os

# Build and run with Docker
docker build -t atlantida-os .
docker run -p 8000:8000 atlantida-os
```
