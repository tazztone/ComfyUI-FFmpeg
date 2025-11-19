import { app } from "/scripts/app.js";
import { LosslessCutCore } from './losslesscut_core.js';

app.registerExtension({
    name: "Comfy.LosslessCut.Enhanced",

    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "LosslessCut") {
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
            };

            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);
                if (message.ui && this.losslessCutCore.videoData) {
                    this.losslessCutCore.inPoint = message.ui.in_point;
                    this.losslessCutCore.outPoint = message.ui.out_point;
                    this.losslessCutCore.currentFrame = Math.floor(message.ui.current_position * this.losslessCutCore.videoData.fps);

                    this.losslessCutCore.timeline.inPoint = message.ui.in_point;
                    this.losslessCutCore.timeline.outPoint = message.ui.out_point;
                    this.losslessCutCore.timeline.currentFrame = this.losslessCutCore.currentFrame;

                    this.losslessCutCore.timeline.drawTimeline();
                    this.losslessCutCore.ui.updateDisplays();
                }
            };
        }
    }
});
