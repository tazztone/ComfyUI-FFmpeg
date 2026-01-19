import { app } from "/scripts/app.js";
import { LosslessCutCore } from './losslesscut_core.js';

app.registerExtension({
    name: "Comfy.LosslessCut.Enhanced",

    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "LosslessCutV3") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;

            nodeType.prototype.onNodeCreated = function() {
                onNodeCreated?.apply(this, arguments);

                const widgetsToHide = ['action', 'in_point', 'out_point', 'current_position'];
                widgetsToHide.forEach(name => {
                    const widget = this.widgets.find(w => w.name === name);
                    if (widget) widget.type = "hidden";
                });

                this.losslessCutCore = new LosslessCutCore(this);
                const interfaceContainer = this.losslessCutCore.setupInterface();

                this.addDOMWidget("losslesscut_ui", "customtext", interfaceContainer);

                // Listen for server-side updates
                api.addEventListener("comfyui-ffmpeg-losslesscut-update", (event) => {
                    const { node_id, in_point, out_point, current_position } = event.detail;
                    if (String(node_id) !== String(this.id)) return;

                    if (this.losslessCutCore.videoData) {
                        this.losslessCutCore.inPoint = in_point;
                        this.losslessCutCore.outPoint = out_point;
                        this.losslessCutCore.currentFrame = Math.floor(current_position * this.losslessCutCore.videoData.fps);

                        this.losslessCutCore.timeline.inPoint = in_point;
                        this.losslessCutCore.timeline.outPoint = out_point;
                        this.losslessCutCore.timeline.currentFrame = this.losslessCutCore.currentFrame;

                        this.losslessCutCore.timeline.drawTimeline();
                        this.losslessCutCore.ui.updateDisplays();
                    }
                });
            };

            // onExecuted fallback or removal - V3 might not trigger this with UI data anymore
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);
                // Legacy support or if we decide to pass data via output in the future
            };
        }
    }
});
