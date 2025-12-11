# Gemini Code Reviewer Action

This GitHub Action integrates a "Gemini Helper" to replace GitHub Copilot for code reviews on Pull Requests. It uses Google's Gemini API to analyze code diffs and post constructive feedback.

## Features

- **Automated Code Review**: automatically triggers on Pull Requests.
- **AI-Powered Feedback**: Uses Google Gemini (gemini-1.5-flash) to suggest improvements and catch bugs.
- **GitHub Integration**: Posts reviews directly as comments on the PR.

## Usage

To use this action in your repository, create a workflow file (e.g., `.github/workflows/gemini-review.yml`) with the following content:

```yaml
name: Gemini Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Run Gemini Reviewer
        uses: google-labs-jules/gemini-helper-action@v1 # Use a specific version tag
        with:
          gemini_api_key: ${{ secrets.GEMINI_API_KEY }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

## Setup

1. **Get a Gemini API Key**: [Get an API key from Google AI Studio](https://makersuite.google.com/app/apikey).
2. **Add Secrets**: Go to your repository settings -> Secrets and variables -> Actions, and add:
   - `GEMINI_API_KEY`: Your Google Gemini API Key.
   - `GITHUB_TOKEN`: This is automatically provided by GitHub, but you can explicitly pass it.

## Releases

This repository is configured to automatically publish releases and Docker images.

- **Releases**: Created automatically when a tag starting with `v` (e.g., `v1.0.0`) is pushed.
- **Docker Images**: Pushed to GitHub Container Registry (GHCR) with every release.

## Local Development & Build

To build the action locally, use the provided script:

```bash
./build.sh
```
