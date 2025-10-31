import cv2
import numpy as np
import argparse
import os

class AgePredictor:
    def __init__(self):
        # Age ranges for classification
        self.age_ranges = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', 
                          '(38-43)', '(48-53)', '(60-100)']
        
        # Initialize models
        self.face_net = None
        self.age_net = None
        
        # Model paths
        self.face_proto = "opencv_face_detector.pbtxt"
        self.face_model = "opencv_face_detector_uint8.pb"
        self.age_proto = "age_deploy.prototxt"
        self.age_model = "age_net.caffemodel"
        
    def load_models(self):
        """Load pre-trained models for face detection and age prediction"""
        try:
            # Load face detection model
            self.face_net = cv2.dnn.readNetFromTensorflow(self.face_model, self.face_proto)
            
            # Load age prediction model
            self.age_net = cv2.dnn.readNetFromCaffe(self.age_proto, self.age_model)
            
            print("Models loaded successfully!")
            return True
            
        except Exception as e:
            print(f"Error loading models: {e}")
            print("Please ensure all model files are in the current directory")
            return False
    
    def detect_faces(self, image, confidence_threshold=0.7):
        """Detect faces in the input image"""
        height, width = image.shape[:2]
        
        # Create blob from image
        blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), [104, 117, 123])
        
        # Set input to the face detection model
        self.face_net.setInput(blob)
        
        # Run forward pass
        detections = self.face_net.forward()
        
        faces = []
        
        # Process detections
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            
            if confidence > confidence_threshold:
                # Get bounding box coordinates
                x1 = int(detections[0, 0, i, 3] * width)
                y1 = int(detections[0, 0, i, 4] * height)
                x2 = int(detections[0, 0, i, 5] * width)
                y2 = int(detections[0, 0, i, 6] * height)
                
                faces.append([x1, y1, x2, y2])
        
        return faces
    
    def predict_age(self, face_image):
        """Predict age for a detected face"""
        # Create blob from face image
        blob = cv2.dnn.blobFromImage(face_image, 1.0, (227, 227), 
                                   (78.4263377603, 87.7689143744, 114.895847746), 
                                   swapRB=False)
        
        # Set input to age prediction model
        self.age_net.setInput(blob)
        
        # Run forward pass
        age_preds = self.age_net.forward()
        
        # Get predicted age range
        age_index = age_preds[0].argmax()
        predicted_age = self.age_ranges[age_index]
        confidence = age_preds[0][age_index]
        
        return predicted_age, confidence
    
    def process_image(self, image_path):
        """Process a single image for age prediction"""
        # Read image
        image = cv2.imread(image_path)
        
        if image is None:
            print(f"Error: Could not load image from {image_path}")
            return None
        
        # Make a copy for display
        result_image = image.copy()
        
        # Detect faces
        faces = self.detect_faces(image)
        
        if not faces:
            print("No faces detected in the image")
            return result_image
        
        print(f"Detected {len(faces)} face(s)")
        
        # Process each detected face
        for i, (x1, y1, x2, y2) in enumerate(faces):
            # Extract face region
            face = image[y1:y2, x1:x2]
            
            if face.size == 0:
                continue
            
            # Predict age
            predicted_age, confidence = self.predict_age(face)
            
            # Draw bounding box
            cv2.rectangle(result_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Add age prediction text
            label = f"Age: {predicted_age}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
            
            # Draw background rectangle for text
            cv2.rectangle(result_image, (x1, y1 - label_size[1] - 10), 
                         (x1 + label_size[0], y1), (0, 255, 0), -1)
            
            # Draw text
            cv2.putText(result_image, label, (x1, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
            
            print(f"Face {i+1}: Predicted age range: {predicted_age} (confidence: {confidence:.2f})")
        
        return result_image
    
    def process_video(self, video_path=0):
        """Process video stream for real-time age prediction"""
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print("Error: Could not open video source")
            return
        
        print("Press 'q' to quit")
        
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Detect faces
            faces = self.detect_faces(frame)
            
            # Process each detected face
            for x1, y1, x2, y2 in faces:
                # Extract face region
                face = frame[y1:y2, x1:x2]
                
                if face.size == 0:
                    continue
                
                # Predict age
                predicted_age, confidence = self.predict_age(face)
                
                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Add age prediction text
                label = f"Age: {predicted_age}"
                cv2.putText(frame, label, (x1, y1 - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            # Display frame
            cv2.imshow('Age Prediction', frame)
            
            # Break on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser(description='Age Prediction using OpenCV')
    parser.add_argument('--image', type=str, help='Path to input image')
    parser.add_argument('--video', type=str, help='Path to input video (use 0 for webcam)')
    parser.add_argument('--output', type=str, help='Path to save output image')
    
    args = parser.parse_args()
    
    # Initialize age predictor
    predictor = AgePredictor()
    
    # Load models
    if not predictor.load_models():
        return
    
    if args.image:
        # Process single image
        result = predictor.process_image(args.image)
        
        if result is not None:
            # Display result
            cv2.imshow('Age Prediction Result', result)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            # Save output if specified
            if args.output:
                cv2.imwrite(args.output, result)
                print(f"Result saved to {args.output}")
    
    elif args.video is not None:
        # Process video
        video_source = 0 if args.video == '0' else args.video
        predictor.process_video(video_source)
    
    else:
        print("Please specify either --image or --video argument")
        print("Example usage:")
        print("  python age_predictor.py --image path/to/image.jpg")
        print("  python age_predictor.py --video 0  # for webcam")
        print("  python age_predictor.py --video path/to/video.mp4")

if __name__ == "__main__":
    main()