# ❤️‍🔥 Contributing to this project

Thank you for your interest in contributing to **pulumi-extra**.

## 🐛 Reporting issues

Please report issues in our [GitHub repository](https://github.com/lasuillard-s/pulumi-extra/issues). Before submitting an issue, please search for existing issues to avoid duplicates.

## 🏗️ Project overview

This project provides extra utilities and resources for Pulumi Python programs.

- Python package (`pulumi-extra`): Resource helpers, output transforms, stack references, and Pulumi runtime utilities
- AWS/GCP helpers: Auto-tagging and auto-labeling utilities for cloud resources
- Pulumi policies: Policy pack policies for required tags, labels, and descriptions

### 🛠️ Tech stack

This project uses the following tech stack:

- [Python](https://www.python.org) 3.10+
- [uv](https://docs.astral.sh/uv/) for dependency management and packaging
- [Ruff](https://docs.astral.sh/ruff/) to format and lint Python code, and [Mypy](https://mypy-lang.org) for type checking
- [pytest](https://docs.pytest.org/en/latest) and [nox](https://nox.thea.codes/en/stable/) for testing
- [MkDocs](https://www.mkdocs.org) for documentation

### 📂 Key directory structure

- `docs/`: Project documentation
- `pulumi_extra/`: The project's Python package source code
- `tests/`: Project tests and nox test sessions
- `flake.nix`: Nix Flakes development environment
- `Justfile`: Commands for development
- `mkdocs.yaml`: Documentation configuration
- `noxfile.py`: nox test configuration
- `pyproject.toml`: Project dependencies and configuration

## 🔧 Set up the development environment

For development, the following tools are required:

### ❄️ Tools managed via Nix Flakes

This repository uses [Nix Flakes](https://nix.dev/concepts/flakes.html) to manage development tools. The following tools are automatically installed when `nix` is available:

- `pre-commit`
- `just`
- `uv`
- `pipx`
- Pulumi CLI (`pulumi`)

Simply run `nix develop` to enter the development environment, then run `just install` to install dependencies. The Nix shell also installs the pre-commit hooks automatically.

If you prefer using a [Dev Container](https://containers.dev), an example configuration file ([`devcontainer.json`](./.devcontainer.example/devcontainer.json)) is provided with Nix and Docker-in-Docker pre-installed.

## ✅ Verifying changes

Before pushing your code, verify that your changes adhere to the project's coding standards. Run `just ci` to execute all necessary linters, formatters, and tests.

Alternatively, use the `pre-commit` hooks to handle formatting, linting, type checking, and quick pytest feedback automatically.

## ✨ Submitting changes

Please feel free to submit pull requests on GitHub. Before opening a PR, ensure your changes pass all checks by running `just ci`.

## 🚀 Release process

The package will be published to PyPI. To release a new version, follow these steps:

1. Prepare release via [Prepare Release workflow](https://github.com/lasuillard-s/pulumi-extra/actions/workflows/prepare-release.yaml) with a `v*` tag.
1. Review and merge the generated release pull request.
1. Create and publish a new release in GitHub Releases.
1. [release.yaml](./.github/workflows/release.yaml) workflow will build distributions, attach them to the GitHub Release, and publish them to PyPI.

Documentation is published to [GitHub Pages](https://lasuillard-s.github.io/pulumi-extra/) via [docs.yaml](./.github/workflows/docs.yaml) when changes are pushed to the `main` branch or to a `v*` tag.
