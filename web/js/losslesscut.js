import { app } from "/scripts/app.js";
import { LosslessCutCore } from './losslesscut_core.js';

app.registerExtension({
    name: "Comfy.LosslessCut.Enhanced",

    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "LosslessCutV3") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;

            nodeType.prototype.onNodeCreated = function () {
                onNodeCreated?.apply(this, arguments);

                const widgetsToHide = ['in_point', 'out_point', 'segments', 'export_screenshot', 'screenshot_time', 'smart_cut'];

                // Store hidden widget references
                this._hiddenWidgets = {};

                // Hide widgets logic
                requestAnimationFrame(() => {
                    const newWidgets = [];
                    for (const widget of this.widgets || []) {
                        if (widgetsToHide.includes(widget.name)) {
                            this._hiddenWidgets[widget.name] = widget;
                            widget.type = "tschide";
                            widget.computeSize = () => [0, 0];
                            widget.draw = () => { };
                        }
                        newWidgets.push(widget);
                    }
                    this.widgets = newWidgets;

                    // Set size (accounting for video player)
                    this.setSize([700, 600]);
                    this.setDirtyCanvas(true, true);
                });

                this.losslessCutCore = new LosslessCutCore(this);
                const interfaceContainer = this.losslessCutCore.setupInterface();

                // Add the custom widget
                this.addDOMWidget("losslesscut_ui", "customtext", interfaceContainer, {
                    getValue() { return ""; },
                    setValue() { },
                });

                // Hook up video widget to fetch metadata
                const videoWidget = this.widgets.find(w => w.name === "video");
                if (videoWidget) {
                    const originalCallback = videoWidget.callback;
                    videoWidget.callback = (value) => {
                        originalCallback?.(value);
                        this.losslessCutCore.nodeIntegration.fetchMetadata(value);
                    };

                    // Initial load if value exists
                    if (videoWidget.value) {
                        this.losslessCutCore.nodeIntegration.fetchMetadata(videoWidget.value);
                    }
                }
            };
        }
    }
});
