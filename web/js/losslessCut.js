import { app } from "/scripts/app.js";

function formatTime(seconds) {
  const date = new Date(seconds * 1000);
  const hours = date.getUTCHours().toString().padStart(2, "0");
  const minutes = date.getUTCMinutes().toString().padStart(2, "0");
  const secs = date.getUTCSeconds().toString().padStart(2, "0");
  return `${hours}:${minutes}:${secs}`;
}

app.registerExtension({
  name: "Comfy.LosslessCut",
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name === "LosslessCut") {
      const onExecuted = nodeType.prototype.onExecuted;
      nodeType.prototype.onExecuted = function (message) {
        onExecuted?.apply(this, arguments);
        if (message.ui) {
          this.in_point_widget.value = message.ui.in_point;
          this.out_point_widget.value = message.ui.out_point;
          this.current_position_widget.value = message.ui.current_position;

          this.inPointDisplay.value = formatTime(this.in_point_widget.value);
          this.outPointDisplay.value = formatTime(this.out_point_widget.value);
          this.currentPositionDisplay.value = formatTime(this.current_position_widget.value);
        }
      };

      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function () {
        onNodeCreated?.apply(this, arguments);

        this.inPointDisplay = this.addWidget("text", "IN", "00:00:00", () => {}, { disabled: true });
        this.outPointDisplay = this.addWidget("text", "OUT", "00:00:00", () => {}, { disabled: true });
        this.currentPositionDisplay = this.addWidget("text", "POS", "00:00:00", () => {}, { disabled: true });

        this.action_widget = this.widgets.find(w => w.name === 'action');
        this.in_point_widget = this.widgets.find(w => w.name === 'in_point');
        this.out_point_widget = this.widgets.find(w => w.name === 'out_point');
        this.current_position_widget = this.widgets.find(w => w.name === 'current_position');

        // Hide the widgets
        this.action_widget.type = "hidden";
        this.in_point_widget.type = "hidden";
        this.out_point_widget.type = "hidden";
        this.current_position_widget.type = "hidden";


        this.addWidget("button", "<< Prev KF", null, () => this.queueAction("prev_kf"));
        this.addWidget("button", "Next KF >>", null, () => this.queueAction("next_kf"));
        this.addWidget("button", "Set IN", null, () => this.queueAction("set_in"));
        this.addWidget("button", "Set OUT", null, () => this.queueAction("set_out"));
        this.addWidget("button", "Cut", null, () => this.queueAction("cut"));
      };

      nodeType.prototype.queueAction = function (action) {
        this.action_widget.value = action;
        app.queuePrompt();
      };
    }
  },
});
