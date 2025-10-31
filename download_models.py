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
    """Download all required model files"""
    
    # Working model URLs
    models = {
        "opencv_face_detector.pbtxt": "https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/opencv_face_detector.pbtxt",
        "opencv_face_detector_uint8.pb": "https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/opencv_face_detector_uint8.pb",
        "age_deploy.prototxt": "https://raw.githubusercontent.com/GilLevi/AgeGenderDeepLearning/master/age_deploy.prototxt",
        "age_net.caffemodel": "https://github.com/GilLevi/AgeGenderDeepLearning/raw/master/models/age_net.caffemodel"
    }
    
    print("Downloading pre-trained models for age prediction...")
    print("=" * 60)
    
    success_count = 0
    total_count = len(models)
    
    for filename, url in models.items():
        if not os.path.exists(filename):
            if download_file(url, filename):
                success_count += 1
        else:
            print(f"✓ {filename} already exists")
            success_count += 1
    
    print("=" * 60)
    print(f"Downloaded {success_count}/{total_count} model files")
    
    if success_count == total_count:
        print("\n🎉 All model files downloaded successfully!")
        print("You can now run the age predictor:")
        print("  python age_predictor.py --image your_image.jpg")
        print("  python age_predictor.py --video 0")
    else:
        print(f"\n⚠️  {total_count - success_count} files failed to download.")
        print("Please check your internet connection and try again.")

if __name__ == "__main__":
    main()