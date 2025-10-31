"""
Test script to verify that all models load correctly
"""

from age_predictor import AgePredictor
import cv2
import numpy as np

def test_model_loading():
    """Test if all models can be loaded successfully"""
    print("Testing model loading...")
    
    predictor = AgePredictor()
    
    if predictor.load_models():
        print("✓ All models loaded successfully!")
        return True
    else:
        print("✗ Failed to load models")
        return False

def test_with_sample_image():
    """Test with a generated sample image"""
    print("\nTesting with sample image...")
    
    # Create a simple test image (white background with a circle representing a face)
    test_image = np.ones((400, 400, 3), dtype=np.uint8) * 255
    cv2.circle(test_image, (200, 200), 80, (200, 180, 160), -1)  # Face-like circle
    cv2.circle(test_image, (180, 180), 8, (0, 0, 0), -1)  # Left eye
    cv2.circle(test_image, (220, 180), 8, (0, 0, 0), -1)  # Right eye
    cv2.ellipse(test_image, (200, 220), (20, 10), 0, 0, 180, (0, 0, 0), 2)  # Mouth
    
    # Save test image
    cv2.imwrite("test_image.jpg", test_image)
    print("✓ Created test_image.jpg")
    
    # Test the predictor
    predictor = AgePredictor()
    
    if predictor.load_models():
        result = predictor.process_image("test_image.jpg")
        
        if result is not None:
            cv2.imwrite("test_result.jpg", result)
            print("✓ Test completed successfully!")
            print("✓ Result saved as test_result.jpg")
            return True
        else:
            print("✗ Failed to process test image")
            return False
    else:
        return False

def main():
    print("Age Predictor Model Test")
    print("=" * 30)
    
    # Test 1: Model loading
    if not test_model_loading():
        return
    
    # Test 2: Sample image processing
    if test_with_sample_image():
        print("\n🎉 All tests passed!")
        print("\nYou can now use the age predictor with your own images:")
        print("  python age_predictor.py --image your_photo.jpg")
        print("  python age_predictor.py --video 0  # for webcam")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    main()