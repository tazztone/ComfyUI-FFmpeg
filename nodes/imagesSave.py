import os
import torch
import gc
from concurrent.futures import ThreadPoolExecutor
from ..func import save_image,clear_memory
file_name_num_start = 0

class ImagesSave:
    """A node to save a batch of images to a specified directory.

    This node takes a tensor of images and saves each image as a separate file
    in the output directory.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        """Specifies the input types for the node.

        Returns:
            dict: A dictionary containing the input types.
        """
        return {
            "required": { 
                "images": ("IMAGE", ),
                "output_path": ("STRING", {"default":"C:/Users/Desktop/output",}),
            },
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("images_length",)
    FUNCTION = "images_save"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg/auxiliary tool"
  
    def images_save(self, images,output_path):
        """Saves a batch of images to a specified directory.

        Args:
            images (torch.Tensor): A tensor of images to save.
            output_path (str): The directory to save the images to.

        Returns:
            tuple: A tuple containing the number of images saved.
        """
        try:
            output_path = os.path.abspath(output_path).strip()
            #判断output_path是否是一个目录
            if not os.path.isdir(output_path):
                raise ValueError("output_path："+output_path+"不是目录（output_path:"+output_path+" is not a directory）")
            
            count = 0
            global file_name_num_start
            if len(os.listdir(output_path)) == 0:
                file_name_num_start = 0  # 要保证图片的名称的数字从0开始，否则合并视频时会报错
            with ThreadPoolExecutor() as executor:
                futures = []
                for image in images:
                    file_name_num_start += 1
                    futures.append(executor.submit(save_image, image, os.path.join(output_path, f"output_image_{file_name_num_start:09d}.png")))
                    count += 1
                    
                for future in futures:
                    future.result()  # 确保所有任务完成
            del images
            clear_memory()
            
            return (count,)
        except Exception as e:
            raise ValueError(e)