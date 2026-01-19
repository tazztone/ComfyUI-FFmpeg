import { api } from "/scripts/api.js";

export class LosslessCutNodeIntegration {
    constructor(core) {
        this.core = core;
    }

    async fetchMetadata(path) {
        if (!path) return;

        try {
            const response = await api.fetchApi("/comfyui-ffmpeg/metadata", {
                method: "POST",
                body: JSON.stringify({ path }),
            });

            if (!response.ok) {
                const err = await response.json();
                console.error("[LosslessCut] Metadata error:", err);
                if (window.app && window.app.ui && window.app.ui.dialog) {
                    window.app.ui.dialog.show(`LosslessCut Error: ${err.error || "Unknown error"}`);
                } else {
                    alert(`LosslessCut Error: ${err.error || "Unknown error"}`);
                }
                if (this.core.ui) this.core.ui.toggleLoadButton(true);
                return;
            }

            const metadata = await response.json();

            // Update Core Data
            this.core.videoData = metadata;
            this.core.timeline.videoData = metadata;

            // Set defaults if new video
            this.core.outPoint = metadata.duration;
            this.core.timeline.outPoint = metadata.duration;
            this.core.inPoint = 0;
            this.core.timeline.inPoint = 0;
            this.core.currentFrame = 0;
            this.core.timeline.currentFrame = 0;

            // Initialize default segment for multi-segment support
            this.core.initializeDefaultSegment();

            this.core.timeline.drawTimeline();
            this.core.ui.updateDisplays();

            this.updateVideoPreview(path);

            console.log(`[LosslessCut] Loaded metadata: ${metadata.duration}s, ${metadata.fps} fps`);

            // Hide load button on success
            if (this.core.ui) {
                this.core.ui.toggleLoadButton(false);
            }

        } catch (error) {
            console.error("[LosslessCut] Failed to fetch metadata:", error);
            if (this.core.ui) this.core.ui.toggleLoadButton(true);
        }
    }

    updateVideoPreview(path) {
        if (!this.core.ui.videoElement) return;

        // Use the stream endpoint
        const streamUrl = `/comfyui-ffmpeg/stream?path=${encodeURIComponent(path)}`;
        this.core.ui.videoElement.src = streamUrl;
        this.core.ui.videoElement.load();
    }

    syncWidgets() {
        const node = this.core.node;
        const inWidget = node._hiddenWidgets?.['in_point'] || node.widgets?.find(w => w.name === 'in_point');
        const outWidget = node._hiddenWidgets?.['out_point'] || node.widgets?.find(w => w.name === 'out_point');
        const screenshotTimeWidget = node._hiddenWidgets?.['screenshot_time'] || node.widgets?.find(w => w.name === 'screenshot_time');
        const segmentsWidget = node._hiddenWidgets?.['segments'] || node.widgets?.find(w => w.name === 'segments');
        const exportScreenshotWidget = node._hiddenWidgets?.['export_screenshot'] || node.widgets?.find(w => w.name === 'export_screenshot');
        const smartCutWidget = node._hiddenWidgets?.['smart_cut'] || node.widgets?.find(w => w.name === 'smart_cut');

        if (inWidget) inWidget.value = this.core.inPoint;
        if (outWidget) outWidget.value = this.core.outPoint;
        // Sync screenshot time to current playhead position
        if (screenshotTimeWidget) screenshotTimeWidget.value = this.core.currentRawTime;

        // For regular cuts, don't export screenshot
        if (exportScreenshotWidget) exportScreenshotWidget.value = false;

        // Sync segments JSON
        if (segmentsWidget && this.core.segments && this.core.segments.length > 0) {
            segmentsWidget.value = JSON.stringify(this.core.segments);
        }

        // Smart cut is ON when lossless lock is OFF (user wants frame-accurate cuts)
        if (smartCutWidget) {
            smartCutWidget.value = !this.core.losslessLock;
        }
    }

    syncWidgetsForScreenshot() {
        const node = this.core.node;
        const screenshotTimeWidget = node._hiddenWidgets?.['screenshot_time'] || node.widgets?.find(w => w.name === 'screenshot_time');
        const exportScreenshotWidget = node._hiddenWidgets?.['export_screenshot'] || node.widgets?.find(w => w.name === 'export_screenshot');

        // Set screenshot time to current playhead
        if (screenshotTimeWidget) screenshotTimeWidget.value = this.core.currentRawTime;

        // Enable screenshot export
        if (exportScreenshotWidget) exportScreenshotWidget.value = true;
    }
}

