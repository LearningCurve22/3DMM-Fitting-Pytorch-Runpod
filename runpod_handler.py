# handler-runpod.py
import os
import shutil
import subprocess
import uuid
import zipfile
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI()

# Environment/config
APP_ROOT = os.path.abspath(os.path.dirname(__file__))
BFM_DIR = os.environ.get("BFM_DIR", "/app/BFM")  # mount your runpod network volume here
RESULTS_ROOT = os.path.join(APP_ROOT, "results")
UPLOADS = os.path.join(APP_ROOT, "uploads")
os.makedirs(RESULTS_ROOT, exist_ok=True)
os.makedirs(UPLOADS, exist_ok=True)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/fit")
async def fit(file: UploadFile = File(...), res_folder: str = Form("results"), extra_args: str = Form("")):
    # Save uploaded file
    uid = str(uuid.uuid4())[:8]
    filename = f"{uid}_{file.filename}"
    in_path = os.path.join(UPLOADS, filename)
    with open(in_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Prepare result folder for this job
    job_res_folder = os.path.join(RESULTS_ROOT, f"job_{uid}")
    os.makedirs(job_res_folder, exist_ok=True)

    # Build the command.
    # We call fit_single_img.py from the repo root - adapt if your repo uses a different invocation.
    # Example: python fit_single_img.py --img_path path --res_folder results --bfm_dir /app/BFM
    cmd = [
        "python", "fit_single_img.py",
        "--img_path", in_path,
        "--res_folder", job_res_folder,
        "--bfm_dir", BFM_DIR
    ]
    # append extra args if provided (space-separated)
    if extra_args:
        cmd += extra_args.split()

    try:
        # Run the fitting process
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        stdout = proc.stdout
        stderr = proc.stderr
        retcode = proc.returncode

        # Save logs
        with open(os.path.join(job_res_folder, "run_stdout.txt"), "w") as f:
            f.write(stdout or "")
        with open(os.path.join(job_res_folder, "run_stderr.txt"), "w") as f:
            f.write(stderr or "")

        if retcode != 0:
            return JSONResponse(status_code=500, content={
                "status": "error",
                "return_code": retcode,
                "stdout_tail": stdout[-2000:],
                "stderr_tail": stderr[-2000:]
            })

        # Zip the job result folder
        zip_path = os.path.join(RESULTS_ROOT, f"{uid}_results.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(job_res_folder):
                for fn in files:
                    full = os.path.join(root, fn)
                    arcname = os.path.relpath(full, job_res_folder)
                    zf.write(full, arcname)

        return {"status": "done", "download": f"/download/{os.path.basename(zip_path)}"}

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "error": str(e)})


@app.get("/download/{zipname}")
def download(zipname: str):
    zip_path = os.path.join(RESULTS_ROOT, zipname)
    if not os.path.exists(zip_path):
        return JSONResponse(status_code=404, content={"error": "not found"})
    return FileResponse(zip_path, media_type="application/zip", filename=zipname)
