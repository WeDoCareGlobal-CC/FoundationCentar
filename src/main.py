"""AtlanTida OS - Application entry point."""

import argparse
import sys
import os

from orchestrator import brain, run_cyclical_execution
from telemetry import app as telemetry_app


def run_server(port: int = 8000, host: str = "0.0.0.0") -> None:
    """Run the telemetry API server."""
    import uvicorn
    print(f"FoundationCentar: Telemetry API starting on http://{host}:{port}")
    uvicorn.run(telemetry_app, host=host, port=port)


def run_cli() -> None:
    """Run in CLI demo mode."""
    print("FoundationCentar v1.0.0 - Brain Agent Online")
    print("=" * 50)

    # Demo requests
    test_requests = [
        {"domain": "operations", "action": "diagnose smart meter"},
        {"domain": "marketing", "action": "create campaign"},
        {"domain": "infrastructure", "action": "deploy to fly.io"},
        {"domain": "unknown", "action": "do something"},
    ]

    for req in test_requests:
        result = brain.route(req)
        print(f"\nRequest: {req}")
        print(f"Result: {result}")

    print("\n" + "=" * 50)
    print("FoundationCentar: Ready.")


def main():
    parser = argparse.ArgumentParser(description="FoundationCentar - One-Click Agent Factory OS")
    parser.add_argument("--mode", choices=["server", "cli"], default="cli",
                        help="Run mode: server (API) or cli (demo)")
    parser.add_argument("--port", type=int, default=8000,
                        help="Port for server mode (default: 8000)")
    parser.add_argument("--host", type=str, default="0.0.0.0",
                        help="Host for server mode (default: 0.0.0.0)")
    parser.add_argument("--daemon", action="store_true",
                        help="Run in cyclical daemon mode")

    args = parser.parse_args()

    if args.mode == "server":
        run_server(port=args.port, host=args.host)
    elif args.daemon:
        run_cyclical_execution()
    else:
        run_cli()


if __name__ == "__main__":
    main()
