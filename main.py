import gtts
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from PIL import Image
import os

def text_to_audio(text, output_audio_file):
    tts = gtts.gTTS(text, lang="en")
    tts.save(output_audio_file)
    print(f"Audio saved: {output_audio_file}")

def crop_and_resize_image(image_path, output_size=(1280, 720)):
    img = Image.open(image_path)
    img_ratio = img.width / img.height
    target_ratio = output_size[0] / output_size[1]

    if img_ratio > target_ratio:
        new_width = int(target_ratio * img.height)
        left = (img.width - new_width) // 2
        img = img.crop((left, 0, left + new_width, img.height))
    else:
        new_height = int(img.width / target_ratio)
        top = (img.height - new_height) // 2
        img = img.crop((0, top, img.width, top + new_height))

    img = img.resize(output_size)
    return img

def create_video_slideshow(image_files, audio_file, output_video_file):
    if not image_files:
        print("No images found!")
        return
    
    audio = AudioFileClip(audio_file)
    audio_duration = audio.duration
    image_duration = max(4, audio_duration / len(image_files))

    clips = []
    for img_path in image_files:
        try:
            processed_image = crop_and_resize_image(img_path)
            temp_image_path = "temp_resized.png"
            processed_image.save(temp_image_path)
            clip = ImageClip(temp_image_path, duration=image_duration).set_fps(10)
            clips.append(clip)
        except Exception as e:
            print(f"Failed to load image: {img_path}, Error: {e}")

    video = concatenate_videoclips(clips, method="compose").set_audio(audio)
    video.write_videofile(output_video_file, fps=10)

    print(f"Video saved: {output_video_file}")

colleges = {
    "1": ("College of Engineering Pune", "The College of Engineering Pune Technological University is a unitary public university of the Government of Maharashtra, situated in Pune, Maharashtra, India. Established in 1854, it is the 3rd oldest engineering institute in India, after College of Engineering, Guindy and IIT Roorkee."),
    "2": ("MIT World Peace University", "The university began as the Maharashtra Institute of Technology (MIT) in 1983, one of the first private engineering colleges in Maharashtra, and a founding institution of the MAEER group. It was initially affiliated with Savitribai Phule Pune University (SPPU). Later, under the guidance of Prof. Vishwanath D. Karad, it transitioned into MIT World Peace University."),
    "3": ("Maulana Mukhtar Ahmad Nadvi Technical Campus", "MMANTC Malegaon, founded in 2012 by Al Jamia Mohammediyah Education Society, offers AICTE/DTE-approved engineering and diploma courses through SPPU and MSBTE affiliations. It features a Siemens Centre of Excellence, placement assistance, and affordable fees."),
    "4": ("SSBT's College of Engineering and Technology", "SSBT's College of Engineering and Technology, Jalgaon, founded in 1983, offers AICTE-approved BE, MBA, MCA, and PhD programs under Kavayitri Bahinabai Chaudhari North Maharashtra University. It features a large campus, modern facilities, placement assistance, and holds NAAC and NBA accreditations."),
    "5": ("Vishwakarma Institute of Technology", "VIT Pune, established in 1983 by the Bansilal Ramnath Agarwal Charitable Trust, is an autonomous AICTE-approved institute permanently affiliated with SPPU. It offers B.Tech, M.Tech, MCA, and PhD programs, known for strong placements, modern infrastructure, and NAAC 'A++' accreditation."),
}

print("\nAvailable Colleges:")
for key, (name, _) in colleges.items():
    print(f"{key}. {name}")

selected_key = input("\nEnter the number of the college (1-5): ").strip()

if selected_key in colleges:
    name, description = colleges[selected_key]
    audio_file = f"outputs/{name.replace(' ', '_')}_audio.mp3"
    video_file = f"outputs/{name.replace(' ', '_')}_video.mp4"

    print(f"\nCreating video for {name}...")

    text_to_audio(description, audio_file)

    image_folder = f"images/{name.replace(' ', '_')}"
    os.makedirs(image_folder, exist_ok=True)  
    image_files = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        print(f"❌ No images found in {image_folder}. Please add images before running the script.")
        exit()

    create_video_slideshow(image_files, audio_file, video_file)

    print(f"{name} video created successfully!")
else:
    print("Invalid input! Please enter a number between 1 and 5.")
