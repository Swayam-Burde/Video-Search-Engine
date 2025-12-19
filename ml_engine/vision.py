import torch
import clip
from PIL import Image

class VideoVision:
    def __init__(self):
        print("Loading CLIP model...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device, jit=False)

    def get_image_embedding(self, image_path):
        image = self.preprocess(Image.open(image_path)).unsqueeze(0).to(self.device)
        with torch.no_grad():
            image_features = self.model.encode_image(image)
        return image_features.cpu().numpy().tolist()[0]

    def get_text_embedding(self, text_query):
        text = clip.tokenize([text_query]).to(self.device)
        with torch.no_grad():
            text_features = self.model.encode_text(text)
        return text_features.cpu().numpy().tolist()[0]

if __name__ == "__main__":
    print("Vision module is ready.")