#!/usr/bin/env bash
set -e

sed -i 's/ZSH_THEME="devcontainers"/ZSH_THEME="kolo"/' ~/.zshrc

export $(cat .env | grep "^[^#\;]" | xargs)

grep -E 'HISTFILE=' ~/.zshrc || echo 'HISTFILE=/workspace/local/tmp/.zsh_history' >> ~/.zshrc;

cd  /workspace/backend \
    && pip install --no-cache-dir --user --upgrade pip pylance black==22.3.0 isort==5.12.0 \
    && poetry install

cd /workspace/frontend \
    && npm install

echo FINISHED