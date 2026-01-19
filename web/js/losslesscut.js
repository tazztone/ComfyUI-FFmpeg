import { app } from "/scripts/app.js";
import { api } from "/scripts/api.js";
import { LosslessCutCore } from './losslesscut_core.js';

app.registerExtension({
    name: "Comfy.LosslessCut.Enhanced",

    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "LosslessCutV3") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;

            nodeType.prototype.onNodeCreated = function () {
                onNodeCreated?.apply(this, arguments);

                const widgetsToHide = ['action', 'in_point', 'out_point', 'current_position'];

                // Store hidden widget references for later access by queueAction
                this._hiddenWidgets = {};

                // Hide widgets properly by removing them from render
                requestAnimationFrame(() => {
                    // Filter out the widgets we want to hide from the widgets array
                    // but keep references so we can still update their values
                    const newWidgets = [];
                    for (const widget of this.widgets || []) {
                        if (widgetsToHide.includes(widget.name)) {
                            this._hiddenWidgets[widget.name] = widget;
                            // Keep the widget functional but hidden
                            widget.type = "tschide"; // Custom type that won't render
                            widget.computeSize = () => [0, 0];
                            widget.draw = () => { }; // Don't draw anything
                        }
                        newWidgets.push(widget);
                    }
                    this.widgets = newWidgets;

                    // Set a larger default size for the video editor
                    this.setSize([650, 480]);
                    this.setDirtyCanvas(true, true);
                });

                this.losslessCutCore = new LosslessCutCore(this);
                const interfaceContainer = this.losslessCutCore.setupInterface();

                // Add the custom widget
                this.addDOMWidget("losslesscut_ui", "customtext", interfaceContainer, {
                    getValue() { return ""; },
                    setValue() { },
                });

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

            // onExecuted fallback
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);
            };
        }
    }
});
