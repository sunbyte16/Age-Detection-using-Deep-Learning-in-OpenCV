"""
Example usage of the Age Predictor class
This demonstrates how to use the AgePredictor programmatically
"""

from age_predictor import AgePredictor
import cv2

def example_image_processing():
    """Example of processing a single image"""
    
    # Initialize the predictor
    predictor = AgePredictor()
    
    # Load models
    if not predictor.load_models():
        print("Failed to load models. Please ensure model files are available.")
        return
    
    # Process an image
    image_path = "sample_image.jpg"  # Replace with your image path
    
    try:
        result = predictor.process_image(image_path)
        
        if result is not None:
            # Display the result
            cv2.imshow('Age Prediction', result)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            # Optionally save the result
            cv2.imwrite('result_with_age_prediction.jpg', result)
            print("Result saved as 'result_with_age_prediction.jpg'")
        
    except Exception as e:
        print(f"Error processing image: {e}")

def example_batch_processing():
    """Example of processing multiple images"""
    
    predictor = AgePredictor()
    
    if not predictor.load_models():
        return
    
    # List of images to process
    image_paths = [
        "image1.jpg",
        "image2.jpg", 
        "image3.jpg"
    ]
    
    for i, image_path in enumerate(image_paths):
        print(f"\nProcessing image {i+1}: {image_path}")
        
        try:
            result = predictor.process_image(image_path)
            
            if result is not None:
                # Save result with numbered filename
                output_path = f"result_{i+1}.jpg"
                cv2.imwrite(output_path, result)
                print(f"Result saved as {output_path}")
                
        except Exception as e:
            print(f"Error processing {image_path}: {e}")

def example_webcam_processing():
    """Example of real-time webcam processing"""
    
    predictor = AgePredictor()
    
    if not predictor.load_models():
        return
    
    print("Starting webcam age prediction...")
    print("Press 'q' to quit")
    
    # Process webcam feed
    predictor.process_video(0)  # 0 for default webcam

if __name__ == "__main__":
    print("Age Predictor Examples")
    print("=" * 30)
    
    choice = input("Choose example:\n1. Single image\n2. Batch processing\n3. Webcam\nEnter choice (1-3): ")
    
    if choice == "1":
        example_image_processing()
    elif choice == "2":
        example_batch_processing()
    elif choice == "3":
        example_webcam_processing()
    else:
        print("Invalid choice")