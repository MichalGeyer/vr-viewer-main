import os
import shutil

# Path to your local .js files
STEREO_JS_SOURCE = 'example/stereo.js'        # image-based version
STEREO_JS_SOURCE_AR2 = 'example_ar2/stereo.js'  # maybe a second variant

# Where the final viewer folders are saved
SAVE_PATH = 'viewers_images'

# URL base for your SBS images
IMAGE_PAIRS_PATH = "https://michalgeyer.github.io/vr-viewer-files-webm/pairs_for_shir/"
# Local base path for your images
IMAGES_LOCAL_PATH = '../vr-viewer-files-webm/pairs_for_shir/'

# Updated HTML template for images (see the snippet above)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>Stereo Image Viewer</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <link type="text/css" rel="stylesheet" href="../../css/main.css">
    <script type="importmap">
        {{
          "imports": {{
            "three": "https://cdn.jsdelivr.net/npm/three@0.166.1/build/three.module.js",
            "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.166.1/examples/jsm/"
          }}
        }}
    </script>
</head>
<body>
    <div id="container" 
         style="position: absolute; top: 50%; left: 50%; 
                transform: translate(-50%, -50%); display: flex; 
                justify-content: center; align-items: center; width: auto; height: auto;">
    </div>
    
    <!-- Hidden SBS image -->
    <img id="stereoImage" 
         src="{image_path}" 
         alt="SBS stereo image" 
         style="display:none" />

    <script type="module" src="stereo.js"></script>
</body>
</html>
"""

def create_html(prompt_name: str, result: str) -> str:
    """
    Generate the HTML content for a given prompt and result.
    For example, 'result' can be 'ours' or 'depth_c' or 'comparison_spatial', etc.
    This will construct the final SBS image URL.
    """
    # e.g. for 'spatial_compare', we might call the file 'comparison_spatial.jpg'
    # Adjust naming as needed:
    image_filename = f"{result}.png"
    
    # Full URL path to the SBS image
    image_path = f"{IMAGE_PAIRS_PATH}/{prompt_name}/spatial_comparison/{image_filename}"
    
    return HTML_TEMPLATE.format(image_path=image_path)

def main():
    # For example: 'temporal_compare', 'spatial_compare', or 'seperate'
    VIEWER_TYPE = 'spatial_compare'
    assert VIEWER_TYPE in ['seperate', 'temporal_compare', 'spatial_compare'], "Invalid viewer type"
    
    # Go through each folder under the local images path
    for prompt in os.listdir(IMAGES_LOCAL_PATH):
        # Skip hidden/system folders
        if prompt.startswith('.'):
            continue
        
        # You mentioned focusing on 'kitchen' in your example
        if not 'kitchen' in prompt:
            continue

        print(prompt)

        if VIEWER_TYPE == 'seperate':
            # Just an example — each result in a separate folder
            ours_folder = os.path.join(SAVE_PATH, f"{prompt}_ours")
            warp_inpaint_folder = os.path.join(SAVE_PATH, f"{prompt}_warp_inpaint")
            
            os.makedirs(ours_folder, exist_ok=True)
            os.makedirs(warp_inpaint_folder, exist_ok=True)
            
            # Create 2 separate HTML viewers
            ours_html = create_html(prompt, "ours")
            warp_inpaint_html = create_html(prompt, "warp_inpaint")
            
            with open(os.path.join(ours_folder, "index.html"), "w", encoding="utf-8") as f:
                f.write(ours_html)
            with open(os.path.join(warp_inpaint_folder, "index.html"), "w", encoding="utf-8") as f:
                f.write(warp_inpaint_html)
            
            # Copy the same stereo.js to each folder
            shutil.copy2(STEREO_JS_SOURCE, ours_folder)
            shutil.copy2(STEREO_JS_SOURCE, warp_inpaint_folder)
            
            print(f"Created HTML for prompt: {prompt}")

        else:
            # 'temporal_compare' or 'spatial_compare'
            filename = 'comparison_temporal' if VIEWER_TYPE == 'temporal_compare' else 'comparison_spatial'
            
            # Create a folder named <prompt>_comparison_temporal or <prompt>_comparison_spatial
            prompt_folder = os.path.join(SAVE_PATH, f"{prompt}_{filename}")
            os.makedirs(prompt_folder, exist_ok=True)

            # Generate an HTML that references an SBS image named 'comparison_temporal.jpg'
            # or 'comparison_spatial.jpg' under the prompt's folder
            html = create_html(prompt, filename)
            
            with open(os.path.join(prompt_folder, "index.html"), "w", encoding="utf-8") as f:
                f.write(html)
            
            # Copy the correct JS file
            if VIEWER_TYPE == 'temporal_compare':
                shutil.copy2(STEREO_JS_SOURCE, prompt_folder)
            else:
                shutil.copy2(STEREO_JS_SOURCE_AR2, prompt_folder)
            
            print(f"Created HTML for prompt: {prompt}")

if __name__ == "__main__":
    main()
