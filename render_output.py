import cv2 as cv
import numpy as np
import time
import simpleaudio as sa

# Import classes
from effects.calibrator import Calibrator
from effects.color_chaos_manipulator import ColorChaosManipulator
from functions.export_video import export_video_global

VIDEO_PATH = 'assets/example.mp4'
AUDIO_FILE = 'assets/worldwide.wav'

capture = cv.VideoCapture(VIDEO_PATH)

def play_audio(audio_file):
    wave_obj = sa.WaveObject.from_wave_file(AUDIO_FILE)
    play_obj = wave_obj.play()

calibrator = Calibrator()
cc_manipulator = ColorChaosManipulator()

apply_calibration = str(input("Apply calibration? Y or N : "))

#play_audio(AUDIO_FILE)
output_frames = []

print("⚡ Processing frames at MAXIMUM SPEED (no display)...")

frame_count = 0
start_time = time.time()

while True:
    isTrue, frame = capture.read()  
    
    if not isTrue: 
        break
    
    frame_count += 1
    
    # Progress update every 30 frames
    if frame_count % 30 == 0:
        elapsed = time.time() - start_time
        fps = frame_count / elapsed if elapsed > 0 else 0
        print(f"📊 Processed {frame_count} frames ({fps:.1f} fps)")
    
    complexity = calibrator.calculate_complexity(frame)
    
    if apply_calibration == "Y" or apply_calibration == "y":
        calibrator.add_frame(frame)
        processed_frame = calibrator.process_current_frame(frame)
        final_frame = cc_manipulator.process_current_frame(processed_frame, complexity)
        output_frames.append(final_frame)
        
    elif apply_calibration == "N" or apply_calibration == "n":
        calibrator.add_frame(frame)
        output_frames.append(frame)  # Just store original frame
        
    else:
        print("Undefined argument.")
        break

capture.release()

# Export results
if output_frames:
    total_time = time.time() - start_time
    print(f"✅ Processed {len(output_frames)} frames in {total_time:.2f}s")
    print(f"📹 Exporting at {len(output_frames)/total_time:.1f} fps...")
    export_video_global(output_frames, "ferhad.mp4")
    print("🎬 Video exported: ferhad.mp4")
else:
    print("❌ No frames processed!")

print("🎉 Done! Open ferhad.mp4 to see your masterpiece!")