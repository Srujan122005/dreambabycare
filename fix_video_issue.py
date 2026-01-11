import os
import shutil

def fix_and_add_video():
    print("Starting automatic fix and video addition...")
    
    # 1. Define paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    source_video = r"C:\Users\91890\Downloads\invideo-ai-1080 Breast or Bottle_ A Gentle 1_50 Guide 2026-01-10.mp4"
    # User asked for diaper section
    dest_folder = os.path.join(base_dir, "static", "videos", "diapering")
    dest_file = os.path.join(dest_folder, "breast_or_bottle.mp4")
    
    # 2. Copy the video
    if os.path.exists(source_video):
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        try:
            shutil.copy2(source_video, dest_file)
            print(f"✅ Video copied successfully to: {dest_file}")
            print("   (It will appear in the Diapering section as requested)")
        except Exception as e:
            print(f"❌ Failed to copy video: {e}")
    else:
        print(f"⚠️ Source video not found at: {source_video}")

    # 3. Fix the TemplateSyntaxError (Remove bad paths from files)
    # The error 'truncated \U escape' happens when a file path like 'C:\Users' is pasted into code
    print("\nScanning for syntax errors (pasted file paths)...")
    files_to_check = [
        os.path.join(base_dir, "templates", "tips.html"),
        os.path.join(base_dir, "translations.py")
    ]
    
    bad_pattern = "C:\\Users" 
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Filter out lines containing the bad path
                new_lines = [line for line in lines if bad_pattern not in line]
                
                if len(new_lines) < len(lines):
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    print(f"✅ Fixed error in {os.path.basename(file_path)} (removed bad line)")
                else:
                    print(f"✓ {os.path.basename(file_path)} is clean")
            except Exception as e:
                print(f"❌ Error checking {os.path.basename(file_path)}: {e}")

if __name__ == "__main__":
    fix_and_add_video()