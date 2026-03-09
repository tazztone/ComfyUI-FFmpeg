import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

// Video Preview Extension for ComfyUI-FFmpeg
app.registerExtension({
	name: "Comfy.FFmpeg.VideoPreview",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.name === "VideoPreviewV3") {
			// Add a custom widget to the node
			const onNodeCreated = nodeType.prototype.onNodeCreated;
			nodeType.prototype.onNodeCreated = function () {
				const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

				// Create video element
				const videoEl = document.createElement("video");
				videoEl.style.width = "100%";
				videoEl.style.marginTop = "10px";
				videoEl.controls = true;
				videoEl.autoplay = false;
				videoEl.loop = true;

				// Add widget
				const widget = this.addDOMWidget("Video", "video", videoEl, {
					serialize: false,
					hideOnZoom: false,
				});

				// Handle node resizing
				widget.computeSize = () => [200, 150];
				
				this.videoWidget = widget;
				this.videoEl = videoEl;

				return r;
			};

			// Handle the execution result
			const onExecuted = nodeType.prototype.onExecuted;
			nodeType.prototype.onExecuted = function (message) {
				onExecuted?.apply(this, arguments);
				
				if (message?.video) {
					const [filename, type] = message.video;
					const url = api.apiURL(`/view?filename=${encodeURIComponent(filename)}&type=${type}&t=${Date.now()}`);
					
					if (this.videoEl) {
						this.videoEl.src = url;
						this.videoEl.load();
					}
				}
			};
		}
	},
});
