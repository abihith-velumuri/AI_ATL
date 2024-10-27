import mss
import time
from PIL import Image
import os
import cv2
import numpy as np
from datetime import datetime
from google.cloud import vision

class VertexEmotionAnalyzer:
    def __init__(self):
        # Initialize the Google Cloud Vision client
        self.client = vision.ImageAnnotatorClient()

    def analyze_emotions(self, image_path):
        """Send image to Vertex AI Vision API to detect faces and emotions."""
        with open(image_path, 'rb') as image_file:
            content = image_file.read()
        
        image = vision.Image(content=content)

        #  Vertex AI Vision API
        response = self.client.face_detection(image=image)
        faces = response.face_annotations
        
        #  API errors
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
            print("joy:")
            print( face.joy_likelihood.name)
            print("sorrow::")
            print( face.sorrow_likelihood.name)
            print("anger:")
            print( face.anger_likelihood.name)
            print("surprise:")
            print( face.surprise_likelihood.name)
            print()
            face_result = {
                "bounding_box": [(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices],
                "emotions": emotions
            }
            analysis_results.append(face_result)

        return analysis_results


def capture_and_analyze(interval=5, duration=60):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"captured_images_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)

    analyzer = VertexEmotionAnalyzer()

    with mss.mss() as sct:
        monitor = sct.monitors[1]  
        bbox = {
            "top": 0,
            "left": 0,
            "width": monitor["width"],
            "height": monitor["height"]
        }

    print(f"Starting capture with the following settings:")
    print(f"Capturing entire screen: {bbox['width']}x{bbox['height']} pixels")
    print(f"Interval: {interval} seconds")
    print(f"Duration: {duration} seconds")
    print(f"Saving images to: {output_dir}")

    start_time = time.time()
    analysis_history = []

    try:
        with mss.mss() as sct:
            while time.time() - start_time < duration:
                current_time = time.time()
                try:
                    screenshot = sct.grab(monitor)
                    filename = os.path.join(output_dir, f'screenshot_{int(current_time)}.png')
                    mss.tools.to_png(screenshot.rgb, screenshot.size, output=filename)

                    results = analyzer.analyze_emotions(filename)

                    if results:
                        
                        smiling_faces = sum(1 for face in results if face['emotions']['joy'] == 'VERY_LIKELY')
                        total_faces = len(results)

                        print(f"\nCapture at {datetime.fromtimestamp(current_time).strftime('%H:%M:%S')}:")
                        print(f"Detected {total_faces} faces, {smiling_faces} smiling")

                        analysis_history.append({
                            'timestamp': current_time,
                            'total_faces': total_faces,
                            'smiling_faces': smiling_faces
                        })
                    else:
                        print("\nNo faces detected in this capture")

                    time.sleep(interval)

                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"Error during capture: {e}")
                    time.sleep(interval)
                    continue

    except KeyboardInterrupt:
        print("\nCapture stopped by user")

    if analysis_history:
        print("\nAnalysis Summary:")
        total_captures = len(analysis_history)
        total_faces_detected = sum(record['total_faces'] for record in analysis_history)
        total_smiles_detected = sum(record['smiling_faces'] for record in analysis_history)

        print(f"\nTotal captures: {total_captures}")
        print(f"Total faces detected: {total_faces_detected}")
        print(f"Total smiles detected: {total_smiles_detected}")
        print(f"Average faces per capture: {total_faces_detected/total_captures:.1f}")
        print(f"Average smiles per capture: {total_smiles_detected/total_captures:.1f}")

        if total_faces_detected > 0:
            smile_percentage = (total_smiles_detected / total_faces_detected) * 100
            print(f"Smile percentage: {smile_percentage:.1f}%")

    print(f"\nAll captures have been saved to: {output_dir}")


if __name__ == "__main__":
    try:
        capture_and_analyze(interval=5, duration=60)
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
