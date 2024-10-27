import mss
import time
import os
from PIL import Image
from datetime import datetime
from google.cloud import vision
import streamlit as st
import pandas as pd
import random

# Initialize session state
if 'p_prev_emotions' not in st.session_state:
    st.session_state.p_prev_emotions = [" ", " ", " ", " "]
if 'p_curr_emotions' not in st.session_state:
    st.session_state.p_curr_emotions = ["High", "Medium", "Medium", "Low"]
if 'current_alert' not in st.session_state:
    st.session_state.current_alert = "You're doing great 😊"

advice_for_emotions = [
    # joy --> sorrow
    "When you notice this shift, slow your pace significantly and lower your vocal tone. Focus on empathy in your delivery and avoid trying to immediately 'fix' or lighten the mood.",
    "Consider sharing a relevant personal experience that shows vulnerability. This helps validate the audience's emotional response while maintaining authenticity.",
    "Watch your body language - maintain open posture but reduce energetic gestures that might seem disconnected from the somber mood.",
    # joy --> anger
    "Address the shift head-on by pausing your planned content. Trying to push through will likely escalate tensions.",
    "Maintain calm, measured speech and avoid defensive body language. Your steady presence can help defuse the tension.",
    "Create immediate space for feedback - the anger often comes from feeling unheard or misunderstood.",
    # joy --> surprise
    "Take a step back in your content and provide more foundational context - surprise often indicates an information gap",
    "Use visual aids or analogies to help connect unfamiliar concepts to known ones",
    "Break down complex information into smaller, more digestible pieces rather than continuing at the same pace",
    
    # sorrow --> joy
    "Build gradually on the positive shift - avoid suddenly matching their energy as it might seem insensitive to their previous state.",
    "Incorporate more dynamic vocal variety and gradually increase your energy level",
    "Begin introducing more interactive elements to your presentation to maintain the positive momentum.",
    # sorrow --> anger
    "Ground yourself physically and emotionally - your stability is crucial when navigating this volatile transition.",
    "Focus on fact-based, clear communication while acknowledging the emotional undercurrent",
    "Create structured opportunities for feedback to prevent the anger from building without outlet",
    # sorrow --> surprise
    "Be prepared to substantiate any unexpected claims with clear evidence or examples.",
    "Use clear, logical transitions to help connect surprising information to what they already know.",
    "Watch for signs of disbelief or skepticism and be ready to provide additional supporting information.",
    
    # anger --> joy
    "Build on the positive shift by incorporating more collaborative elements into your presentation.",
    "Gradually increase the pace and energy of your delivery to match their improving mood.",
    "Use this opportunity to establish common ground that you can reference if tensions rise again.",
    # anger --> sorrow
    "Significantly reduce your talking speed and increase pause lengths.",
    "Lower both your vocal tone and volume while maintaining clear enunciation.",
    "Remove any barriers between you and the audience (like podiums or tables) to create a more intimate speaking environment.",
    # anger --> surprise
    "Use this moment of unexpected information to reset the emotional temperature of the room.",
    "Incorporate more visual elements or demonstrations to help maintain focus on new information rather than lingering anger.",
    "Be extra clear and methodical in your explanation to prevent confusion from reigniting frustration.",
    
    # surprise --> joy
    "Capitalize on the energy by introducing more dynamic elements to your presentation.",
    "Use this moment to deepen engagement through interactive components or discussion.",
    "Match their positive energy while maintaining clear structure to prevent the session from becoming too scattered.",
    # surprise --> sorrow
    "Immediately shift to a more measured, gentle delivery style.",
    "Create more physical and emotional space through longer pauses and softer vocal tones.",
    "Be prepared to deviate from your planned content to address emotional needs.",
    # surprise --> anger
    "Ground your physical presence - plant your feet and maintain steady, calm movements.",
    "Slow your rate of speech and lower your volume slightly to model the energy you want to see.",
    "Have supporting evidence readily available to address skepticism before it turns to hostility."
]

# Streamlit UI setup
st.title("🌮")
st.title("AwkoTalko")

# Create placeholders for dynamic content
alert_placeholder = st.empty()
table_placeholder = st.empty()

# Define emotion likelihood values
LIKELIHOOD_VALUES = {
    "VERY_UNLIKELY": 0,
    "UNLIKELY": 0.25,
    "LIKELY": 0.75,
    "VERY_LIKELY": 1
}

CATEGORY_MAPPING = {
    "VERY_UNLIKELY": "Low",
    "UNLIKELY": "Medium",
    "LIKELY": "Medium",
    "VERY_LIKELY": "High"
}

def update_alert(previous_emotion_for_advice, post_emotion_for_advice):
    if previous_emotion_for_advice == "joy":
        if post_emotion_for_advice == "sorrow":
            random_int = random.randint(0, 2)
        elif post_emotion_for_advice == "anger":
            random_int = random.randint(3, 5)
        else:
            random_int = random.randint(6, 8)
    elif previous_emotion_for_advice == "sorrow":
        if post_emotion_for_advice == "joy":
            random_int = random.randint(9, 11)
        elif post_emotion_for_advice == "anger":
            random_int = random.randint(12, 14)
        else:
            random_int = random.randint(15, 17)
    elif previous_emotion_for_advice == "anger":
        if post_emotion_for_advice == "joy":
            random_int = random.randint(18, 20)
        elif post_emotion_for_advice == "sorrow":
            random_int = random.randint(21, 23)
        else:
            random_int = random.randint(24, 26)
    else:  # surprise
        if post_emotion_for_advice == "joy":
            random_int = random.randint(27, 29)
        elif post_emotion_for_advice == "sorrow":
            random_int = random.randint(30, 32)
        else:
            random_int = random.randint(33, 35)
    
    st.session_state.current_alert = advice_for_emotions[random_int]

def update_ui():
    # Update alert
    alert_placeholder.markdown(f"### Alert\n{st.session_state.current_alert}")
    
    # Update table
    df = pd.DataFrame(
        [
            {"Emotion": "Joy", "Previously": st.session_state.p_prev_emotions[0], "Currently": st.session_state.p_curr_emotions[0]},
            {"Emotion": "Sorrow", "Previously": st.session_state.p_prev_emotions[1], "Currently": st.session_state.p_curr_emotions[1]},
            {"Emotion": "Anger", "Previously": st.session_state.p_prev_emotions[2], "Currently": st.session_state.p_curr_emotions[2]},
            {"Emotion": "Surprise", "Previously": st.session_state.p_prev_emotions[3], "Currently": st.session_state.p_curr_emotions[3]},
        ]
    )
    table_placeholder.dataframe(df, use_container_width=True, hide_index=True)

class VertexEmotionAnalyzer:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def analyze_emotions(self, image_path):
        with open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = self.client.face_detection(image=image)
        faces = response.face_annotations

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

    print(f"Starting capture with interval: {interval}s, duration: {duration}s")
    start_time = time.time()
    previous_top_emotions = {}
    previous_bottom_emotions = {}
    curr_emotion = "joy"  # Initialize curr_emotion

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

                # Analyze emotions
                top_results = analyzer.analyze_emotions(top_filename)
                bottom_results = analyzer.analyze_emotions(bottom_filename)

                # Process top emotions
                if top_results:
                    top_emotions = top_results[0]['emotions']
                    top_alerts = emotion_change_alert(previous_top_emotions, top_emotions)
                    for alert in top_alerts:
                        print(alert)
                    previous_top_emotions = top_emotions

                # Process bottom emotions
                if bottom_results:
                    bottom_emotions = bottom_results[0]['emotions']
                    likelihoods = []
                    for emotion, likelihood in bottom_emotions.items():
                        likelihoods.append(likelihood)
                    
                    # Update session state
                    st.session_state.p_prev_emotions = st.session_state.p_curr_emotions.copy()
                    st.session_state.p_curr_emotions = [CATEGORY_MAPPING[l] for l in likelihoods]
                    
                    prev_emotion = curr_emotion
                    curr_emotion = max(bottom_emotions, key=bottom_emotions.get)
                    
                    # Update alert and UI
                    update_alert(prev_emotion.lower(), curr_emotion.lower())
                    update_ui()
                    
                    bottom_alerts = emotion_change_alert(previous_bottom_emotions, bottom_emotions)
                    for alert in bottom_alerts:
                        print(alert)
                    
                    previous_bottom_emotions = bottom_emotions

                time.sleep(interval)

            except Exception as e:
                print(f"Error during capture: {e}")
                time.sleep(interval)
                continue

    except KeyboardInterrupt:
        print("\nCapture stopped by user")

    print(f"\nAll captures have been saved to: {output_dir}")

if __name__ == "__main__":
    try:
        update_ui()  # Initial UI render
        capture_and_analyze(interval=5, duration=60)
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
