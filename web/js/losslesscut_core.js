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

        // Multiple Segments Support
        this.segments = []; // Array of {in: number, out: number}
        this.activeSegmentIndex = 0; // Currently editing segment

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

    initializeDefaultSegment() {
        // Create initial segment covering full video
        if (this.videoData && this.segments.length === 0) {
            this.segments = [{ in: 0, out: this.videoData.duration }];
            this.activeSegmentIndex = 0;
            this.inPoint = 0;
            this.outPoint = this.videoData.duration;
        }
    }

    setInPoint(time = null) {
        if (!this.videoData) return;
        let targetTime = time !== null ? time : this.currentRawTime;

        if (this.losslessLock) {
            targetTime = this.snapToKeyframe(targetTime);
        }

        // Check if this IN point is outside all existing segments
        const isInsideExisting = this.segments.some(seg =>
            targetTime >= seg.in && targetTime <= seg.out
        );

        if (!isInsideExisting && this.segments.length > 0) {
            // Auto-create new segment starting at this point
            const newSegment = {
                in: targetTime,
                out: this.videoData.duration // Default to end, user will adjust
            };
            this.segments.push(newSegment);
            this.activeSegmentIndex = this.segments.length - 1;
            console.log(`[LosslessCut] Created new segment #${this.activeSegmentIndex}`);
        }

        this.inPoint = targetTime;

        // Update active segment
        if (this.segments.length > 0 && this.activeSegmentIndex < this.segments.length) {
            this.segments[this.activeSegmentIndex].in = targetTime;
        }

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

        // Update active segment
        if (this.segments.length > 0 && this.activeSegmentIndex < this.segments.length) {
            this.segments[this.activeSegmentIndex].out = targetTime;
        }

        this.timeline.outPoint = this.outPoint;
        this.timeline.drawTimeline();
        this.ui.updateDisplays();
    }

    deleteSegment(index) {
        if (index < 0 || index >= this.segments.length) return;
        if (this.segments.length <= 1) {
            // Can't delete last segment, just reset it
            this.segments[0] = { in: 0, out: this.videoData.duration };
            this.activeSegmentIndex = 0;
        } else {
            this.segments.splice(index, 1);
            if (this.activeSegmentIndex >= this.segments.length) {
                this.activeSegmentIndex = this.segments.length - 1;
            }
        }

        // Sync active segment to inPoint/outPoint
        const active = this.segments[this.activeSegmentIndex];
        this.inPoint = active.in;
        this.outPoint = active.out;
        this.timeline.inPoint = this.inPoint;
        this.timeline.outPoint = this.outPoint;
        this.timeline.drawTimeline();
        this.ui.updateDisplays();
    }

    selectSegment(index) {
        if (index < 0 || index >= this.segments.length) return;
        this.activeSegmentIndex = index;
        const seg = this.segments[index];
        this.inPoint = seg.in;
        this.outPoint = seg.out;
        this.timeline.inPoint = this.inPoint;
        this.timeline.outPoint = this.outPoint;
        this.timeline.drawTimeline();
        this.ui.updateDisplays();
    }

    snapToKeyframe(time) {
        if (!this.videoData || !this.videoData.keyframes || this.videoData.keyframes.length === 0) {
            return time;
        }
        const keyframes = this.videoData.keyframes;

        let low = 0;
        let high = keyframes.length - 1;

        if (time <= keyframes[low]) return keyframes[low];
        if (time >= keyframes[high]) return keyframes[high];

        while (low <= high) {
            let mid = Math.floor((low + high) / 2);
            if (keyframes[mid] === time) return keyframes[mid];
            if (keyframes[mid] < time) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }

        return (Math.abs(keyframes[low] - time) < Math.abs(keyframes[high] - time))
            ? keyframes[low]
            : keyframes[high];
    }

    toggleLosslessLock() {
        this.losslessLock = !this.losslessLock;
        if (this.ui) this.ui.updateLockButton(this.losslessLock);
    }

    gotoPrevKeyframe() {
        if (!this.videoData || !this.videoData.keyframes || this.videoData.keyframes.length === 0) return;
        const currentTime = this.currentRawTime;
        const keyframes = this.videoData.keyframes;
        const target = currentTime - 0.01;

        let low = 0;
        let high = keyframes.length - 1;
        let prev = undefined;

        while (low <= high) {
            let mid = Math.floor((low + high) / 2);
            if (keyframes[mid] < target) {
                prev = keyframes[mid];
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }

        if (prev !== undefined) {
            this.seekTo(prev);
        } else {
            this.seekTo(0);
        }
    }

    gotoNextKeyframe() {
        if (!this.videoData || !this.videoData.keyframes || this.videoData.keyframes.length === 0) return;
        const currentTime = this.currentRawTime;
        const keyframes = this.videoData.keyframes;
        const target = currentTime + 0.01;

        let low = 0;
        let high = keyframes.length - 1;
        let next = undefined;

        while (low <= high) {
            let mid = Math.floor((low + high) / 2);
            if (keyframes[mid] > target) {
                next = keyframes[mid];
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }

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

    takeScreenshot() {
        // Set screenshot widget to export at current playhead
        this.nodeIntegration.syncWidgetsForScreenshot();
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

