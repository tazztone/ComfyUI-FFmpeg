export class LosslessCutTimeline {
    constructor(core) {
        this.core = core;
        this.canvas = null;
        this.ctx = null;
        this.videoData = null;
        this.zoomLevel = 1;
        this.scrollOffset = 0;
        this.inPoint = 0;
        this.outPoint = 0;
        this.currentFrame = 0;
    }

    setupCanvas() {
        this.canvas = document.createElement('canvas');
        this.canvas.style.width = '100%';
        this.canvas.style.height = '40px';
        this.canvas.style.border = '1px solid #333';
        this.canvas.style.backgroundColor = '#1a1a1a'; // Dark bg to ensure visibility

        // Set default size
        this.canvas.width = 600;
        this.canvas.height = 150;
        this.ctx = this.canvas.getContext('2d');

        // Draw placeholder immediately
        this.drawPlaceholder();

        // Use ResizeObserver to handle actual size after attachment.
        const resizeObserver = new ResizeObserver((entries) => {
            for (const entry of entries) {
                const rect = entry.contentRect;
                if (rect.width > 0 && rect.height > 0) {
                    this.canvas.width = rect.width * devicePixelRatio;
                    this.canvas.height = rect.height * devicePixelRatio;
                    this.ctx.setTransform(1, 0, 0, 1, 0, 0); // Reset transform
                    this.ctx.scale(devicePixelRatio, devicePixelRatio);

                    if (this.videoData) {
                        this.drawTimeline();
                    } else {
                        this.drawPlaceholder();
                    }
                }
            }
        });
        resizeObserver.observe(this.canvas);

        return this.canvas;
    }

    drawPlaceholder() {
        // Use CSS pixel dimensions (before devicePixelRatio scaling)
        const width = this.canvas.width / (window.devicePixelRatio || 1);
        const height = this.canvas.height / (window.devicePixelRatio || 1);

        this.ctx.fillStyle = '#1a1a1a';
        this.ctx.fillRect(0, 0, width, height);
        this.ctx.fillStyle = '#888';
        this.ctx.font = '14px monospace';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText(
            'No video metadata loaded. Please connect a video.',
            width / 2,
            height / 2
        );
    }

    drawTimeline() {
        if (!this.videoData) {
            this.drawInitialMessage();
            return;
        }

        const ctx = this.ctx;
        const width = this.canvas.width / devicePixelRatio;
        const height = this.canvas.height / devicePixelRatio;

        ctx.fillStyle = '#1a1a1a';
        ctx.fillRect(0, 0, width, height);

        this.drawRuler(ctx, width, height);
        this.drawKeyframes(ctx, width, height);
        this.drawInOutRegion(ctx, width, height);
        this.drawPlayhead(ctx, width, height);
    }

    drawInitialMessage() {
        const ctx = this.ctx;
        const width = this.canvas.width / devicePixelRatio;
        const height = this.canvas.height / devicePixelRatio;

        ctx.fillStyle = '#1a1a1a';
        ctx.fillRect(0, 0, width, height);
        ctx.fillStyle = '#999';
        ctx.font = '14px monospace';
        ctx.textAlign = 'center';
        ctx.fillText('No video metadata loaded. Please connect a video.', width / 2, height / 2);
    }

    drawRuler(ctx, width, height) {
        ctx.strokeStyle = '#333';
        ctx.fillStyle = '#999';
        ctx.font = '10px monospace';

        const duration = this.videoData.duration;
        const visibleDuration = duration / this.zoomLevel;
        const startTime = this.scrollOffset;
        const endTime = startTime + visibleDuration;

        const tickInterval = this.calculateTickInterval(visibleDuration);

        for (let time = 0; time <= duration; time += tickInterval) {
            if (time < startTime || time > endTime) continue;

            const x = this.timeToPixel(time, width);
            ctx.beginPath();
            ctx.moveTo(x, height - 20);
            ctx.lineTo(x, height);
            ctx.stroke();

            ctx.fillText(this.formatTimecode(time), x + 2, height - 5);
        }
    }

    drawKeyframes(ctx, width, height) {
        if (!this.videoData.keyframes) return;

        // Make keyframes less intrusive
        ctx.fillStyle = 'rgba(0, 255, 0, 0.4)';
        ctx.strokeStyle = 'rgba(0, 255, 0, 0.4)';
        ctx.lineWidth = 1;

        for (let kfTime of this.videoData.keyframes) {
            const x = this.timeToPixel(kfTime, width);

            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, height - 25);
            ctx.stroke();

            // Small triangle at top
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x + 3, 3);
            ctx.lineTo(x, 6);
            ctx.lineTo(x - 3, 3);
            ctx.closePath();
            ctx.fill();
        }
    }

    drawInOutRegion(ctx, width, height) {
        const inX = this.timeToPixel(this.inPoint, width);
        const outX = this.timeToPixel(this.outPoint, width);

        // 1. Darken areas OUTSIDE the selection
        ctx.fillStyle = 'rgba(0, 0, 0, 0.65)';
        // Left side (start to IN)
        if (inX > 0) {
            ctx.fillRect(0, 0, inX, height);
        }
        // Right side (OUT to end)
        if (outX < width) {
            ctx.fillRect(outX, 0, width - outX, height);
        }

        // 2. Highlight SELECTED region slightly
        ctx.fillStyle = 'rgba(255, 255, 255, 0.05)';
        ctx.fillRect(inX, 0, outX - inX, height - 25);

        // 3. Draw IN Marker
        ctx.fillStyle = '#00ff00';
        ctx.fillRect(inX - 2, 0, 4, height); // Full height line

        // 4. Draw OUT Marker
        ctx.fillStyle = '#ff3333';
        ctx.fillRect(outX - 2, 0, 4, height); // Full height line

        // 5. Draw labels (handle overlap)
        ctx.font = 'bold 12px sans-serif';
        const labelDistance = outX - inX;

        if (labelDistance < 60) {
            // Too close - put IN above, OUT below
            ctx.fillStyle = '#00ff00';
            ctx.textAlign = 'center';
            ctx.fillText('IN', inX, 15);

            ctx.fillStyle = '#ff3333';
            ctx.fillText('OUT', outX, 30);
        } else {
            // Normal - labels next to markers
            ctx.fillStyle = '#00ff00';
            ctx.textAlign = 'left';
            ctx.fillText('IN', inX + 6, 15);

            ctx.fillStyle = '#ff3333';
            ctx.textAlign = 'right';
            ctx.fillText('OUT', outX - 6, 15);
        }
    }

    drawPlayhead(ctx, width, height) {
        const x = this.timeToPixel(this.currentFrame / this.videoData.fps, width);

        ctx.strokeStyle = '#ff00ff';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
        ctx.lineWidth = 1;

        ctx.fillStyle = '#ff00ff';
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x - 5, 10);
        ctx.lineTo(x + 5, 10);
        ctx.closePath();
        ctx.fill();
    }

    timeToPixel(time, width) {
        const visibleDuration = this.videoData.duration / this.zoomLevel;
        const startTime = this.scrollOffset;
        return ((time - startTime) / visibleDuration) * width;
    }

    pixelToTime(pixel, width) {
        const visibleDuration = this.videoData.duration / this.zoomLevel;
        const startTime = this.scrollOffset;
        return startTime + (pixel / width) * visibleDuration;
    }

    calculateTickInterval(duration) {
        if (duration < 10) return 1;
        if (duration < 60) return 5;
        if (duration < 300) return 30;
        return 60;
    }

    formatTimecode(seconds) {
        const h = Math.floor(seconds / 3600).toString().padStart(2, '0');
        const m = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0');
        const s = Math.floor(seconds % 60).toString().padStart(2, '0');
        const f = Math.floor((seconds % 1) * this.videoData.fps).toString().padStart(2, '0');
        return `${h}:${m}:${s}:${f}`;
    }
}
