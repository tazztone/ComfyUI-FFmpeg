# ComfyUI-FFmpeg Roadmap

This document outlines the development roadmap for **ComfyUI-FFmpeg**, focusing on stability, modernization, and feature expansion.

## 🏁 Phase 1: Stabilization & Foundation (Current Focus)

The immediate goal is to ensure the reliability and security of existing nodes.

*   **Testing Infrastructure**:
    *   [x] Establish `pytest` infrastructure with `unit` and `integration` separation.
    *   [x] Fix flaky tests (e.g., `test_keyframe_aware_cutting`).
    *   [x] Un-skip and fix complex mocked tests (`test_lossless_cut`).
    *   [x] Achieve >80% code coverage.
*   **Code Quality & Security**:
    *   [x] Centralize FFmpeg logic in `func.py`.
    *   [x] Audit all `subprocess` calls for security (ensure `shlex.split` usage).
    *   [x] Standardize error handling and user feedback (logging).
*   **Documentation**:
    *   [x] Update `AGENTS.md` for developer onboarding.
    *   [x] Ensure all nodes have corresponding usage docs in `README.md`.

## 🚀 Phase 2: Architecture Modernization (V3 Migration)

ComfyUI is moving towards a V3 schema. We need to prepare our nodes for this transition.

*   **Schema Migration**:
    *   [ ] Prototype one node using the new `define_schema` and `async comfy_entrypoint`.
    *   [ ] Progressive migration of core nodes (e.g., `Save Images`, `Load Images`) to V3.
*   **Type Safety**:
    *   [ ] Add type hints to all Python code.
    *   [ ] Strict type checking for `INPUT_TYPES` definitions.

## ✨ Phase 3: Feature Expansion

Expanding the capabilities to cover more FFmpeg features and improve user experience.

*   **Interactive Features**:
    *   [ ] Improve `LosslessCut` UI with better timeline controls and scrubbing.
    *   [ ] Add interactive cropping/region-of-interest selection node.
*   **Advanced Audio**:
    *   [ ] Add visual equalizer/spectrum analyzer node.
    *   [ ] Support for VST plugins (via FFmpeg filters where applicable) or complex audio filter graphs.
*   **Streaming & Formats**:
    *   [ ] Support for RTSP/RTMP stream input nodes.
    *   [ ] Better support for animated WebP and AVIF formats.

## 🔮 Phase 4: Long-Term Goals

*   **Performance**:
    *   [ ] GPU acceleration support (NVENC/QSV) detection and auto-configuration.
    *   [ ] Parallel processing for batch operations.
*   **Ecosystem**:
    *   [ ] "One-click" preset library for common transcoding tasks (e.g., "Compress for Web", "Extract Audio").
    *   [ ] Integration with external video AI tools (e.g., frame interpolation models).

---

> **Note:** This roadmap is a living document and will evolve based on community feedback and ComfyUI core updates.
