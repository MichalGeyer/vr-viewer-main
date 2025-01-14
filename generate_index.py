import os

VIEWERS_DIR = "./viewers"
OUTPUT_INDEX = "index.html"  # Where we'll write the generated HTML

HTML_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>3D Video Survey</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      background-color: #f5f5f5;
      font-family: sans-serif;
    }

    h1 {
      margin-bottom: 20px;
    }

    .button {
      background-color: #2E7D32;
      color: #fff;
      border: none;
      padding: 10px 20px;
      margin: 5px;
      font-size: 16px;
      border-radius: 8px;
      cursor: pointer;
      transition: background-color 0.2s;
    }
    .button:hover {
      background-color: #1b5e20;
    }

    .viewer-container {
      display: none;
      flex-direction: column;
      align-items: center;
    }

    iframe {
      width: 80vw;
      height: 60vh;
      border: 2px solid #ddd;
      border-radius: 8px;
      background-color: #fff;
      margin-bottom: 20px;
    }

    .nav-buttons {
      display: flex;
      gap: 20px;
    }

    .back-button {
      position: absolute;
      top: 20px;
      left: 20px;
      background-color: rgba(0, 0, 0, 0.6);
      color: white;
      padding: 10px 15px;
      font-size: 14px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      transition: background-color 0.3s;
    }

    .back-button:hover {
      background-color: rgba(255, 255, 255, 0.8);
      color: black;
    }
  </style>
</head>
<body>
  <h1>3D Video Survey</h1>
  <p class="instructions">
    Click <strong>Enter VR</strong> for each video to view two videos side by side.<br>
    The videos will play twice and then pause on a frame.<br>
    Your task is to determine in which video <strong> has a more realistic 3D effect</strong>.
    Pay attention to the 3D effect of reflections and of objects behind transperent surfaces.<br> 
    Start with the test viewer, to get familiar with the task and make sure you understand it.<br>
    Thank you for your input!
  </p>
  <button id="testViewerButton" class="button">Test Viewer</button>
  <button id="startButton" class="button">Main Viewer</button>

  <div class="viewer-container" id="viewerContainer">
    <div id="videoIdTitle" class="video-id-title"></div>
    <iframe id="viewerFrame" src="" frameborder="0"></iframe>
    <div class="nav-buttons">
      <button id="prevButton" class="button">&larr; Prev</button>
      <button id="nextButton" class="button">Next &rarr;</button>
      <button id="backButton" class="back-button">Back</button>
    </div>
  </div>

  <script>
    // The main viewer array:
    const viewerUrls = [
"""

HTML_MIDDLE = """    ];

    // A simple utility function to shuffle any given array in place.
    function shuffleArray(array) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
      return array;
    }

    // Shuffle the main viewer URLs on page load
    shuffleArray(viewerUrls);

    // caption_to_id object generated below
    const caption_to_id = {
"""

HTML_MIDDLE2 = """    };

    // Test viewer URLs (not shuffled by default)
    const testViewerUrls = [
      "viewers_test/flickr_comparison_spatial/index.html",
      "viewers_test/TEST-VIDEO-A_close-up_view_of_a_laptop_displaying_audio_software_comparison_spatial/index.html"
    ];

    let currentIndex = 0;
    let isTestViewer = false;

    const startButton = document.getElementById('startButton');
    const testViewerButton = document.getElementById('testViewerButton');
    const viewerContainer = document.getElementById('viewerContainer');
    const viewerFrame = document.getElementById('viewerFrame');
    const prevButton = document.getElementById('prevButton');
    const nextButton = document.getElementById('nextButton');
    const backButton = document.getElementById('backButton');
    const videoIdTitle = document.getElementById('videoIdTitle');

    // Show the viewer iframe at the specified index
    function showViewer(index, isTest = false) {
      const urls = isTest ? testViewerUrls : viewerUrls;
      viewerFrame.src = urls[index];
      // Pull the last subfolder name from the path (e.g. "A_glass_door..." from ".../A_glass_door.../index.html")
      const folderName = urls[index].split('/').slice(-2, -1)[0];
      // Use that folderName to get the ID from caption_to_id
      const videoId = caption_to_id[folderName] !== undefined ? caption_to_id[folderName] : folderName;
      videoIdTitle.textContent = 'VIDEO ID: ' + videoId;
    }

    // Show the main instructions/home screen
    function showMainScreen() {
      viewerContainer.style.display = 'none';
      viewerFrame.src = '';
      document.querySelector('h1').style.display = 'block';
      document.querySelector('.instructions').style.display = 'block';
      startButton.style.display = 'block';
      testViewerButton.style.display = 'block';
    }

    startButton.addEventListener('click', () => {
      isTestViewer = false;
      currentIndex = 0;
      showViewer(currentIndex);
      document.querySelector('h1').style.display = 'none';
      document.querySelector('.instructions').style.display = 'none';
      startButton.style.display = 'none';
      testViewerButton.style.display = 'none';
      viewerContainer.style.display = 'flex';
    });

    testViewerButton.addEventListener('click', () => {
      isTestViewer = true;
      currentIndex = 0;
      showViewer(currentIndex, true);
      document.querySelector('h1').style.display = 'none';
      document.querySelector('.instructions').style.display = 'none';
      startButton.style.display = 'none';
      testViewerButton.style.display = 'none';
      viewerContainer.style.display = 'flex';
    });

    backButton.addEventListener('click', () => {
      showMainScreen();
    });

    prevButton.addEventListener('click', () => {
      if (currentIndex > 0) {
        currentIndex--;
        showViewer(currentIndex, isTestViewer);
      }
    });

    nextButton.addEventListener('click', () => {
      const urls = isTestViewer ? testViewerUrls : viewerUrls;
      if (currentIndex < urls.length - 1) {
        currentIndex++;
        showViewer(currentIndex, isTestViewer);
      }
    });
  </script>
</body>
</html>
"""

def parse_folder_name(folder_name: str):
    """Extracts the prompt and the type based on folder name patterns."""
    if folder_name.endswith("_comparison_spatial"):
        prompt = folder_name[:-(len("_comparison_spatial"))]
        label = "comparison_spatial"
    elif folder_name.endswith("_comparison_temporal"):
        prompt = folder_name[:-(len("_comparison_temporal"))]
        label = "comparison_temporal"
    else:
        prompt = folder_name
        label = "unknown"
    return prompt, label

def main():
    # Gather all subfolders in ./viewers
    viewer_folders = []
    for item in os.listdir(VIEWERS_DIR):
        # Skip certain items you don't want in the list
        if item.endswith('depthc') or '.DS' in item or item == 'images':
            continue
        full_path = os.path.join(VIEWERS_DIR, item)
        if os.path.isdir(full_path):
            viewer_folders.append(item)

    # Sort viewer folders so insertion into both arrays is consistent
    viewer_folders_sorted = sorted(viewer_folders)

    # 1) Generate lines for viewerUrls
    viewer_urls_lines = []
    for folder in viewer_folders_sorted:
        index_path = os.path.join("viewers", folder, "index.html").replace("\\", "/")
        viewer_urls_lines.append(f'      "{index_path}",')

    # 2) Generate the caption_to_id object
    caption_to_id_lines = []
    for i, folder in enumerate(viewer_folders_sorted):
        caption_to_id_lines.append(f'      "{folder}": {i},')

    # Combine final HTML
    final_html = []
    final_html.append(HTML_HEAD)                          # Up to "const viewerUrls = ["
    final_html.append("\n".join(viewer_urls_lines))       # The <script> array for viewerUrls
    final_html.append(HTML_MIDDLE)                        # Start of shuffle + caption_to_id
    final_html.append("\n".join(caption_to_id_lines))     # fill in the caption_to_id object
    final_html.append(HTML_MIDDLE2)                       # The rest of the script

    # Write out the HTML file
    with open(OUTPUT_INDEX, "w", encoding="utf-8") as f:
        f.write("".join(final_html))

    print(f"Generated {OUTPUT_INDEX} with {len(viewer_folders_sorted)} entries.")

if __name__ == "__main__":
    main()
