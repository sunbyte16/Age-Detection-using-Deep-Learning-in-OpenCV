import urllib.request
import os
import sys

def download_file(url, filename):
    """Download file from URL with progress"""
    print(f"Downloading {filename}...")
    try:
        def progress_hook(block_num, block_size, total_size):
            downloaded = block_num * block_size
            if total_size > 0:
                percent = min(100, (downloaded * 100) // total_size)
                sys.stdout.write(f"\r  Progress: {percent}% ({downloaded}/{total_size} bytes)")
                sys.stdout.flush()
        
        urllib.request.urlretrieve(url, filename, progress_hook)
        print(f"\n✓ {filename} downloaded successfully")
        return True
    except Exception as e:
        print(f"\n✗ Error downloading {filename}: {e}")
        return False

def main():
    """Download missing model files from alternative sources"""
    
    # Alternative URLs for missing files
    missing_models = {
        "opencv_face_detector_uint8.pb": "https://github.com/spmallick/learnopencv/raw/master/AgeGender/opencv_face_detector_uint8.pb",
        "age_deploy.prototxt": "https://github.com/spmallick/learnopencv/raw/master/AgeGender/age_deploy.prototxt"
    }
    
    print("Downloading missing model files...")
    print("=" * 50)
    
    success_count = 0
    
    for filename, url in missing_models.items():
        if not os.path.exists(filename):
            if download_file(url, filename):
                success_count += 1
        else:
            print(f"✓ {filename} already exists")
            success_count += 1
    
    print("=" * 50)
    
    # Check all required files
    required_files = [
        "opencv_face_detector.pbtxt",
        "opencv_face_detector_uint8.pb", 
        "age_deploy.prototxt",
        "age_net.caffemodel"
    ]
    
    all_present = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            all_present = False
    
    if all_present:
        print("\n🎉 All model files are now available!")
        print("You can run the age predictor:")
        print("  python age_predictor.py --image your_image.jpg")
    else:
        print("\n⚠️  Some files are still missing.")

if __name__ == "__main__":
    main()