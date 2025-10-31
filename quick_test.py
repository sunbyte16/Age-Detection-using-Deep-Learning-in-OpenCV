"""
Quick test script for the age predictor
"""

import os
import glob
from age_predictor import AgePredictor
import cv2

def find_image_files():
    """Find all image files in the current directory"""
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff']
    image_files = []
    
    for ext in extensions:
        image_files.extend(glob.glob(ext))
        image_files.extend(glob.glob(ext.upper()))
    
    return image_files

def main():
    """Quick test with available images"""
    
    print("Age Predictor Quick Test")
    print("=" * 30)
    
    # Initialize predictor
    predictor = AgePredictor()
    
    if not predictor.load_models():
        print("Failed to load models!")
        return
    
    # Find available images
    image_files = find_image_files()
    
    if not image_files:
        print("No image files found in current directory.")
        print("Add some .jpg, .png, or other image files and try again.")
        return
    
    print(f"Found {len(image_files)} image file(s):")
    for i, img in enumerate(image_files, 1):
        print(f"  {i}. {img}")
    
    print("\nProcessing all images...")
    print("-" * 30)
    
    for img_file in image_files:
        print(f"\nProcessing: {img_file}")
        
        try:
            result = predictor.process_image(img_file)
            
            if result is not None:
                # Save result
                output_name = f"result_{os.path.splitext(img_file)[0]}.jpg"
                cv2.imwrite(output_name, result)
                print(f"  ✓ Result saved as: {output_name}")
            else:
                print(f"  ✗ Failed to process {img_file}")
                
        except Exception as e:
            print(f"  ✗ Error processing {img_file}: {e}")
    
    print("\n🎉 Processing complete!")
    print("\nTo test with webcam, run:")
    print("  python age_predictor.py --video 0")

if __name__ == "__main__":
    main()