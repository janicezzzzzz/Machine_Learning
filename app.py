from flask import Flask, request, jsonify
from torchvision import transforms
from PIL import Image
import torch
import torch.nn as nn
import torchvision.models as models
import os

app = Flask(__name__)

# Load your trained model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = models.resnet18(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, 102)
model.load_state_dict(torch.load("flower_model.pth", map_location=device))
model.eval()
model.to(device)

# Label map for class index to flower name
flower_labels = {i: f"flower_{i}" for i in range(102)}
flower_labels[0] = "rose"       # example
flower_labels[1] = "sunflower"  # example

# Flower meanings
flower_meanings = {
    "rose": "Love and passion",
    "sunflower": "Adoration and loyalty",
    "tulip": "Perfect love",
    "daisy": "Innocence and purity",
    "lily": "Purity and renewal",
    # Add more as needed
}

# Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# Predict flower
def predict_flower(image):
    image = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(image)
        _, pred = torch.max(output, 1)
    class_idx = pred.item()
    flower_name = flower_labels.get(class_idx, "Unknown Flower")
    meaning = flower_meanings.get(flower_name.lower(), "Meaning not found")
    return flower_name, meaning

# Route
@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    try:
        image = Image.open(file.stream).convert("RGB")
        flower_name, meaning = predict_flower(image)
        return jsonify({"flower": flower_name, "meaning": meaning})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
