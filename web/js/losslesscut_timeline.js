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
        this.canvas.style.height = '150px';
        this.canvas.style.border = '1px solid #333';

        const rect = this.canvas.getBoundingClientRect();
        this.canvas.width = rect.width * devicePixelRatio;
        this.canvas.height = rect.height * devicePixelRatio;
        this.ctx = this.canvas.getContext('2d');
        this.ctx.scale(devicePixelRatio, devicePixelRatio);

        return this.canvas;
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

        ctx.fillStyle = '#00ff00';
        ctx.strokeStyle = '#00ff00';

        for (let kfTime of this.videoData.keyframes) {
            const x = this.timeToPixel(kfTime, width);

            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, height - 25);
            ctx.stroke();

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

        ctx.fillStyle = 'rgba(255, 255, 0, 0.2)';
        ctx.fillRect(inX, 0, outX - inX, height - 25);

        ctx.fillStyle = '#00ff00';
        ctx.fillRect(inX - 2, 0, 4, height - 25);
        ctx.fillText('IN', inX + 5, 15);

        ctx.fillStyle = '#ff0000';
        ctx.fillRect(outX - 2, 0, 4, height - 25);
        ctx.fillText('OUT', outX - 50, 15);
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
