# CI & PyPI Setup Guide

This document explains how the PSAE CI/CD pipeline works and what you need to configure to go fully live.

---

## How CI works (free-tier-first design)

### Testing — zero cost by default

| What | How | Cost |
|------|-----|------|
| FinBERT sentiment in CI | HuggingFace free Inference API (`PSAE_SENTIMENT_PROVIDER=huggingface_api`) | **Free** |
| spaCy NER | `en_core_web_sm` downloaded at CI time (~12MB) | **Free** |
| OpenAI / GPT-4o | Mocked in unit tests (`-m "not integration"`) | **Free** |
| CI runner | GitHub Actions (2,000 free minutes/month on public repos) | **Free** |

### Publishing — OIDC first (no token needed once configured)

PyPI now supports **Trusted Publishers** via OIDC — no `PYPI_TOKEN` secret required once you set it up.

**OIDC setup (one-time, free):**
1. Go to https://pypi.org/manage/account/publishing/
2. Add a new trusted publisher for each package:
   - **Owner:** `TawandaVera`
   - **Repository:** `psae-core` (repeat for each)
   - **Workflow:** `ci.yml`
   - **Environment:** `pypi`
3. Repeat for TestPyPI at https://test.pypi.org/manage/account/publishing/

Once OIDC is configured, `PYPI_TOKEN` is never used. It only acts as a fallback.

---

## Secrets reference

Three secrets are pre-created in all 6 repos. Update them with real values:

### `PYPI_TOKEN` — PyPI publish fallback
- **When needed:** Only if OIDC trusted publisher is NOT configured (above)
- **Get it:** https://pypi.org/manage/account/token/ → scope to each package
- **Update:** Settings → Secrets → Actions → `PYPI_TOKEN` → Update

### `OPENAI_API_KEY` — GPT-4o enrichment in integration tests
- **When needed:** Only for `pytest -m integration` (not run in standard CI)
- **Free alternative:** Leave empty — integration tests are skipped gracefully
- **Get it:** https://platform.openai.com/api-keys

### `HF_API_TOKEN` — HuggingFace Inference API (higher rate limits)
- **When needed:** If free-tier HF rate limits are hit in CI
- **Free alternative:** Leave empty — free tier (no token) is used automatically
- **Get it:** https://huggingface.co/settings/tokens (free account, read-only token)

---

## Update a secret via GitHub CLI (fastest)

```bash
# Install: https://cli.github.com
gh auth login

REPOS="psae-core psae-ingest psae-signal psae-factor psae-backtest psae-folio"

# Set PYPI_TOKEN on all repos at once
for repo in $REPOS; do
  echo "pypi-AgEI..." | gh secret set PYPI_TOKEN --repo TawandaVera/$repo
done

# Set OPENAI_API_KEY
for repo in $REPOS; do
  echo "sk-proj-..." | gh secret set OPENAI_API_KEY --repo TawandaVera/$repo
done

# Set HF_API_TOKEN (free read token)
for repo in $REPOS; do
  echo "hf_..." | gh secret set HF_API_TOKEN --repo TawandaVera/$repo
done
```

---

## Release flow

1. Tag a release: `git tag v0.1.0 && git push --tags`
2. Create a GitHub Release from the tag
3. CI triggers automatically:
   - Runs tests
   - Builds wheel + sdist
   - Publishes to **TestPyPI** first (validates the package)
   - On success → publishes to **PyPI**

Installs will then work as:
```bash
pip install psae-core psae-signal psae-factor psae-backtest psae-folio
```
