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
        this.currentRawTime = 0; // Track precise float time to avoid rounding errors
        this.isPlaying = false;
        this.losslessLock = true; // Constrain IN/OUT to keyframes for lossless cuts

        this.timeline = new LosslessCutTimeline(this);
        this.ui = new LosslessCutUI(this);
        this.events = new LosslessCutEvents(this);
        this.nodeIntegration = new LosslessCutNodeIntegration(this);
    }

    setupInterface() {
        const container = this.ui.createInterface();
        this.events.setupEventListeners();

        // Sync video player time updates to timeline
        if (this.ui.videoElement) {
            this.ui.videoElement.addEventListener('timeupdate', () => {
                if (this.videoData) {
                    const time = this.ui.videoElement.currentTime;
                    this.currentRawTime = time;
                    this.currentFrame = Math.floor(time * this.videoData.fps);
                    this.timeline.currentFrame = this.currentFrame;
                    this.timeline.drawTimeline();
                    this.ui.updateDisplays();
                }
            });

            this.ui.videoElement.addEventListener('play', () => {
                this.isPlaying = true;
                this.ui.updatePlayButton(true);
            });

            this.ui.videoElement.addEventListener('pause', () => {
                this.isPlaying = false;
                this.ui.updatePlayButton(false);
            });
        }

        return container;
    }

    setInPoint(time = null) {
        if (!this.videoData) return;
        let targetTime = time !== null ? time : this.currentRawTime;

        if (this.losslessLock) {
            targetTime = this.snapToKeyframe(targetTime);
        }

        this.inPoint = targetTime;
        this.timeline.inPoint = this.inPoint;
        this.timeline.drawTimeline();
        this.ui.updateDisplays();
    }

    setOutPoint(time = null) {
        if (!this.videoData) return;
        let targetTime = time !== null ? time : this.currentRawTime;

        if (this.losslessLock) {
            targetTime = this.snapToKeyframe(targetTime);
        }

        this.outPoint = targetTime;
        this.timeline.outPoint = this.outPoint;
        this.timeline.drawTimeline();
        this.ui.updateDisplays();
    }

    snapToKeyframe(time) {
        if (!this.videoData || !this.videoData.keyframes || this.videoData.keyframes.length === 0) {
            return time;
        }

        let nearest = this.videoData.keyframes[0];
        let minDist = Math.abs(time - nearest);

        for (const kf of this.videoData.keyframes) {
            const dist = Math.abs(time - kf);
            if (dist < minDist) {
                minDist = dist;
                nearest = kf;
            }
        }

        return nearest;
    }

    toggleLosslessLock() {
        this.losslessLock = !this.losslessLock;
        if (this.ui) this.ui.updateLockButton(this.losslessLock);
    }

    gotoPrevKeyframe() {
        if (!this.videoData || !this.videoData.keyframes) return;
        const currentTime = this.currentRawTime;

        // Find nearest keyframe before current time (with small tolerance)
        const prev = this.videoData.keyframes
            .filter(k => k < currentTime - 0.01)
            .sort((a, b) => b - a)[0]; // max of values smaller than current

        if (prev !== undefined) {
            this.seekTo(prev);
        } else {
            this.seekTo(0);
        }
    }

    gotoNextKeyframe() {
        if (!this.videoData || !this.videoData.keyframes) return;
        const currentTime = this.currentRawTime;

        const next = this.videoData.keyframes
            .filter(k => k > currentTime + 0.01)
            .sort((a, b) => a - b)[0]; // min of values larger

        if (next !== undefined) {
            this.seekTo(next);
        } else {
            // No more keyframes, go to end
            this.seekTo(this.videoData.duration);
        }
    }

    performCut() {
        this.nodeIntegration.syncWidgets();
        // Trigger graph execution
        if (window.app && window.app.queuePrompt) {
            window.app.queuePrompt(0, 1);
        }
    }

    seekTo(time) {
        if (!this.videoData) return;

        // Clamp time
        time = Math.max(0, Math.min(time, this.videoData.duration));

        this.currentRawTime = time;
        this.currentFrame = Math.floor(time * this.videoData.fps);
        this.timeline.currentFrame = this.currentFrame;

        if (this.ui.videoElement && Math.abs(this.ui.videoElement.currentTime - time) > 0.1) {
            this.ui.videoElement.currentTime = time;
        }

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
        const time = (this.currentFrame - 1) / this.videoData.fps;
        this.seekTo(time);
    }

    stepForward() {
        if (!this.videoData) return;
        const time = (this.currentFrame + 1) / this.videoData.fps;
        this.seekTo(time);
    }

    togglePlay() {
        if (!this.ui.videoElement) return;
        if (this.ui.videoElement.paused) {
            this.ui.videoElement.play();
        } else {
            this.ui.videoElement.pause();
        }
    }
}
