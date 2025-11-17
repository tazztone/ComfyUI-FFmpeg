import { app } from "/scripts/app.js";

app.registerExtension({
    name: "Jules.LosslessCut",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "LosslessCut") {
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);

                if (message.ui) {
                    if (message.ui.in_point) {
                        this.widgets.find(w => w.name === "in_point").value = message.ui.in_point[0];
                    }
                    if (message.ui.out_point) {
                        this.widgets.find(w => w.name === "out_point").value = message.ui.out_point[0];
                    }
                    if (message.ui.current_position) {
                        this.widgets.find(w => w.name === "current_position").value = message.ui.current_position[0];
                    }
                    if (message.ui.video_path_) {
                        this.widgets.find(w => w.name === "video_path_").value = message.ui.video_path_[0];
                    }
                }
            };

            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                onNodeCreated?.apply(this, arguments);

                const createButton = (name, callback) => {
                    const button = this.addWidget("button", name, name, callback.bind(this));
                    return button;
                };

                createButton("prev_kf", function () { this.triggerButton("prev_kf"); });
                createButton("next_kf", function () { this.triggerButton("next_kf"); });
                createButton("set_in", function () { this.triggerButton("set_in"); });
                createButton("set_out", function () { this.triggerButton("set_out"); });
            };

            nodeType.prototype.triggerButton = function(buttonName) {
                this.widgets.find(w => w.name === "button").value = buttonName;
                this.graph.queueExecution();
            };
        }
    },
});
