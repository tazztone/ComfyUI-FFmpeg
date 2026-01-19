export class LosslessCutNodeIntegration {
    constructor(core) {
        this.core = core;
    }

    async loadVideoMetadata() {
        const node_id = this.core.node.id;
        const url = `/output/losslesscut_data_${node_id}.json?t=${Date.now()}`;

        try {
            const response = await fetch(url);
            if (!response.ok) {
                console.warn(`[LosslessCut] Metadata not found at ${url}. Run the node first.`);
                return;
            }

            const metadata = await response.json();
            this.core.videoData = metadata;
            this.core.timeline.videoData = metadata;
            this.core.outPoint = metadata.duration;
            this.core.timeline.outPoint = metadata.duration;

            this.core.timeline.drawTimeline();
            this.core.ui.updateDisplays();

            console.log(`Loaded video metadata: ${metadata.duration}s, ${metadata.fps} fps, ${metadata.keyframes.length} keyframes`);
        } catch (error) {
            console.log('No metadata available yet, will try again after next execution.');
        }
    }

    queueAction(action) {
        // Access widgets directly from the node (stored in _hiddenWidgets or find them)
        const node = this.core.node;
        const actionWidget = node._hiddenWidgets?.['action'] || node.widgets?.find(w => w.name === 'action');
        const inWidget = node._hiddenWidgets?.['in_point'] || node.widgets?.find(w => w.name === 'in_point');
        const outWidget = node._hiddenWidgets?.['out_point'] || node.widgets?.find(w => w.name === 'out_point');
        const posWidget = node._hiddenWidgets?.['current_position'] || node.widgets?.find(w => w.name === 'current_position');

        if (!actionWidget) {
            console.error('[LosslessCut] Action widget not found');
            return;
        }

        // Set action
        actionWidget.value = action;
        // console.log(`[LosslessCut] Queuing action: ${action}`);

        // Sync current state to widgets so backend receives correct values
        if (this.core.videoData) {
            if (inWidget) inWidget.value = this.core.inPoint;
            if (outWidget) outWidget.value = this.core.outPoint;
            if (posWidget) posWidget.value = this.core.currentFrame / this.core.videoData.fps;
        }

        // Trigger graph update to ensure values are picked up
        node.graph?.setDirtyCanvas(true, false);

        // Queue prompt execution
        if (window.app && window.app.queuePrompt) {
            window.app.queuePrompt(0, 1);
        }

        // Reload metadata after execution (give it time to process)
        setTimeout(() => this.loadVideoMetadata(), 1500);
    }
}
