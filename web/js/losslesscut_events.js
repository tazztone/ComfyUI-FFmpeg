export class LosslessCutEvents {
    constructor(core) {
        this.core = core;
        this.isDragging = false;
        this.dragType = null;
        this.dragStartX = 0;
    }

    setupEventListeners() {
        const canvas = this.core.timeline.canvas;

        canvas.addEventListener('mousedown', (e) => this.handleMouseDown(e));
        window.addEventListener('mousemove', (e) => this.handleMouseMove(e)); // Window for drag outside
        window.addEventListener('mouseup', (e) => this.handleMouseUp(e));
        canvas.addEventListener('wheel', (e) => this.handleWheel(e));
        canvas.addEventListener('dblclick', (e) => this.handleDoubleClick(e));

        document.addEventListener('keydown', (e) => this.handleKeyDown(e));

        // Ensure container can take focus for key events
        if (this.core.ui.container) {
            this.core.ui.container.tabIndex = 0;
            this.core.ui.container.addEventListener('click', () => {
                this.core.ui.container.focus();
            });
        }
    }

    handleMouseDown(e) {
        const rect = this.core.timeline.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const time = this.core.timeline.pixelToTime(x, rect.width);

        if (e.button === 0) { // Left click
            // Check if clicking near IN or OUT marker (within 10px)
            const inX = this.core.timeline.timeToPixel(this.core.inPoint, rect.width);
            const outX = this.core.timeline.timeToPixel(this.core.outPoint, rect.width);

            const hitThreshold = 10;

            if (Math.abs(x - inX) < hitThreshold) {
                this.isDragging = true;
                this.dragType = 'in_marker';
                return;
            } else if (Math.abs(x - outX) < hitThreshold) {
                this.isDragging = true;
                this.dragType = 'out_marker';
                return;
            }

            if (e.shiftKey) {
                this.core.setInPoint(time);
            } else if (e.ctrlKey) {
                this.core.setOutPoint(time);
            } else {
                this.isDragging = true;
                this.dragType = 'seek';
                this.core.seekTo(time);
            }
        } else if (e.button === 1) { // Middle click
            this.isDragging = true;
            this.dragType = 'pan';
            this.dragStartX = x;
        }
    }

    handleMouseMove(e) {
        const rect = this.core.timeline.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;

        if (!this.isDragging) {
            // Hover logic for cursor
            const inX = this.core.timeline.timeToPixel(this.core.inPoint, rect.width);
            const outX = this.core.timeline.timeToPixel(this.core.outPoint, rect.width);
            const hitThreshold = 10;

            if (Math.abs(x - inX) < hitThreshold || Math.abs(x - outX) < hitThreshold) {
                this.core.timeline.canvas.style.cursor = 'ew-resize';
            } else {
                this.core.timeline.canvas.style.cursor = 'default';
            }
            return;
        }

        const time = this.core.timeline.pixelToTime(x, rect.width);

        if (this.dragType === 'seek') {
            this.core.seekTo(time);
        } else if (this.dragType === 'in_marker') {
            this.core.setInPoint(time);
            this.core.seekTo(time); // Update video preview
        } else if (this.dragType === 'out_marker') {
            this.core.setOutPoint(time);
            this.core.seekTo(time); // Update video preview
        } else if (this.dragType === 'pan') {
            const visibleDuration = this.core.videoData.duration / this.core.timeline.zoomLevel;
            const dt = ((x - this.dragStartX) / rect.width) * visibleDuration;

            this.core.timeline.scrollOffset -= dt;
            this.core.timeline.drawTimeline();
            this.dragStartX = x;
        }
    }

    handleMouseUp(e) {
        this.isDragging = false;
        this.dragType = null;
    }

    handleWheel(e) {
        e.preventDefault();

        const rect = this.core.timeline.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;

        // Calculate time at mouse position BEFORE zoom
        const mouseTime = this.core.timeline.pixelToTime(x, rect.width);

        if (e.ctrlKey || e.deltaY !== 0) { // Always Zoom on wheel
            const zoomFactor = 1.1; // Smoother zoom

            if (e.deltaY < 0) {
                // Zoom In
                this.core.timeline.zoomLevel = Math.min(this.core.timeline.zoomLevel * zoomFactor, 200);
            } else {
                // Zoom Out
                this.core.timeline.zoomLevel = Math.max(this.core.timeline.zoomLevel / zoomFactor, 1);
            }

            // Calculate new scroll offset to keep mouseTime at the same pixel position
            // pixel = (time - scrollOffset) / duration * width * zoom
            // mouseTime = scrollOffset + (pixel / width) * (duration / zoom)
            // scrollOffset = mouseTime - (pixel / width) * (duration / zoom)

            const visibleDuration = this.core.videoData.duration / this.core.timeline.zoomLevel;
            const newScrollOffset = mouseTime - (x / rect.width) * visibleDuration;

            // Clamp scroll offset
            this.core.timeline.scrollOffset = Math.max(0, Math.min(newScrollOffset, this.core.videoData.duration - visibleDuration));

            this.core.timeline.drawTimeline();
        }
    }

    handleDoubleClick(e) {
        const rect = this.core.timeline.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const time = this.core.timeline.pixelToTime(x, rect.width);

        const nearestKF = this.findNearestKeyframe(time);
        if (nearestKF !== null) {
            this.core.seekTo(nearestKF);
        }
    }

    handleKeyDown(e) {
        // Check if focus is within our UI container OR the video element
        const active = document.activeElement;
        const container = this.core.ui.container;

        if (!container || (!container.contains(active) && container !== active)) {
            return;
        }

        switch (e.key) {
            case ' ':
                e.preventDefault();
                this.core.togglePlay();
                break;
            case 'ArrowLeft':
                e.preventDefault();
                if (e.shiftKey) {
                    this.core.stepBackward();
                } else {
                    this.core.gotoPrevKeyframe();
                }
                break;
            case 'ArrowRight':
                e.preventDefault();
                if (e.shiftKey) {
                    this.core.stepForward();
                } else {
                    this.core.gotoNextKeyframe();
                }
                break;
            case 'i':
            case 'I':
                this.core.setInPoint();
                break;
            case 'o':
            case 'O':
                this.core.setOutPoint();
                break;
            case 'Home':
                this.core.goToStart();
                break;
            case 'End':
                this.core.goToEnd();
                break;
        }
    }

    findNearestKeyframe(time) {
        if (!this.core.videoData || !this.core.videoData.keyframes) return null;

        let nearest = null;
        let minDist = Infinity;

        for (let kf of this.core.videoData.keyframes) {
            const dist = Math.abs(kf - time);
            if (dist < minDist) {
                minDist = dist;
                nearest = kf;
            }
        }

        return nearest;
    }
}
