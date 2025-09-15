import runpod
import base64
import tempfile
from fit_one import fit_image  # Your function to run 3DMM fitting

# Handler function for Runpod
def handler(event):
    try:
        # Input image comes from API call
        image_data = event["input"]["image"]

        # Save input image temporarily
        temp_in = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        temp_in.write(base64.b64decode(image_data))
        temp_in.close()

        # Run fitting → generate .obj
        output_obj_path = fit_image(temp_in.name)

        # Read the OBJ file and encode as base64
        with open(output_obj_path, "rb") as f:
            obj_data = base64.b64encode(f.read()).decode("utf-8")

        return {
            "status": "success",
            "output_obj": obj_data
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# Start Runpod serverless
runpod.serverless.start({"handler": handler})

