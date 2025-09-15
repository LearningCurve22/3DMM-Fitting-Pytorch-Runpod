import runpod
import requests
import subprocess
import uuid
import os

MORPHABLE_MODEL = "/workspace/volume/01_MorphableModel.mat"
EXP_PCA = "/workspace/volume/Exp_Pca.bin"

def handler(event):
    image_url = event["input"]["image_url"]
    img_name = f"input_{uuid.uuid4().hex}.jpg"
    output_name = f"output_{uuid.uuid4().hex}.obj"

    # Download image
    img_path = os.path.join("/workspace", img_name)
    with open(img_path, "wb") as f:
        f.write(requests.get(image_url).content)

    # Run fitting
    subprocess.run([
        "python", "fit_one.py",
        "--image", img_path,
        "--morphable", MORPHABLE_MODEL,
        "--exp", EXP_PCA,
        "--output", output_name
    ])

    return {"result": output_name}

runpod.serverless.start({"handler": handler})
