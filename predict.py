from cog import BasePredictor, Path
from diffusers import StableDiffusionPipeline
import torch

class Predictor(BasePredictor):
    def setup(self):
        self.pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16,
            use_safetensors=True
        ).to("cuda")

    def predict(self) -> Path:
        prompt = "a cat in a hat, cartoon style"
        image = self.pipe(prompt).images[0]
        output_path = "/tmp/output.png"
        image.save(output_path)
        return Path(output_path)