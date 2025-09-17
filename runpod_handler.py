# handler-runpod.py
import os
import subprocess
import uuid
import base64

import runpod

BFM_DIR = os.environ.get("BFM_DIR", "/runpod-volume/BFM")
RESULTS_ROOT = "/runpod-volume/results"
UPLOADS = "/app/uploads"
os.makedirs(RESULTS_ROOT, exist_ok=True)
os.makedirs(UPLOADS, exist_ok=True)

def handler(job):
    """
    job["input"] must contain:
    {
      "image_name": "face.jpg",
      "image_bytes": base64 string of the image
    }
    """
    job_input = job["input"]

    # Save uploaded image
    uid = str(uuid.uuid4())[:8]
    image_name = job_input.get("image_name", f"{uid}.jpg")
    image_path = os.path.join(UPLOADS, f"{uid}_{image_name}")

    with open(image_path, "wb") as f:
        f.write(base64.b64decode(job_input["image_bytes"]))

    # Prepare result folder
    job_res_folder = os.path.join(RESULTS_ROOT, f"job_{uid}")
    os.makedirs(job_res_folder, exist_ok=True)

    # Run fitting script
    cmd = [
        "python", "fit_single_img.py",
        "--img_path", image_path,
        "--res_folder", job_res_folder,
        "--bfm_dir", BFM_DIR
    ]

    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if proc.returncode != 0:
        return {
            "status": "error",
            "stderr": proc.stderr[-500:],
            "stdout": proc.stdout[-500:]
        }

    # Collect only .obj and *_coeffs.npy
    outputs = {}
    for fn in os.listdir(job_res_folder):
        if fn.endswith(".obj") or fn.endswith("_coeffs.npy"):
            full_path = os.path.join(job_res_folder, fn)
            with open(full_path, "rb") as f:
                outputs[fn] = base64.b64encode(f.read()).decode("utf-8")

    return {
        "status": "done",
        "files": outputs
    }

# Start RunPod serverless handler
runpod.serverless.start({"handler": handler})
