import mss
import time
import os
from PIL import Image
from datetime import datetime
from google.cloud import vision

# Define emotion likelihood values
LIKELIHOOD_VALUES = {
    "VERY_UNLIKELY": 0,
    "UNLIKELY": 0.25,
    "LIKELY": 0.75,
    "VERY_LIKELY": 1
}


class VertexEmotionAnalyzer:
    def __init__(self):
        # Initialize the Google Cloud Vision client
        self.client = vision.ImageAnnotatorClient()

    def analyze_emotions(self, image_path):
        """Send image to Vertex AI Vision API to detect faces and emotions."""
        with open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        # Vertex AI Vision API
        response = self.client.face_detection(image=image)
        faces = response.face_annotations

        # API errors
        if response.error.message:
            raise Exception(f"Error from Vertex AI Vision API: {response.error.message}")

        analysis_results = []

        for face in faces:
            emotions = {
                "joy": face.joy_likelihood.name,
                "sorrow": face.sorrow_likelihood.name,
                "anger": face.anger_likelihood.name,
                "surprise": face.surprise_likelihood.name
            }
            face_result = {
                "bounding_box": [(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices],
                "emotions": emotions
            }
            analysis_results.append(face_result)

        return analysis_results


def emotion_change_alert(previous_emotions, current_emotions):
    """Check if there is a significant change in emotions (greater than 0.5)."""
    alert_messages = []
    for emotion, current_likelihood in current_emotions.items():
        current_value = LIKELIHOOD_VALUES.get(current_likelihood, 0)
        previous_value = LIKELIHOOD_VALUES.get(previous_emotions.get(emotion, "VERY_UNLIKELY"), 0)
        if abs(current_value - previous_value) > 0.5:
            alert_messages.append(f"**Alert: {emotion} changed significantly from {previous_emotions[emotion]} to {current_likelihood}**")
    return alert_messages


def capture_and_analyze(interval=5, duration=60):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"captured_images_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)

    analyzer = VertexEmotionAnalyzer()

    with mss.mss() as sct:
        monitor = sct.monitors[1]
        width = monitor["width"]
        height = monitor["height"]
        
        top_bbox = {
            "top": 0,
            "left": 0,
            "width": width,
            "height": height // 2
        }

        bottom_bbox = {
            "top": height // 2,
            "left": 0,
            "width": width,
            "height": height // 2
        }

    print(f"Starting capture with the following settings:")
    print(f"Capturing top half: {top_bbox['width']}x{top_bbox['height']} pixels")
    print(f"Capturing bottom half: {bottom_bbox['width']}x{bottom_bbox['height']} pixels")
    print(f"Interval: {interval} seconds")
    print(f"Duration: {duration} seconds")
    print(f"Saving images to: {output_dir}")

    start_time = time.time()
    analysis_history = []
    previous_top_emotions = {}
    previous_bottom_emotions = {}

    try:
        while time.time() - start_time < duration:
            current_time = time.time()
            try:
                # Capture top half
                top_screenshot = sct.grab(top_bbox)
                top_filename = os.path.join(output_dir, f'top_screenshot_{int(current_time)}.png')
                mss.tools.to_png(top_screenshot.rgb, top_screenshot.size, output=top_filename)

                # Capture bottom half
                bottom_screenshot = sct.grab(bottom_bbox)
                bottom_filename = os.path.join(output_dir, f'bottom_screenshot_{int(current_time)}.png')
                mss.tools.to_png(bottom_screenshot.rgb, bottom_screenshot.size, output=bottom_filename)

                # Analyze emotions for top and bottom screenshots
                top_results = analyzer.analyze_emotions(top_filename)
                bottom_results = analyzer.analyze_emotions(bottom_filename)

                # Process top emotions
                if top_results:
                    top_emotions = top_results[0]['emotions']
                    print(f"\nCapture at {datetime.fromtimestamp(current_time).strftime('%H:%M:%S')}:")
                    print("You are displaying:")
                    for emotion, likelihood in top_emotions.items():
                        print(f" - {emotion}: {likelihood}")
                    
                    # Check for significant changes in top emotions
                    top_alerts = emotion_change_alert(previous_top_emotions, top_emotions)
                    for alert in top_alerts:
                        print(alert)
                    
                    previous_top_emotions = top_emotions
                else:
                    print("\nNo faces detected in the top capture.")

                # Process bottom emotions
                if bottom_results:
                    bottom_emotions = bottom_results[0]['emotions']
                    print("They are expressing:")
                    for emotion, likelihood in bottom_emotions.items():
                        print(f" - {emotion}: {likelihood}")
                    
                    # Check for significant changes in bottom emotions
                    bottom_alerts = emotion_change_alert(previous_bottom_emotions, bottom_emotions)
                    for alert in bottom_alerts:
                        print(alert)

                    previous_bottom_emotions = bottom_emotions
                else:
                    print("No faces detected in the bottom capture.")

                time.sleep(interval)

            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(f"Error during capture: {e}")
                time.sleep(interval)
                continue

    except KeyboardInterrupt:
        print("\nCapture stopped by user")

    print(f"\nAll captures have been saved to: {output_dir}")


if __name__ == "__main__":
    try:
        capture_and_analyze(interval=5, duration=60)
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
