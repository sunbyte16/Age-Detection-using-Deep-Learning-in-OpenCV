"""
Download sample images for testing the age predictor
"""

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
                sys.stdout.write(f"\r  Progress: {percent}%")
                sys.stdout.flush()
        
        urllib.request.urlretrieve(url, filename, progress_hook)
        print(f"\n✓ {filename} downloaded successfully")
        return True
    except Exception as e:
        print(f"\n✗ Error downloading {filename}: {e}")
        return False

def main():
    """Download sample images for testing"""
    
    # Sample images with faces (using placeholder/demo images)
    sample_images = {
        "sample_person1.jpg": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face",
        "sample_person2.jpg": "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop&crop=face",
        "sample_person3.jpg": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop&crop=face"
    }
    
    print("Downloading sample images for age prediction testing...")
    print("=" * 60)
    
    success_count = 0
    
    for filename, url in sample_images.items():
        if not os.path.exists(filename):
            if download_file(url, filename):
                success_count += 1
        else:
            print(f"✓ {filename} already exists")
            success_count += 1
    
    print("=" * 60)
    print(f"Downloaded {success_count}/{len(sample_images)} sample images")
    
    if success_count > 0:
        print("\n🎉 Sample images ready for testing!")
        print("\nTry these commands:")
        for filename in sample_images.keys():
            if os.path.exists(filename):
                print(f"  python age_predictor.py --image {filename}")
    else:
        print("\n⚠️  No sample images available.")
        print("You can add your own image files to test with.")

if __name__ == "__main__":
    main()