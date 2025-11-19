import { LosslessCutUI } from './losslesscut_ui.js';
import { LosslessCutEvents } from './losslesscut_events.js';
import { LosslessCutTimeline } from './losslesscut_timeline.js';
import { LosslessCutNodeIntegration } from './losslesscut_node_integration.js';

export class LosslessCutCore {
    constructor(node) {
        this.node = node;
        this.videoData = null;
        this.inPoint = 0;
        this.outPoint = 0;
        this.currentFrame = 0;
        this.isPlaying = false;

        this.timeline = new LosslessCutTimeline(this);
        this.ui = new LosslessCutUI(this);
        this.events = new LosslessCutEvents(this);
        this.nodeIntegration = new LosslessCutNodeIntegration(this);

        this.setupInterface();
    }

    setupInterface() {
        const container = this.ui.createInterface();
        this.events.setupEventListeners();
        this.nodeIntegration.loadVideoMetadata();
        return container;
    }

    setInPoint(time = null) {
        if (!this.videoData) return;
        this.inPoint = time !== null ? time : (this.currentFrame / this.videoData.fps);
        this.timeline.inPoint = this.inPoint;
        this.nodeIntegration.queueAction('set_in');
        this.timeline.drawTimeline();
        this.ui.updateDisplays();
    }

    setOutPoint(time = null) {
        if (!this.videoData) return;
        this.outPoint = time !== null ? time : (this.currentFrame / this.videoData.fps);
        this.timeline.outPoint = this.outPoint;
        this.nodeIntegration.queueAction('set_out');
        this.timeline.drawTimeline();
        this.ui.updateDisplays();
    }

    gotoPrevKeyframe() {
        this.nodeIntegration.queueAction('prev_kf');
    }

    gotoNextKeyframe() {
        this.nodeIntegration.queueAction('next_kf');
    }

    performCut() {
        this.nodeIntegration.queueAction('cut');
    }

    seekTo(time) {
        if (!this.videoData) return;
        this.currentFrame = Math.floor(time * this.videoData.fps);
        this.timeline.currentFrame = this.currentFrame;
        this.timeline.drawTimeline();
        this.ui.updateDisplays();
    }

    zoomIn() {
        if (!this.videoData) return;
        this.timeline.zoomLevel = Math.min(this.timeline.zoomLevel * 1.5, 100);
        this.timeline.drawTimeline();
    }

    zoomOut() {
        if (!this.videoData) return;
        this.timeline.zoomLevel = Math.max(this.timeline.zoomLevel / 1.5, 1);
        this.timeline.drawTimeline();
    }

    resetZoom() {
        if (!this.videoData) return;
        this.timeline.zoomLevel = 1;
        this.timeline.scrollOffset = 0;
        this.timeline.drawTimeline();
    }

    goToStart() {
        this.seekTo(0);
    }

    goToEnd() {
        if (!this.videoData) return;
        this.seekTo(this.videoData.duration);
    }

    stepBackward() {
        if (!this.videoData) return;
        this.seekTo((this.currentFrame - 1) / this.videoData.fps);
    }

    stepForward() {
        if (!this.videoData) return;
        this.seekTo((this.currentFrame + 1) / this.videoData.fps);
    }

    togglePlay() {
        // Not implemented yet
    }
}
