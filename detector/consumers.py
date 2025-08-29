import json
import cv2
import base64
import supervision as sv
from ultralytics import YOLO
from channels.generic.websocket import AsyncWebsocketConsumer
import threading
import asyncio
import time

# --- Load the model once when the server starts ---
try:
    model = YOLO('detector/best.pt')
    print("YOLO model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
# ---------------------------------------------------

def process_video(consumer):
    """
    This function runs in a separate thread and handles the video processing.
    """
    if model is None:
        print("Model not loaded, cannot process video.")
        return

    video_path = 'detector/pothole_video.mp4'
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file at {video_path}")
        return

    box_annotator = sv.RoundBoxAnnotator(thickness=2)
    label_annotator = sv.LabelAnnotator(text_thickness=1, text_scale=0.5)

    while not consumer.stop_thread:
        ret, frame = cap.read()
        if not ret:
            print("Video ended, looping...")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # --- THE FIX: Resize the frame to a smaller, web-friendly size ---
        # This is the most important line to solve the connection issue.
        frame = cv2.resize(frame, (640, 360))

        # Run YOLOv8 inference on the resized frame
        result = model(frame, agnostic_nms=True)[0]
        detections = sv.Detections.from_ultralytics(result)
        pothole_count = len(detections)

        # Prepare labels for annotation
        labels = [
            f"{model.model.names[class_id]} {confidence:0.2f}"
            for confidence, class_id in zip(detections.confidence, detections.class_id)
        ]

        # Annotate the resized frame
        annotated_frame = frame.copy()
        annotated_frame = box_annotator.annotate(scene=annotated_frame, detections=detections)
        annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)

        # Encode the final frame to send over WebSocket
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')

        payload = {
            'image': jpg_as_text,
            'pothole_count': pothole_count
        }

        # Schedule the sending of the frame in the main event loop
        asyncio.run_coroutine_threadsafe(
            consumer.send_frame(payload),
            consumer.loop
        )
        
        # Control the frame rate
        time.sleep(1/24)

    cap.release()
    print("Video processing thread stopped.")


class PotholeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("WebSocket connected.")
        
        self.stop_thread = False
        self.loop = asyncio.get_event_loop()
        
        # Start the blocking video processing in a separate thread
        self.processing_thread = threading.Thread(target=process_video, args=(self,))
        self.processing_thread.start()

    async def disconnect(self, close_code):
        print("WebSocket disconnected.")
        self.stop_thread = True
        if self.processing_thread.is_alive():
            self.processing_thread.join()

    async def send_frame(self, frame_data):
        """
        Sends frame data to the client. This method is called from the processing thread.
        """
        try:
            await self.send(text_data=json.dumps(frame_data))
        except Exception as e:
            print(f"Error sending frame: {e}")
            self.stop_thread = True