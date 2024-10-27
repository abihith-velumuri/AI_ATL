# AI_ATL

The config file needs to be stored in a folder in the same root directory as the Zoom_capture.py file, called .streamlight.
## Inspiration
Our journey began with a connection between one of our team members and a special needs teacher who opened her eyes to the daily communication challenges faced by students with autism. Through this experience, we witnessed firsthand how difficulties in reading and responding to emotional cues can create barriers to meaningful interaction and community involvement. This insight sparked our mission: to create technology that bridges the gap between speakers and their audiences, making effective communication more accessible to everyone. Once we started working on the project we realized that this application can help many people in addition to those who are on the spectrum. Many people who are simply socially awkward or nervous during a presentation can utilize this software as well. This realization helped us expand our stakeholder audience and design a general product that has a variety of different use cases.
<br />

## What it does
AwkoTalko is an innovative AI-powered plugin that integrates seamlessly with popular video conferencing platforms like Microsoft Teams, Zoom, and Google Meet. The system performs real-time emotional recognition on audience members during online presentations or meetings, providing speakers with invaluable insights about their audience's engagement and emotional responses. AwkoTalko also provides suggestions on how to navigate unpredictable and stressful social situations and helps the user come off as their best selves.
<br>
Key features include:
* Real-time emotional analysis of audience members' facial expressions and reactions
* An intuitive dashboard displaying emotional shifts and trends
* AI-driven recommendations for adjusting presentation style and content
* Integration with major video conferencing platforms
<br />

## How we built it
We used the following technologies to create our application:
1. Google Cloud Vision API for Emotional Analysis: To detect emotions, we integrated Google Cloud Vision’s face detection. We developed the VertexEmotionAnalyzer class to analyze images by sending screenshots to the API, which gives us the likelihoods of emotions like joy, sorrow, anger, and surprise. This allows us to detect and understand emotional states for both ourselves and the other person.
2. MSS library for Real-Time Screenshot Capture: Using mss, we set up interval-based screenshot capture, dividing the screen into top and bottom sections. We capture our own face in the top section and the audience’s in the bottom section. Each screenshot is analyzed to gather emotional data in real time, so we’re always aware of any shifts in our emotional expressions.
3. Streamlit for a Dynamic Web Interface: To make the experience interactive, we used Streamlit to host a web interface that displays alerts for large mood changes in the audience, helping us stay in tune with their emotional state as it evolves.
4. Algorithm to Detect Significant Emotion Change Alerts: To make the system responsive to changes, we created a computer vision-based algorithm to continuously check for major shifts in emotions by comparing the current and previous likelihood values. If the change exceeds a certain threshold, an alert is triggered, helping us to quickly identify significant mood changes.
By combining the screenshot captures, emotion analysis, and Streamlit’s live update capability, our project runs a continuous, real-time emotion-tracking system. This setup allows us to keep a close eye on emotional shifts and respond promptly to any major changes, creating an engaging, insightful experience.
<br />

## Challenges we ran into
Throughout is Hackathon, our team ran into several significant challenges that took a while to overcome:
1. Dependency Management and Virtual Environment Tracking: Installing all the necessary dependencies and managing the virtual environment was tricky. It took some time to configure everything correctly and ensure all required libraries were compatible, especially when dealing with versions and keeping the virtual environment in sync with the project needs.
2. Learning Google Cloud Platform: Since it was our first time using the Google Cloud Vision API, we had a learning curve with the setup and usage of API keys, understanding quotas, and working with image analysis responses. We spent time exploring the API documentation and learning how to integrate it seamlessly with our code.
3. Screenshot Capture Issues: Initially, our screenshot captures only included the background image, not the actual screen content we intended to analyze. We solved this through multiple rounds of testing and debugging, adjusting capture settings until we achieved the desired output.
4. Real-Time Processing and Analysis: Handling and analyzing screenshots without latency was challenging. We needed to ensure that the process ran smoothly without slowing down the overall system. Optimizing the capture and processing intervals was essential to maintain a responsive experience.
<br />

## Accomplishments that we're proud of
Despite the challenges, we've achieved several significant milestones:
* Created a working prototype that successfully integrates with major video conferencing platforms
* Developed an AI model that recognizes subtle emotional changes with high accuracy
* Built a real-time feedback system that provides actionable insights without disrupting the speaker
* Designed an intuitive interface that makes complex emotional data easily digestible
* Received positive feedback from early testing with neurodivergent users
* Learned a ton about computer vision and AI, including hands-on experience using OpenCV for image processing, Streamlit for creating intuitive UIs, and Google Cloud’s Vision API for training models to perform emotional recognition
<br />

## What we learned
This project has taught us valuable lessons about:
* The complexity of human emotion and the challenges of quantifying it
* The importance of inclusive design in technology development
* The delicate balance between providing helpful feedback and information overload
* The technical challenges of real-time video processing and analysis
* The critical role of user privacy in emotional recognition technology
<br />

## What's next for AwkoTalko
The future of AwkoTalko extends far beyond its current implementation:
<br>
#### Short-term Goals:
1. Expand platform compatibility, right now the applications functions by taking continuous screenshots, but we want it to be a feature in many different platforms such as google meet, zoom, and webex
2. Enhance emotion recognition accuracy, we a using vision API but it gives us limited emotions to choose from, we would like to build a model that recognizes different facial emotions
3. Incorporate audio, audio is an important part of a conversation and voice inflections and patterns can also give hints as to how someone is feeling
4. Develop more sophisticated feedback algorithms so that users can give us information on how helpful our model is
5. Allow for contextualization, many conversations are different depending on how close you are to someone on the situation in which you are talking to them, we want to add a context option to our app so that our AI model can make more informed predictions
<br />

<br>
#### Long-term Vision:
1. Create specialized versions for different use cases:
   - Educational environments
   - Corporate training
   - Public speaking coaching
   - Therapy and counseling sessions
2. Develop additional features:
   - Voice tone analysis
   - Body language recognition
   - Custom feedback profiles
   - Historical performance tracking
   - Personalized improvement recommendations
3. Build a community:
   - Create a platform for users to share experiences
   - Develop best practices for different speaking scenarios
   - Establish partnerships with educational institutions and corporate training programs
<br />

<br>
Our ultimate goal is to make AwkoTalko a comprehensive communication enhancement tool that helps people of all backgrounds become more effective and confident speakers. By focusing initially on supporting neurodivergent individuals, we're building a foundation for technology that can benefit everyone who wants to improve their communication skills.
<br />
