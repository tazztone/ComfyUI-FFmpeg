export class LosslessCutUI {
    constructor(core) {
        this.core = core;
        this.container = null;
    }

    createInterface() {
        this.container = document.createElement('div');
        this.container.className = 'losslesscut-interface';

        const timeline = this.core.timeline.setupCanvas();
        this.container.appendChild(timeline);

        const controls = this.createControls();
        this.container.appendChild(controls);

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
        `;

        const buttonStyle = `
            padding: 5px 10px;
            background: #444;
            color: #fff;
            border: 1px solid #666;
            border-radius: 3px;
            cursor: pointer;
            font-size: 12px;
        `;

        this.addButton(controlsDiv, '|< Start', buttonStyle, () => this.core.goToStart(), 'Jump to start');
        this.addButton(controlsDiv, '<< Prev KF', buttonStyle, () => this.core.gotoPrevKeyframe(), 'Go to previous keyframe');
        this.addButton(controlsDiv, '< Frame', buttonStyle, () => this.core.stepBackward(), 'Step back 1 frame');
        this.addButton(controlsDiv, '▶️ Play', buttonStyle, () => this.core.togglePlay(), 'Play/Pause (not fully implemented)');
        this.addButton(controlsDiv, 'Frame >', buttonStyle, () => this.core.stepForward(), 'Step forward 1 frame');
        this.addButton(controlsDiv, 'Next KF >>', buttonStyle, () => this.core.gotoNextKeyframe(), 'Go to next keyframe');
        this.addButton(controlsDiv, 'End >|', buttonStyle, () => this.core.goToEnd(), 'Jump to end');

        const inButton = this.addButton(controlsDiv, '[ Set IN', buttonStyle, () => this.core.setInPoint(), 'Mark IN point at current position');
        inButton.style.background = '#006600';

        const outButton = this.addButton(controlsDiv, 'Set OUT ]', buttonStyle, () => this.core.setOutPoint(), 'Mark OUT point at current position');
        outButton.style.background = '#660000';

        const cutButton = this.addButton(controlsDiv, '✂️ Cut', buttonStyle, () => this.core.performCut(), 'Cut video from IN to OUT');
        cutButton.style.background = '#0066cc';
        cutButton.style.fontWeight = 'bold';

        this.addButton(controlsDiv, 'Zoom -', buttonStyle, () => this.core.zoomOut(), 'Zoom out timeline');
        this.addButton(controlsDiv, 'Zoom +', buttonStyle, () => this.core.zoomIn(), 'Zoom in timeline');
        this.addButton(controlsDiv, 'Fit', buttonStyle, () => this.core.resetZoom(), 'Fit entire video in timeline');

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
            padding: 8px;
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
            font-size: 16px; 
            font-weight: bold; 
            font-family: 'Courier New', monospace;
            margin-top: 4px;
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
        btn.addEventListener('mouseenter', () => btn.style.background = '#555');
        btn.addEventListener('mouseleave', () => {
            if (text.includes('Set IN')) {
                btn.style.background = '#006600';
            } else if (text.includes('Set OUT')) {
                btn.style.background = '#660000';
            } else if (text.includes('Cut')) {
                btn.style.background = '#0066cc';
            } else {
                btn.style.background = '#444';
            }
        });
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
}
