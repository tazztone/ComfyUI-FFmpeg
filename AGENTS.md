# Agent Instructions

## Publishing to Comfy Registry

This repository is configured to publish nodes to the Comfy Registry.

### Setup

1.  Ensure you have a Publisher ID and API Key from [Comfy Registry](https://registry.comfy.org/).
2.  The GitHub Action `.github/workflows/publish_action.yml` handles automated publishing.
3.  **IMPORTANT:** You must set the `REGISTRY_ACCESS_TOKEN` secret in your GitHub repository settings with your API Key.

### Publishing a New Version

To publish a new version of the nodes:

1.  Update the `version` field in `pyproject.toml`.
    *   Example: change `version = "1.0.0"` to `version = "1.0.1"`.
2.  Push the change to the `main` branch.
3.  The GitHub Action will automatically detect the change to `pyproject.toml` and publish the new version.

### Reference

For more details, see the [Publishing Documentation](https://docs.comfy.org/registry/publishing).
