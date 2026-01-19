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
                // Optionally show error in UI
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

            this.core.timeline.drawTimeline();
            this.core.ui.updateDisplays();

            this.updateVideoPreview(path);

            console.log(`[LosslessCut] Loaded metadata: ${metadata.duration}s, ${metadata.fps} fps`);

        } catch (error) {
            console.error("[LosslessCut] Failed to fetch metadata:", error);
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

        if (inWidget) inWidget.value = this.core.inPoint;
        if (outWidget) outWidget.value = this.core.outPoint;
    }
}
