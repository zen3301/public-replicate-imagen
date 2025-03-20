from cog import BasePredictor, Input, Path
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
import torch
from PIL import Image
import numpy as np
from insightface.app import FaceAnalysis
import os
import requests

class Predictor(BasePredictor):
    def setup(self):
        ip_adapter_path = "ip-adapter-faceid-plusv2_sd15.bin"
        if not os.path.exists(ip_adapter_path):
            url = "https://drive.google.com/uc?export=download&id=1XjDS2mGcsRX63_XiaOqV6EFpOi8t3MMy"
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(ip_adapter_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

        self.controlnet = ControlNetModel.from_pretrained("lllyasviel/control_v11p_sd15_openpose").to("cuda")
        self.pipe = StableDiffusionControlNetPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            controlnet=self.controlnet
        ).to("cuda")
        self.pipe.load_ip_adapter(ip_adapter_path)
        self.app = FaceAnalysis(providers=['CUDAExecutionProvider'])
        self.app.prepare(ctx_id=0, det_size=(640, 640))

    def predict(
        self,
        prompt: str = Input(description="Text prompt", default="a cat in a hat, cartoon style"),
        pose_image: Path = Input(description="Pose image (PNG)"),
        face_image: Path = Input(description="Face image (PNG)")
    ) -> Path:
        pose_img = Image.open(pose_image).convert("RGB")
        face_img = Image.open(face_image).convert("RGB")
        faces = self.app.get(np.array(face_img))
        if not faces:
            raise ValueError("No face detected in face.png!")
        face_embedding = faces[0].normed_embedding
        output = self.pipe(
            prompt,
            image=pose_img,
            ip_adapter_image=face_img
        ).images[0]
        output_path = "test_ip_full.png"
        output.save(output_path)
        return Path(output_path)