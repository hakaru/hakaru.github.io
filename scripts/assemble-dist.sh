#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

# 1. Docusaurus ビルド
echo "==> Building Docusaurus"
cd M2DX-docs-src
npm ci
npm run build
cd "$REPO_ROOT"

# 2. dist/ に既存静的ファイルを集約
echo "==> Assembling dist/"
rm -rf dist
mkdir -p dist
rsync -a \
  --exclude='dist/'                 \
  --exclude='M2DX-docs-src/'        \
  --exclude='node_modules/'         \
  --exclude='.git/'                 \
  --exclude='.github/'              \
  --exclude='.claude/'              \
  --exclude='.superpowers/'         \
  --exclude='docs/superpowers/'     \
  --exclude='tasks/'                \
  --exclude='__pycache__/'          \
  --exclude='*.pyc'                 \
  --exclude='AGENTS.md'             \
  ./ dist/

# 3. Docusaurus 成果物を /M2DX-docs/ に重ねる
echo "==> Overlaying M2DX-docs/"
mkdir -p dist/M2DX-docs
rsync -a M2DX-docs-src/build/ dist/M2DX-docs/

echo "==> Done"
ls dist/ | head -20
