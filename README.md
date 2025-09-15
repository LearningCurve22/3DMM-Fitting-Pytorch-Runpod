# 3DMM-Fitting-Pytorch Runpod API

This repository adapts the original [3DMM-Fitting-Pytorch](https://github.com/ascust/3DMM-Fitting-Pytorch) project to run as a **serverless API on Runpod**.  
The API accepts a single face image as input and outputs a **3D face reconstruction (.obj)** using the Basel Face Model (BFM) and expression PCA data.  

---

## 🚀 Features
- Run as a **serverless API** on [Runpod](https://runpod.io)  
- Accepts user-uploaded face images via API  
- Produces **3D face meshes (.obj)** using 3DMM fitting  
- Supports persistent volumes for model files  

---

## 📂 Project Structure
```
3DMM-Fitting-Runpod/
│── app.py                # FastAPI app (local testing)
│── runpod_handler.py     # Runpod serverless handler
│── fit_one.py            # 3DMM fitting logic (adapted)
│── core/                 # Core 3DMM utilities (from original repo)
│── util/                 # Helper functions (from original repo)
│── requirements.txt      # Python dependencies
│── Dockerfile            # Runpod container build
│── README.md             # This file
```

---

## ⚙️ Setup

### 1. Clone Repo
```bash
git clone https://github.com/YOUR-USERNAME/3DMM-Fitting-Pytorch-Runpod.git
cd 3DMM-Fitting-Pytorch-Runpod
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Model Files
Due to licensing restrictions, **model files are not included** in this repo.  
Download and place the following files into your **Runpod volume**:

- `01_MorphableModel.mat`
- `Exp_Pca.bin`

Example Runpod mount path:
```
/workspace/volume/01_MorphableModel.mat
/workspace/volume/Exp_Pca.bin
```

---

## ▶️ Run Locally (FastAPI)
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```
Then open [http://localhost:8000/docs](http://localhost:8000/docs) to test.

---

## ☁️ Run on Runpod Serverless

1. Build & push container (Runpod will do this automatically if connected to GitHub).  
2. Mount your volume with model files.  
3. Deploy as a serverless endpoint.  

---

## 📡 API Usage

### Endpoint: `/fit`
**Method:** `POST`  
**Input:** Image file (`.jpg`/`.png`)  
**Output:** `.obj` file (3D face mesh)  

Example (Python):
```python
import requests

url = "https://YOUR-RUNPOD-ENDPOINT/fit"
files = {"file": open("face.jpg", "rb")}
response = requests.post(url, files=files)

with open("output.obj", "wb") as f:
    f.write(response.content)
```

---

## ⚠️ Notes
- This repo is for **research and educational use only**.  
- The **Basel Face Model (BFM)** license forbids redistribution. You must obtain the model files yourself.  

---

## 📜 License
This repo follows the original [3DMM-Fitting-Pytorch license](https://github.com/ascust/3DMM-Fitting-Pytorch).  
Model files must be obtained separately under their own license terms.  
