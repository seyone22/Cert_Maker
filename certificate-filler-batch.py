from PIL import Image, ImageDraw, ImageFont
import os
import json
import argparse
import csv

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

def fetch_records(csvFilename):
    try:
        data = []
        with open(csvFilename, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader)  # This gets the header row

            for row in csvreader:
                # Create a dictionary entry for each row using the header names as keys
                row_data = dict(zip(header, row))
                data.append(row_data)

        return data
    except FileNotFoundError:
        print(f"Data Error: '{csvFilename}' not found.")
        return None
    except Exception as e:
        print(f"Data Error: {e}")
        return None


def generate_certificate(cert_template_path, data, config, save):
    try:
        # counter for number of times the loop runs
        counter = 1
        # Load the certificate template image
        if(cert_template_path == None):
            cert_template_path = "cert_template.png"

        # Load defaults
        font = ImageFont.truetype(config["defaults"]["font_name"], config["defaults"]["font_size"])
        base_name, extension = os.path.splitext(cert_template_path)

        for row_data in data:
            # Opens the template
            template_img = Image.open(cert_template_path)

            # Creates a drawing context
            draw = ImageDraw.Draw(template_img)
            # Defines the filename of the output file
            save_iterator = row_data[save]
            output_path = f"{base_name}_{save_iterator}{extension}"
            # Defines text positions on the certificate
            for text_entry in config["headers"]:
                position = tuple(text_entry["position"])
                name = text_entry["name"]
                font_name = text_entry.get("font_name", config["defaults"]["font_name"])
                font_size = text_entry.get("font_size", config["defaults"]["font_size"])
                color = text_entry.get("color", config["defaults"]["color"])
                font = ImageFont.truetype(font_name, font_size)

                # Perform the actual overlay of text
                draw.text(position, row_data[name], fill=color, font=font)

            # Save the final certificate image
            template_img.save(output_path)
            template_img.close()
            print(f"Certificate generated successfully! Saved at {output_path}")

    except FileNotFoundError:
        print("Error: Certificate template file not found.")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    # Load the config file
    config = load_config("config-batch.json")

    parser = argparse.ArgumentParser(description="Batch overlay certificates with text from a CSV")
    parser.add_argument("-t", "--template", help="Filename of template to overlay. If not provided, the default template 'cert_template.png' will be used.", required=False)
    parser.add_argument("-d", "--data", help="CSV file containing data. This CSV file should contain a header row with the same header names as defined in the config-batch.json file.", required=True)
    parser.add_argument("--save", help="Value to name the output files with. Ensure that this field is unique, and the same as in the config and csv!", required=True)

    args = parser.parse_args()

    # Get input file name from user
    # certificate_template_path = input("Enter the name of the file: ")
    # Get output file name from user (default is 'inputFileName_modified')
    # output_path = input("Enter the name of the output file (with extension): ")
    
    # Generates a data structure from CSV data
    data = fetch_records(args.data)


    # Generate the certificate, with the config file
    generate_certificate(args.template, data, config, args.save)
