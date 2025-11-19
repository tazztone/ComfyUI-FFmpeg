export class LosslessCutNodeIntegration {
    constructor(core) {
        this.core = core;
    }

    async loadVideoMetadata() {
        const node_id = this.core.node.id;
        const url = `/output/losslesscut_data_${node_id}.json?t=${Date.now()}`;

        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error('Metadata not found');

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
        const actionWidget = this.core.node.widgets.find(w => w.name === 'action');
        if (actionWidget) {
            actionWidget.value = action;
            window.app.queuePrompt();

            setTimeout(() => this.loadVideoMetadata(), 2000);
        }
    }
}
