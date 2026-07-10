#!/usr/bin/env bash
set -euo pipefail

if ! command -v dtctl >/dev/null 2>&1; then
  echo "dtctl is not installed or not on PATH." >&2
  echo "Install it with: brew install dynatrace-oss/tap/dtctl" >&2
  exit 127
fi

current_context="$(dtctl config current-context 2>/dev/null || true)"

if [[ -z "$current_context" ]]; then
  echo "No active dtctl context is configured." >&2
  echo "Run: dtctl auth login --context my-env --environment \"https://<env>.apps.dynatrace.com\"" >&2
  exit 1
fi

echo "Current dtctl context: $current_context"
echo

dtctl config describe-context "$current_context"
echo

dtctl doctor
