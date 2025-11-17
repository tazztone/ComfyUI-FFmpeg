import os
import subprocess
import folder_paths
from ..func import set_file_name,video_type

current_path = os.path.abspath(__file__)
font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.normpath(__file__))), 'fonts')
folder_paths.folder_names_and_paths["fonts"] = ([font_dir], {'.ttf'})

class AddTextWatermark:
    """A node to add a text watermark to a video.

    This node overlays text onto a video at a specified position, with a
    customizable font, size, and color.
    """
 
    # 初始化方法
    def __init__(self): 
        pass 
    
    @classmethod
    def INPUT_TYPES(s):
        """Specifies the input types for the node.

        Returns:
            dict: A dictionary containing the input types.
        """
        return {
            "required": { 
                "video_path": ("STRING", {
                    "default":"C:/Users/Desktop/video.mp4",
                    "tooltip": "Path to the video file to add the text watermark to."
                }),
                "output_path": ("STRING", {
                    "default":"C:/Users/Desktop/output/",
                    "tooltip": "Path to the directory where the output video will be saved."
                }),
                'font_file': (["default"] + folder_paths.get_filename_list("fonts"), {
                    "tooltip": "Font file to use for the text watermark. 'default' uses FFmpeg's default font."
                }),
                'font_size': ("INT", {
                    "default": 15, "min": 1, "max": 1000, "step": 1,
                    "tooltip": "Font size of the text watermark in points."
                }),
                'font_color': ("STRING", {
                    "default": "#FFFFFF",
                    "tooltip": "Color of the text watermark. Can be a color name (e.g., 'white') or a hex code (e.g., '#FFFFFF')."
                }),
                "text": ("STRING", {
                    "default": "Watermark",
                    "tooltip": "The text to display as the watermark."
                }),
                "position_x":  ("INT", {
                    "default": 10, "step": 1,
                    "tooltip": "The x-coordinate of the text watermark's position (from the left edge)."
                }),
                "position_y":  ("INT", {
                    "default": 10, "step": 1,
                    "tooltip": "The y-coordinate of the text watermark's position (from the top edge)."
                }),
            },
        }

    RETURN_TYPES = ("STRING","STRING",)
    RETURN_NAMES = ("video_path","output_path",)
    FUNCTION = "add_text_watermark" 
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg" 

    def add_text_watermark(self,video_path,output_path,font_file,font_size,font_color,text,position_x,position_y):
        """Adds a text watermark to a video.

        This method uses FFmpeg to draw text on a video.

        Args:
            video_path (str): The path to the input video file.
            output_path (str): The directory to save the output video file.
            font_file (str): The name of the font file to use.
            font_size (int): The font size.
            font_color (str): The font color.
            text (str): The text to write on the video.
            position_x (int): The x-coordinate of the text.
            position_y (int): The y-coordinate of the text.

        Returns:
            tuple: A tuple containing the input video path and the output
                   video path.
        """
        try:
            video_path = os.path.abspath(video_path).strip()
            output_path = os.path.abspath(output_path).strip()
             # 视频不存在
            if not video_path.lower().endswith(video_type()):
                raise ValueError("video_path："+video_path+"不是视频文件（video_path:"+video_path+" is not a video file）")
            
            if not os.path.exists(video_path):
                raise ValueError("video_path："+video_path+"不存在（video_path:"+video_path+" does not exist）")
            
            #判断output_path是否是一个目录
            if not os.path.isdir(output_path):
                raise ValueError("output_path："+output_path+"不是目录（output_path:"+output_path+" is not a directory）")
            
            file_name = set_file_name(video_path)
            output_path = os.path.join(output_path, file_name)
            
            # 替换为双斜杠
            font_path = os.path.join(font_dir, font_file).replace("\\", "/").replace(":", "\\:")
            # 构建命令 C\\:/Windows/Fonts/simhei.ttf   fontfile='J\\:/Comfyui-for-OOTDiffusion/ComfyUI/custom_nodes/ComfyUI-FFmpeg/fonts/Alibaba-PuHuiTi-Heavy.ttf
            if font_file == "default":
                cmd = [
                    'ffmpeg',
                    '-i', video_path,
                    '-vf', f"drawtext=text='{text}':x={position_x}:y={position_y}:fontsize={font_size}:fontcolor={font_color}",
                    output_path,
                ]
            else:
                cmd = [
                    'ffmpeg',
                    '-i', video_path,
                    '-vf', f"drawtext=text='{text}':x={position_x}:y={position_y}:fontfile='{font_path}':fontsize={font_size}:fontcolor={font_color}",
                    output_path,
                ]
            result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            # 检查返回码
            if result.returncode != 0:
                # 如果有错误，输出错误信息
                 print(f"Error: {result.stderr.decode('utf-8')}")
                 raise ValueError(f"Error: {result.stderr.decode('utf-8')}")
            else:
                # 输出标准输出信息
                print(result.stdout)
        except Exception as e:
            raise ValueError(e)
        
        return (video_path,output_path)