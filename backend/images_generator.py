# backend/images_generator.py
# ULTRA DETAILED - Extracts exact characters, genders, and details from prompt and story

import os
import requests
import base64
from pathlib import Path
import time
import random
import re

class ImageGenerator:
    def __init__(self):
        self.images_dir = Path("assets/images/generated")
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.session_id = int(time.time()) + random.randint(0, 9999)
    
    def extract_characters_and_details(self, user_prompt: str, story_text: str) -> dict:
        """
        Extract EXACT character details including gender, names, roles
        """
        combined_text = (user_prompt + " " + story_text).lower()
        
        characters = []
        
        # Male characters - SPECIFIC names and descriptions
        male_patterns = {
            'Krishna': ['krishna', 'shri krishna', 'shree krishna', 'lord krishna'],
            'Arjun': ['arjun', 'arjuna', 'arjuna warrior'],
            'Ram': ['ram', 'rama', 'lord ram', 'shri ram'],
            'Lakshman': ['lakshman', 'laxman', 'lakshmana'],
            'Hanuman': ['hanuman', 'pawan putra'],
            'Ravan': ['ravan', 'ravana', 'demon king'],
            'Bheem': ['bheem', 'bheema', 'bhima'],
            'Yudhishthir': ['yudhishthir', 'yudhishthira'],
            'Karna': ['karna'],
            'father': ['father', 'dad', 'papa', 'pita'],
            'grandfather': ['grandfather', 'dada', 'nana', 'grandpa'],
            'brother': ['brother', 'bhai'],
            'son': ['son', 'beta', 'boy child'],
            'boy': ['boy', 'young boy', 'male child'],
            'friend_male': ['two boys', 'boy friends', 'male friends'],
            'king': ['king', 'raja', 'emperor'],
        }
        
        # Female characters - SPECIFIC names and descriptions
        female_patterns = {
            'Sita': ['sita', 'sita devi', 'mata sita'],
            'Draupadi': ['draupadi', 'panchali'],
            'Radha': ['radha', 'radha rani'],
            'Kunti': ['kunti', 'kunti devi'],
            'mother': ['mother', 'mom', 'maa', 'mata'],
            'grandmother': ['grandmother', 'dadi', 'nani', 'grandma'],
            'sister': ['sister', 'bahen', 'didi'],
            'daughter': ['daughter', 'beti', 'girl child'],
            'girl': ['girl', 'young girl', 'female child'],
            'friend_female': ['two girls', 'girl friends', 'female friends'],
            'queen': ['queen', 'rani'],
        }
        
        # Detect male characters
        for name, patterns in male_patterns.items():
            for pattern in patterns:
                if pattern in combined_text:
                    characters.append({
                        'name': name,
                        'gender': 'male',
                        'description': self.get_character_description(name, 'male')
                    })
                    break
        
        # Detect female characters
        for name, patterns in female_patterns.items():
            for pattern in patterns:
                if pattern in combined_text:
                    characters.append({
                        'name': name,
                        'gender': 'female',
                        'description': self.get_character_description(name, 'female')
                    })
                    break
        
        # Remove duplicates
        seen_names = set()
        unique_chars = []
        for char in characters:
            if char['name'] not in seen_names:
                seen_names.add(char['name'])
                unique_chars.append(char)
        
        return {
            'characters': unique_chars,
            'main_topic': user_prompt.strip(),
            'combined_text': combined_text
        }
    
    def get_character_description(self, name: str, gender: str) -> str:
        """
        Get VERY SPECIFIC visual description for each character
        MUST look exactly like the real/mythological figure
        """
        descriptions = {
            # Male mythology characters - EXACT iconic appearance
            'Krishna': 'Lord Krishna with BLUE SKIN COLOR, peacock feather in crown on head, yellow silk dhoti, holding bamboo flute, divine radiant smile, male god with dark blue complexion, traditional Indian deity appearance',
            'Arjun': 'Arjuna the warrior prince, strong athletic male warrior, silver armor and warrior clothes, holding large bow with arrows on back, headband, brave determined face, male Pandava hero',
            'Ram': 'Lord Rama with BLUE SKIN COLOR, bow and quiver of arrows, golden crown, royal yellow dhoti, calm noble face, male prince deity with dark blue complexion',
            'Lakshman': 'Lakshmana, loyal brother warrior, male with armor, holding bow, traditional warrior dress, devoted expression, strong male companion',
            'Hanuman': 'Hanuman the monkey god, RED-ORANGE BODY, muscular monkey face and tail, male monkey deity with devotional pose, powerful build',
            'Ravan': 'Ravana demon king with TEN HEADS stacked vertically, golden crown on each head, fierce demonic face, male demon with dark complexion, multiple arms',
            'Bheem': 'Bheema the strongest Pandava, VERY MUSCULAR male warrior, holding large mace weapon, massive build, powerful physique, warrior clothes',
            'Karna': 'Karna the tragic hero, male archer warrior, GOLDEN KAVACH ARMOR covering chest, earrings, bow and arrows, noble warrior appearance',
            
            # Male family members
            'father': 'Indian father, adult male, traditional kurta pajama, caring expression, male parent',
            'grandfather': 'Indian grandfather, elderly male, white beard, traditional dhoti or kurta, wise old man',
            'brother': 'young Indian boy, brother, traditional clothes, male sibling',
            'son': 'young Indian boy child, son, traditional clothes for boys, male child',
            'boy': 'young Indian boy, male child, simple traditional clothes, playful boy',
            'friend_male': 'two young Indian boys, male friends, traditional boys clothes, playing together',
            'king': 'Indian king, adult male, royal crown, royal robes, regal male ruler',
            
            # Female mythology characters - EXACT iconic appearance
            'Sita': 'Sita Devi, beautiful Indian goddess, elegant RED AND GOLD SAREE, flower jewelry in hair, gentle serene face, divine female appearance, traditional goddess look',
            'Draupadi': 'Draupadi the fire-born queen, beautiful strong Indian woman, DARK LONG HAIR, royal colorful saree, gold jewelry, fierce intelligent eyes, female Panchal princess',
            'Radha': 'Radha Rani, beautiful devoted goddess, BLUE OR PINK SAREE, flower garlands, loving expression toward Krishna, elegant female deity',
            'Kunti': 'Kunti Devi the queen mother, mature graceful Indian woman, royal saree, motherly wise face, traditional jewelry, elderly female queen',
            
            # Female family members
            'mother': 'Indian mother, adult woman, beautiful saree, caring expression, female parent, maternal look',
            'grandmother': 'Indian grandmother, elderly woman, white hair, traditional saree, wise old woman',
            'sister': 'young Indian girl, sister, traditional dress or salwar, female sibling',
            'daughter': 'young Indian girl child, daughter, traditional girls dress, female child',
            'girl': 'young Indian girl, female child, traditional dress, playful girl',
            'friend_female': 'two young Indian girls, female friends, traditional girls clothes, playing together',
            'queen': 'Indian queen, adult woman, royal crown, royal saree, jewelry, regal female ruler',
        }
        
        return descriptions.get(name, f'{name}, {gender} character, traditional Indian appearance')
    
    def create_ultra_detailed_prompts(self, user_prompt: str, story_text: str, num_images: int) -> list:
        """
        Create EXTREMELY detailed prompts with exact character descriptions
        """
        
        # Extract characters
        details = self.extract_characters_and_details(user_prompt, story_text)
        characters = details['characters']
        main_topic = details['main_topic']
        
        print(f"\n   🔍 DETECTED CHARACTERS:")
        if characters:
            for char in characters:
                print(f"      • {char['name']} ({char['gender']})")
        else:
            print(f"      • No specific characters - using general scene")
        
        # Build character description string
        if len(characters) >= 2:
            # Multiple characters
            char_desc = f"{characters[0]['description']} with {characters[1]['description']}"
        elif len(characters) == 1:
            # Single character
            char_desc = characters[0]['description']
        else:
            # No specific characters - use topic directly
            char_desc = main_topic
        
        print(f"   📝 Character Description: {char_desc[:80]}...")
        
        # Art style
        art_style = "colorful children's storybook illustration, detailed cartoon art style, warm bright colors, hand-drawn look, Indian cultural setting, clear and expressive"
        
        prompts = []
        
        for i in range(num_images):
            if i == 0:
                # Scene 1: Establishing shot
                prompt = f"{main_topic}. Showing {char_desc} clearly. {art_style}. Main establishing scene with all characters visible and properly depicted."
                
            elif i == 1:
                # Scene 2: Close-up
                prompt = f"{main_topic}. Close-up of {char_desc} with detailed faces. {art_style}. Emotional expressions, accurate character depiction, clear gender representation."
                
            elif i == 2:
                # Scene 3: Full scene
                prompt = f"{main_topic}. Full scene showing {char_desc} in traditional Indian setting. {art_style}. Complete background, accurate character appearance, proper clothing."
                
            elif i == 3:
                # Scene 4: Interaction
                prompt = f"{main_topic}. {char_desc} interacting together. {art_style}. Clear interaction between characters, accurate depiction of each person, proper gender and appearance."
                
            elif i == 4:
                # Scene 5: Different angle
                prompt = f"{main_topic}. Different perspective showing {char_desc}. {art_style}. Alternative view, maintaining accurate character details and gender representation."
                
            else:  # i == 5 or more
                # Scene 6: Emotional moment
                prompt = f"{main_topic}. Emotional meaningful moment with {char_desc}. {art_style}. Touching scene, accurate character portrayal, proper representation of all individuals."
            
            # Add gender reinforcement for clarity
            if characters:
                genders = [c['gender'] for c in characters]
                gender_note = f" IMPORTANT: Show {' and '.join(genders)} characters as described - maintain accurate gender representation."
                prompt += gender_note
            
            prompts.append(prompt)
        
        return prompts[:num_images]
    
    def generate_single_image(self, prompt: str, scene_num: int) -> str:
        """Generate one image with detailed prompt"""
        
        print(f"  🎨 Image {scene_num}...", end=" ")
        
        try:
            from urllib.parse import quote
            
            # Encode the full detailed prompt
            encoded_prompt = quote(prompt)
            
            # Create seed for variety
            seed = (self.session_id + scene_num * 12345) % 999999
            
            # Pollinations AI URL
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed={seed}&nologo=true&model=flux"
            
            # Make request
            response = requests.get(url, timeout=90)
            
            if response.status_code == 200:
                content_length = len(response.content)
                
                if content_length > 15000:
                    # Save to file
                    filename = f"scene_{scene_num:02d}.png"
                    filepath = self.images_dir / filename
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    # Convert to base64
                    img_b64 = base64.b64encode(response.content).decode('utf-8')
                    
                    size_kb = content_length / 1024
                    print(f"✅ ({size_kb:.0f} KB)")
                    
                    return img_b64
                else:
                    print(f"❌ Too small")
                    return None
            else:
                print(f"❌ Status {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error")
            return None
    
    def generate_images_from_story(self, story_text: str, num_images: int = 6, 
                                   user_prompt: str = "") -> list:
        """
        Generate images with EXACT character details
        """
        
        print(f"\n{'='*70}")
        print(f"🎨 ULTRA-DETAILED IMAGE GENERATION")
        print(f"{'='*70}")
        print(f"   Topic: '{user_prompt}'")
        print(f"   Images: {num_images}")
        
        if not user_prompt or not user_prompt.strip():
            user_prompt = "Indian cultural scene"
            print(f"   ⚠️  No topic given, using default")
        
        # Create ultra-detailed prompts
        print(f"\n📝 Analyzing story for character details...")
        prompts = self.create_ultra_detailed_prompts(user_prompt, story_text, num_images)
        
        # Generate images
        print(f"\n🎨 Generating {num_images} images with detailed character descriptions...")
        print(f"{'='*70}\n")
        
        images = []
        
        for i in range(num_images):
            img = self.generate_single_image(prompts[i], i + 1)
            images.append(img)
            
            if i < num_images - 1:
                print(f"  ⏳ Waiting 7 seconds...\n")
                time.sleep(7)
        
        # Count success
        successful = sum(1 for img in images if img is not None)
        failed_count = num_images - successful
        
        print(f"\n{'='*70}")
        print(f"📊 RESULTS:")
        print(f"   ✅ Successful: {successful}/{num_images}")
        if failed_count > 0:
            print(f"   ❌ Failed: {failed_count}/{num_images}")
        print(f"{'='*70}")
        
        # Retry failed once
        failed_indices = [i for i, img in enumerate(images) if img is None]
        
        if failed_indices and successful > 0:
            print(f"\n♻️  Retrying {len(failed_indices)} failed...\n")
            
            for idx in failed_indices:
                img = self.generate_single_image(prompts[idx], idx + 1)
                if img:
                    images[idx] = img
                time.sleep(7)
        
        final = sum(1 for img in images if img is not None)
        
        print(f"\n{'='*70}")
        print(f"✅ FINAL: {final}/{num_images} images")
        print(f"{'='*70}\n")
        
        return images


def generate_images_from_story(story_text: str, num_images: int = 6, 
                               user_prompt: str = "") -> list:
    """Generate images with exact character details"""
    try:
        generator = ImageGenerator()
        return generator.generate_images_from_story(story_text, num_images, user_prompt)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return [None] * num_images