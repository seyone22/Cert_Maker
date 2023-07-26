from PIL import Image, ImageDraw, ImageFont
import os
import json

def load_config(config_path):
    try:
        with open(config_path, 'r') as f:
            config_data = json.load(f)
            return config_data
    except FileNotFoundError:
        raise Exception("Config Error: Config file not found.")
    except json.JSONDecodeError:
        raise Exception("Config Error: Invalid JSON format in the config file.")
    except Exception as e:
        raise Exception(f"Config Error: {e}")

def generate_certificate(cert_template_path, output_path, config):
    try:
        # Load the certificate template image
        if(cert_template_path == ""):
            cert_template_path = "cert_template.png"
        template_img = Image.open(cert_template_path)

        # Creates a drawing context
        draw = ImageDraw.Draw(template_img)

        # Load defaults
        font = ImageFont.truetype(config["defaults"]["font_name"], config["defaults"]["font_size"])
        base_name, extension = os.path.splitext(cert_template_path)
        if(output_path == ""):
            output_path = f"{base_name}_modified{extension}"

        # Defines text positions on the certificate
        for text_entry in config["text_positions"]:
            position = tuple(text_entry["position"])
            text = text_entry["text"]
            font_name = text_entry.get("font_name", config["defaults"]["font_name"])
            font_size = text_entry.get("font_size", config["defaults"]["font_size"])
            color = text_entry.get("color", config["defaults"]["color"])
            font = ImageFont.truetype(font_name, font_size)

            # Perform the actual overlay of text
            draw.text(position, text, fill=color, font=font)

        # Save the final certificate image
        template_img.save(output_path)
        print(f"Certificate generated successfully! Saved at {output_path}")

    except FileNotFoundError:
        print("Error: Certificate template file not found.")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    # Load the config file
    config = load_config("config.json")

    # Get input file name from user
    certificate_template_path = input("Enter the name of the file: ")
    # Get output file name from user (default is 'inputFileName_modified')
    output_path = input("Enter the name of the output file (with extension): ")
    
    # Generate the certificate, with the config file
    generate_certificate(certificate_template_path, output_path, config)
