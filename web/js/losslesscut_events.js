export class LosslessCutEvents {
    constructor(core) {
        this.core = core;
        this.isDragging = false;
        this.dragType = null;
    }

    setupEventListeners() {
        const canvas = this.core.timeline.canvas;

        canvas.addEventListener('mousedown', (e) => this.handleMouseDown(e));
        canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
        canvas.addEventListener('mouseup', (e) => this.handleMouseUp(e));
        canvas.addEventListener('wheel', (e) => this.handleWheel(e));
        canvas.addEventListener('dblclick', (e) => this.handleDoubleClick(e));

        document.addEventListener('keydown', (e) => this.handleKeyDown(e));
    }

    handleMouseDown(e) {
        const rect = this.core.timeline.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const time = this.core.timeline.pixelToTime(x, rect.width);

        if (e.button === 0) { // Left click
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
        if (!this.isDragging) return;

        const rect = this.core.timeline.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;

        if (this.dragType === 'seek') {
            const time = this.core.timeline.pixelToTime(x, rect.width);
            this.core.seekTo(time);
        } else if (this.dragType === 'pan') {
            const timeDelta = this.core.timeline.pixelToTime(x - this.dragStartX, rect.width);
            this.core.timeline.scrollOffset -= timeDelta;
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

        if (e.ctrlKey) {
            if (e.deltaY < 0) {
                this.core.zoomIn();
            } else {
                this.core.zoomOut();
            }
        } else {
            const scrollAmount = (e.deltaY / 100) * (this.core.videoData.duration / 10);
            this.core.timeline.scrollOffset += scrollAmount;
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
        if (!this.core.timeline.canvas.contains(document.activeElement)) return;

        switch(e.key) {
            case ' ':
                e.preventDefault();
                this.core.togglePlay();
                break;
            case 'ArrowLeft':
                e.preventDefault();
                if (e.shiftKey) {
                    this.core.gotoPrevKeyframe();
                } else {
                    this.core.stepBackward();
                }
                break;
            case 'ArrowRight':
                e.preventDefault();
                if (e.shiftKey) {
                    this.core.gotoNextKeyframe();
                } else {
                    this.core.stepForward();
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
        if (!this.core.videoData.keyframes) return null;

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
