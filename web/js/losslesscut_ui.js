export class LosslessCutUI {
    constructor(core) {
        this.core = core;
        this.container = null;
        this.videoElement = null;
        this.inDisplay = null;
        this.outDisplay = null;
        this.posDisplay = null;
    }

    createInterface() {
        this.container = document.createElement('div');
        this.container.className = 'losslesscut-interface';
        this.container.style.display = 'flex';
        this.container.style.flexDirection = 'column';
        this.container.style.height = '100%';
        this.container.style.background = '#222';
        this.container.style.color = '#ddd';

        // 1. Video Preview
        this.videoElement = document.createElement('video');
        this.videoElement.style.width = '100%';
        this.videoElement.style.maxHeight = '300px';
        this.videoElement.style.background = '#000';
        this.videoElement.controls = false; // We use our own controls
        this.container.appendChild(this.videoElement);

        // 2. Timeline
        const timeline = this.core.timeline.setupCanvas();
        this.container.appendChild(timeline);

        // 3. Controls (Buttons)
        const controls = this.createControls();
        this.container.appendChild(controls);

        // 4. Info Panel (Timecodes)
        const infoPanel = this.createInfoPanel();
        this.container.appendChild(infoPanel);

        return this.container;
    }

    createControls() {
        const controlsDiv = document.createElement('div');
        controlsDiv.style.cssText = `
            display: flex;
            gap: 5px;
            margin-top: 10px;
            flex-wrap: wrap;
            justify-content: center;
        `;

        const buttonStyle = `
            padding: 5px 10px;
            background: #444;
            color: #fff;
            border: 1px solid #666;
            border-radius: 3px;
            cursor: pointer;
            font-size: 12px;
            min-width: 30px;
        `;

        this.addButton(controlsDiv, '|<', buttonStyle, () => this.core.goToStart(), 'Jump to start (Home)');
        this.addButton(controlsDiv, '<< KF', buttonStyle, () => this.core.gotoPrevKeyframe(), 'Prev Keyframe (Left Arrow)');
        this.addButton(controlsDiv, '-1', buttonStyle, () => this.core.stepBackward(), 'Step back 1 frame (Shift + Left Arrow)');

        // Play/Pause button needs state update
        this.playButton = this.addButton(controlsDiv, '▶', buttonStyle, () => this.core.togglePlay(), 'Play/Pause (Space)');

        this.addButton(controlsDiv, '+1', buttonStyle, () => this.core.stepForward(), 'Step forward 1 frame (Shift + Right Arrow)');
        this.addButton(controlsDiv, 'KF >>', buttonStyle, () => this.core.gotoNextKeyframe(), 'Next Keyframe (Right Arrow)');
        this.addButton(controlsDiv, '>|', buttonStyle, () => this.core.goToEnd(), 'Jump to end (End)');

        const separator = document.createElement('div');
        separator.style.width = '10px';
        controlsDiv.appendChild(separator);

        const inButton = this.addButton(controlsDiv, '[ IN', buttonStyle, () => this.core.setInPoint(), 'Set IN point (I)');
        inButton.style.background = '#006600';

        const outButton = this.addButton(controlsDiv, 'OUT ]', buttonStyle, () => this.core.setOutPoint(), 'Set OUT point (O)');
        outButton.style.background = '#660000';

        const separator2 = document.createElement('div');
        separator2.style.width = '10px';
        controlsDiv.appendChild(separator2);

        const cutButton = this.addButton(controlsDiv, '✂ CUT', buttonStyle, () => this.core.performCut(), 'Execute Cut');
        cutButton.style.background = '#0066cc';
        cutButton.style.fontWeight = 'bold';

        // Zoom controls
        const zoomDiv = document.createElement('div');
        zoomDiv.style.marginLeft = 'auto';
        this.addButton(controlsDiv, '-', buttonStyle, () => this.core.zoomOut(), 'Zoom Out');
        this.addButton(controlsDiv, '+', buttonStyle, () => this.core.zoomIn(), 'Zoom In');

        return controlsDiv;
    }

    createInfoPanel() {
        const infoDiv = document.createElement('div');
        infoDiv.style.cssText = `
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-top: 10px;
            font-family: monospace;
            font-size: 11px;
            padding: 5px;
        `;

        this.inDisplay = this.createInfoBox(infoDiv, 'IN Point', '00:00:00:00', '#006600');
        this.outDisplay = this.createInfoBox(infoDiv, 'OUT Point', '00:00:00:00', '#660000');
        this.posDisplay = this.createInfoBox(infoDiv, 'Position', '00:00:00:00', '#0066cc');

        return infoDiv;
    }

    createInfoBox(parent, label, value, color) {
        const box = document.createElement('div');
        box.style.cssText = `
            background: ${color}22;
            border: 2px solid ${color};
            padding: 4px;
            border-radius: 4px;
            text-align: center;
        `;

        const labelSpan = document.createElement('div');
        labelSpan.textContent = label;
        labelSpan.style.cssText = 'color: #aaa; font-size: 10px; font-weight: bold; text-transform: uppercase;';

        const valueSpan = document.createElement('div');
        valueSpan.textContent = value;
        valueSpan.style.cssText = `
            color: ${color}; 
            font-size: 14px; 
            font-weight: bold; 
            font-family: 'Courier New', monospace;
            margin-top: 2px;
        `;

        box.appendChild(labelSpan);
        box.appendChild(valueSpan);
        parent.appendChild(box);

        return valueSpan;
    }

    addButton(parent, text, style, onClick, tooltip = '') {
        const btn = document.createElement('button');
        btn.textContent = text;
        btn.style.cssText = style;
        if (tooltip) btn.title = tooltip;

        btn.addEventListener('click', onClick);
        btn.addEventListener('mouseenter', () => btn.style.opacity = '0.8');
        btn.addEventListener('mouseleave', () => btn.style.opacity = '1');
        parent.appendChild(btn);
        return btn;
    }

    updateDisplays() {
        if (this.core.videoData) {
            this.inDisplay.textContent = this.core.timeline.formatTimecode(this.core.inPoint);
            this.outDisplay.textContent = this.core.timeline.formatTimecode(this.core.outPoint);
            this.posDisplay.textContent = this.core.timeline.formatTimecode(
                this.core.currentFrame / this.core.videoData.fps
            );
        }
    }

    updatePlayButton(isPlaying) {
        if (this.playButton) {
            this.playButton.textContent = isPlaying ? '⏸' : '▶';
        }
    }
}
