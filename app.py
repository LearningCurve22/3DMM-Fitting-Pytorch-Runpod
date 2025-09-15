from fastapi import FastAPI, UploadFile
import subprocess, tempfile, os

app = FastAPI()

MORPHABLE_MODEL = "/workspace/volume/01_MorphableModel.mat"
EXP_PCA = "/workspace/volume/Exp_Pca.bin"

@app.post("/fit")
async def fit_face(file: UploadFile):
    # Save uploaded image
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp_path = tmp.name
        tmp.write(await file.read())

    output_path = tmp_path.replace(".jpg", ".obj")

    # Run fitting
    subprocess.run([
        "python", "fit_one.py",
        "--image", tmp_path,
        "--morphable", MORPHABLE_MODEL,
        "--exp", EXP_PCA,
        "--output", output_path
    ])

    return {"output": output_path}
