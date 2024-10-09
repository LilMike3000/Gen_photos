import tkinter as tk
import customtkinter as ctk
import os
import requests
from PIL import Image, ImageTk
from io import BytesIO
import base64
from datetime import datetime

class ImageGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Generator")
        self.root.geometry("700x700")

        self.output_dir = "generated_images"
        os.makedirs(self.output_dir, exist_ok=True)

        self.prompt_label = ctk.CTkLabel(root, text="Prompt:")
        self.prompt_label.pack(pady=5)
        self.prompt_text = ctk.CTkTextbox(root, width=500, height=100)
        self.prompt_text.pack(pady=5)
        
        # Your prompt
        self.prompt_text.insert("1.0", "A man and a woman in Paris. Photorealistic")
        
        self.model_name_label = ctk.CTkLabel(root, text="Model Name:")
        self.model_name_label.pack(pady=5)
        self.model_name_entry = ctk.CTkEntry(root, width=200)
        self.model_name_entry.pack(pady=5)
        self.model_name_entry.insert(0, "dev")

        self.guidance_scale_label = ctk.CTkLabel(root, text="Guidance Scale:")
        self.guidance_scale_label.pack(pady=5)
        self.guidance_scale_entry = ctk.CTkEntry(root, width=200)
        self.guidance_scale_entry.pack(pady=5)
        self.guidance_scale_entry.insert(0, "7")

        self.width_label = ctk.CTkLabel(root, text="Width:")
        self.width_label.pack(pady=5)
        self.width_entry = ctk.CTkEntry(root, width=200)
        self.width_entry.pack(pady=5)
        self.width_entry.insert(0, "1024")

        self.height_label = ctk.CTkLabel(root, text="Height:")
        self.height_label.pack(pady=5)
        self.height_entry = ctk.CTkEntry(root, width=200)
        self.height_entry.pack(pady=5)
        self.height_entry.insert(0, "720")

        self.steps_label = ctk.CTkLabel(root, text="Steps:")
        self.steps_label.pack(pady=5)
        self.steps_entry = ctk.CTkEntry(root, width=200)
        self.steps_entry.pack(pady=5)
        self.steps_entry.insert(0, "20")

        self.iterations_label = ctk.CTkLabel(root, text="Iterations:")
        self.iterations_label.pack(pady=5)
        self.iterations_entry = ctk.CTkEntry(root, width=200)
        self.iterations_entry.pack(pady=5)
        self.iterations_entry.insert(0, "1")

        self.generate_button = ctk.CTkButton(root, text="Generate", command=self.generate_images)
        self.generate_button.pack(pady=20)

        self.status_label = ctk.CTkLabel(root, text="Status: Ready")
        self.status_label.pack(pady=5)

    def generate_images(self):
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        model_name = self.model_name_entry.get()
        guidance_scale = float(self.guidance_scale_entry.get())
        width = int(self.width_entry.get())
        height = int(self.height_entry.get())
        steps = int(self.steps_entry.get())
        iterations = int(self.iterations_entry.get())

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer 134f9ceb214d4cd6adde252855c0d020',
        }

        json_data = {
            'model_name': model_name,
            'guidance_scale': guidance_scale,
            'width': width,
            'model': 'Flux/Dev',
            'prompt': prompt,
            'steps': steps,
            'height': height,
        }

        for i in range(iterations):
            self.status_label.configure(text=f"Status: Generating image {i+1} of {iterations}")
            self.root.update_idletasks()

            response = requests.post('https://open.tensoropera.ai/inference/api/v1/text2Image', headers=headers, json=json_data)

            if response.status_code == 200:
                response_data = response.json()
                image_base64 = response_data['data']['b64_json']
                image_data = base64.b64decode(image_base64)
                image = Image.open(BytesIO(image_data))

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_path = os.path.join(self.output_dir, f"flux_gen_{timestamp}_{i+1}.png")
                image.save(image_path)
                self.status_label.configure(text=f"Status: Image {i+1} saved")
            else:
                self.status_label.configure(text=f"Error: {response.status_code}")
                print(f"Error: {response.status_code}, {response.text}")

        self.status_label.configure(text="Status: Completed")
        self.root.update_idletasks()

if __name__ == "__main__":
    root = ctk.CTk()
    app = ImageGeneratorApp(root)
    root.mainloop()
