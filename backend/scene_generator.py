# backend/scene_generator.py
# FASTER VERSION - Quicker TTS speech for shorter videos

import cv2
import numpy as np
from pathlib import Path
import base64
from PIL import Image
import io
import os
import re
import subprocess

try:
    from gtts import gTTS
    TTS_OK = True
except:
    TTS_OK = False

class VideoGenerator:
    def __init__(self):
        self.videos_dir = Path("assets/videos")
        self.videos_dir.mkdir(parents=True, exist_ok=True)
        self.audio_dir = Path("assets/audio")
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        
        self.fps = 30
        self.size = (1280, 720)
    
    def b64_to_img(self, b64):
        """Convert base64 to numpy array"""
        try:
            if not b64:
                return None
            data = base64.b64decode(b64)
            img = Image.open(io.BytesIO(data))
            img = img.convert('RGB')
            arr = np.array(img)
            print(f"    ✓ Decoded: {arr.shape}")
            return arr
        except Exception as e:
            print(f"    ✗ Decode failed: {e}")
            return None
    
    def resize_for_video(self, img):
        """Resize image maintaining aspect ratio"""
        try:
            h, w = img.shape[:2]
            target_w, target_h = self.size
            
            # Calculate scaling
            scale = min(target_w / w, target_h / h)
            new_w = int(w * scale)
            new_h = int(h * scale)
            
            # Resize
            resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
            
            # Create canvas and center image
            canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)
            x_offset = (target_w - new_w) // 2
            y_offset = (target_h - new_h) // 2
            canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
            
            # Convert RGB to BGR for OpenCV
            canvas = cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR)
            
            print(f"    ✓ Resized to {self.size}")
            return canvas
        except Exception as e:
            print(f"    ✗ Resize failed: {e}")
            return None
    
    def create_fade(self, img1, img2, frames):
        """Smooth fade transition"""
        result = []
        for i in range(frames):
            alpha = i / frames
            blend = cv2.addWeighted(img1, 1-alpha, img2, alpha, 0)
            result.append(blend)
        return result
    
    def create_zoom(self, img, frames):
        """Ken Burns effect"""
        result = []
        h, w = img.shape[:2]
        
        for i in range(frames):
            progress = i / frames
            zoom = 1 + 0.08 * progress
            
            crop_w = int(w / zoom)
            crop_h = int(h / zoom)
            
            x = int((w - crop_w) * progress * 0.5)
            y = int((h - crop_h) * progress * 0.5)
            
            x = max(0, min(x, w - crop_w))
            y = max(0, min(y, h - crop_h))
            
            cropped = img[y:y+crop_h, x:x+crop_w]
            zoomed = cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)
            result.append(zoomed)
        
        return result
    
    def calculate_duration_smart(self, story: str, num_images: int) -> tuple:
        """
        FASTER CALCULATION - Normal speech speed for shorter videos
        Returns: (total_duration, time_per_image)
        """
        words = len(story.split())
        
        # NORMAL/FAST reading speed - 3.5 words per second
        # This gives natural-sounding but not slow speech
        words_per_second = 3.5
        
        # Calculate time needed to read story at normal speed
        time_for_full_story = words / words_per_second
        
        # Add only 10% buffer (less than before)
        total_duration = time_for_full_story * 1.1
        
        # Ensure minimum 3 seconds per image (reduced from 4)
        min_per_image = 3
        min_total_from_images = num_images * min_per_image
        
        # Use MAXIMUM of both
        if total_duration < min_total_from_images:
            total_duration = min_total_from_images
        
        # Calculate time per image
        time_per_image = total_duration / num_images
        
        print(f"\n   📊 VIDEO TIMING (FASTER):")
        print(f"   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"   Story: {words} words")
        print(f"   Reading speed: {words_per_second} words/second (NORMAL)")
        print(f"   Time to read: {time_for_full_story:.1f} seconds")
        print(f"   Buffer (10%): +{time_for_full_story * 0.1:.1f} seconds")
        print(f"   Total duration: {total_duration:.1f} seconds")
        print(f"   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"   Images: {num_images}")
        print(f"   Time per image: {time_per_image:.1f} seconds")
        print(f"   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        return (total_duration, time_per_image)
    
    def generate_audio(self, story: str, sid: str):
        """Generate TTS audio with NORMAL SPEED (not slow)"""
        if not TTS_OK:
            print("   ⚠️  gTTS not installed - Please install: pip install gtts")
            return None
        
        try:
            print("\n   🎤 GENERATING AUDIO (NORMAL SPEED)...")
            print("   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            
            # Clean text
            clean = re.sub(r'\s+', ' ', story).strip()
            
            path = self.audio_dir / f"audio_{sid}.mp3"
            
            words = len(clean.split())
            print(f"   Words: {words}")
            print(f"   Creating NORMAL SPEED speech...")
            
            # Use slow=False for NORMAL/FASTER speech
            # This makes videos shorter
            tts = gTTS(text=clean, lang='en', slow=False)
            tts.save(str(path))
            
            if os.path.exists(path):
                size = os.path.getsize(path) / 1024
                # Estimate duration with normal speed
                estimated_duration = words / 3.5  # Normal = 3.5 words/second
                print(f"   ✅ Audio: {size:.1f} KB")
                print(f"   ✅ Estimated: ~{estimated_duration:.0f} seconds")
                print(f"   ✅ Speed: NORMAL (faster videos)")
                print("   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                return str(path)
            else:
                print(f"   ❌ Audio file not created")
                return None
                
        except Exception as e:
            print(f"   ❌ Audio error: {e}")
            print(f"   💡 Install: pip install gtts")
            return None
    
    def merge_audio(self, video_path: str, audio_path: str) -> bool:
        """Merge audio using FFmpeg"""
        try:
            print("   🎵 Merging audio...")
            
            output = video_path.replace('.mp4', '_with_audio.mp4')
            
            # FFmpeg command
            cmd = [
                'ffmpeg', '-y', '-loglevel', 'error',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'libx264',
                '-preset', 'fast',
                '-crf', '22',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-shortest',
                '-movflags', '+faststart',
                output
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=180)
            
            if result.returncode == 0 and os.path.exists(output):
                os.remove(video_path)
                os.rename(output, video_path)
                print("   ✅ Audio merged!")
                return True
            else:
                error = result.stderr.decode() if result.stderr else "Unknown"
                print(f"   ❌ FFmpeg failed: {error}")
                return False
                
        except FileNotFoundError:
            print("   ❌ FFmpeg not installed")
            return False
        except Exception as e:
            print(f"   ❌ Audio merge error: {e}")
            return False
    
    def create_slideshow_video(self, images_b64, sid, story=None, effects=True):
        """Create FASTER video with normal speed narration"""
        
        print(f"\n{'='*60}")
        print(f"🎬 CREATING VIDEO (FASTER)")
        print(f"{'='*60}\n")
        
        print(f"📥 Received {len(images_b64)} images")
        
        # Process images
        processed = []
        for i, b64 in enumerate(images_b64, 1):
            if b64:
                print(f"\n  Processing image {i}:")
                img_arr = self.b64_to_img(b64)
                if img_arr is not None:
                    resized = self.resize_for_video(img_arr)
                    if resized is not None:
                        processed.append(resized)
                        print(f"  ✓ Image {i} ready")
        
        if not processed:
            print("\n✗ No images processed")
            return None
        
        print(f"\n✓ {len(processed)} images ready\n")
        
        # FASTER timing calculation
        if story:
            total_dur, per_image = self.calculate_duration_smart(story, len(processed))
        else:
            total_dur = len(processed) * 4
            per_image = 4
            print(f"   ⏱️  Default: {per_image:.1f}s per image")
        
        # Generate FAST audio
        audio_path = None
        actual_audio_duration = None
        
        if story and TTS_OK:
            audio_path = self.generate_audio(story, sid)
            
            if audio_path and os.path.exists(audio_path):
                try:
                    # Get actual audio duration
                    import subprocess
                    result = subprocess.run(
                        ['ffprobe', '-v', 'error', '-show_entries', 
                         'format=duration', '-of', 
                         'default=noprint_wrappers=1:nokey=1', audio_path],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if result.returncode == 0:
                        actual_audio_duration = float(result.stdout.strip())
                        print(f"\n   🎵 Audio: {actual_audio_duration:.1f}s")
                        
                        # Match video to audio
                        total_dur = actual_audio_duration + 0.5
                        per_image = total_dur / len(processed)
                        
                        print(f"   🎬 Video adjusted:")
                        print(f"   Duration: {total_dur:.1f}s")
                        print(f"   Per image: {per_image:.1f}s")
                except:
                    print(f"   ℹ️  Using calculated time")
                    pass
        
        # Create video
        video_file = f"story_{sid}.mp4"
        video_path = self.videos_dir / video_file
        
        print(f"\n🎥 Writing video...\n")
        
        # H.264 codec
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        writer = cv2.VideoWriter(
            str(video_path), 
            fourcc, 
            self.fps, 
            self.size,
            isColor=True
        )
        
        if not writer.isOpened():
            print("   ⚠️  Trying fallback...")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(str(video_path), fourcc, self.fps, self.size, isColor=True)
        
        if not writer.isOpened():
            print("✗ Video writer failed")
            return None
        
        # Calculate frames
        frames_per_image = int(per_image * self.fps)
        transition_frames = int(0.4 * self.fps) if effects else 0  # Shorter transitions
        
        print(f"   ⏱️  Per image: {per_image:.1f}s")
        print(f"   🎞️  Frames: {frames_per_image}")
        if effects:
            print(f"   🔄 Transitions: {transition_frames}")
        print()
        
        total_frames = 0
        
        # Write frames
        for idx, img in enumerate(processed):
            print(f"  📹 Image {idx+1}/{len(processed)}...")
            
            if effects:
                frames = self.create_zoom(img, frames_per_image)
            else:
                frames = [img] * frames_per_image
            
            for frame in frames:
                writer.write(frame)
                total_frames += 1
            
            print(f"  ✓ {len(frames)} frames")
            
            # Transitions
            if idx < len(processed) - 1 and effects and transition_frames > 0:
                trans_frames = self.create_fade(img, processed[idx+1], transition_frames)
                for frame in trans_frames:
                    writer.write(frame)
                    total_frames += 1
                print(f"  ✓ Transition ({transition_frames})")
        
        writer.release()
        cv2.destroyAllWindows()
        
        # Verify
        if not os.path.exists(video_path):
            print("\n✗ Video not created")
            return None
        
        size_bytes = os.path.getsize(video_path)
        if size_bytes < 1000:
            print(f"\n✗ Too small: {size_bytes} bytes")
            return None
        
        duration = total_frames / self.fps
        size_mb = size_bytes / (1024 * 1024)
        
        print(f"\n✅ Video created:")
        print(f"   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"   Duration: {duration:.1f}s")
        print(f"   Size: {size_mb:.2f} MB")
        print(f"   Frames: {total_frames}")
        print(f"   Images: {len(processed)}")
        
        if story:
            words = len(story.split())
            print(f"   Words: {words}")
            print(f"   ✅ FASTER video (normal speech)")
        
        print(f"   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # Merge audio
        audio_merged = False
        if audio_path and os.path.exists(audio_path):
            print(f"\n   🎵 Audio: {audio_path}")
            audio_merged = self.merge_audio(str(video_path), audio_path)
            
            if audio_merged:
                print(f"   ✅ Audio merged!")
            else:
                print(f"   ⚠️  Audio merge failed")
        else:
            if story:
                print(f"   ⚠️  No audio")
            else:
                print(f"   ℹ️  Silent video")
        
        print(f"\n{'='*60}")
        print(f"✨ COMPLETE!")
        print(f"   Images: {len(processed)}")
        print(f"   Audio: {'✅ MERGED (FAST)' if audio_merged else '❌ SKIPPED'}")
        print(f"   File: {video_file}")
        print(f"{'='*60}\n")
        
        return str(video_path)


def create_slideshow_video(images_b64, sid, story=None, effects=True):
    """Create faster slideshow video"""
    try:
        gen = VideoGenerator()
        return gen.create_slideshow_video(images_b64, sid, story, effects)
    except Exception as e:
        print(f"✗ Video error: {e}")
        import traceback
        traceback.print_exc()
        return None