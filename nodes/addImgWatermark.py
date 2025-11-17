import os
import subprocess
from ..func import get_image_size,set_file_name,video_type


class AddImgWatermark:
    """A node to add an image watermark to a video.

    This node overlays an image onto a video at a specified position and size.
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
                    "tooltip": "Path to the video file to add the watermark to."
                }),
                "output_path": ("STRING", {
                    "default":"C:/Users/Desktop/output/",
                    "tooltip": "Path to the directory where the output video will be saved."
                }),
                "watermark_image": ("STRING", {
                    "default":"C:/Users/Desktop/logo.png",
                    "tooltip": "Path to the image file to use as a watermark."
                }),
                "watermark_img_width":  ("INT", {
                    "default": 100,
                    "min": 1,
                    "step": 1,
                    "tooltip": "Width of the watermark image in pixels. The height will be scaled proportionally."
                }),
                "position_x":  ("INT", {
                    "default": 10,
                    "step": 1,
                    "tooltip": "The x-coordinate of the watermark's position (from the left edge)."
                }),
                "position_y":  ("INT", {
                    "default": 10,
                    "step": 1,
                    "tooltip": "The y-coordinate of the watermark's position (from the top edge)."
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_complete_path",)
    FUNCTION = "add_img_watermark" 
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg" 

    def add_img_watermark(self,video_path,output_path,watermark_image,watermark_img_width,position_x,position_y):
        """Adds an image watermark to a video.

        This method uses FFmpeg to overlay an image onto a video.

        Args:
            video_path (str): The path to the input video file.
            output_path (str): The directory to save the output video file.
            watermark_image (str): The path to the watermark image file.
            watermark_img_width (int): The width of the watermark image.
            position_x (int): The x-coordinate of the watermark.
            position_y (int): The y-coordinate of the watermark.

        Returns:
            tuple: A tuple containing the path to the output video file.
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
            
            # 文件不是图片
            if not watermark_image.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                raise ValueError("watermark_image不是图片文件（watermark file is not a image file）")
            
            if not os.path.exists(watermark_image):
                raise ValueError("watermark_image："+watermark_image+"不存在（watermark_image :"+watermark_image+" does not exist）")
            
            file_name = set_file_name(video_path)
            output_path = os.path.join(output_path, file_name)
            width,height = get_image_size(watermark_image)
            watermark_img_height = int(height * watermark_img_width / width)  # 按比例计算新高度
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-i', watermark_image,
                '-filter_complex',f"[1:v]scale={watermark_img_width}:{watermark_img_height}[wm];[0:v][wm]overlay=x={position_x}:y={position_y}:format=auto",
                output_path,
            ]
            result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            #os.remove(image_save_path) # 删除临时水印图片
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
        return (output_path,)