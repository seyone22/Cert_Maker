# Batch Certificate Detail Filler

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/seyone22/Cert_Maker/python-app.yml)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Introduction

This application was created with the aim of assisting the University of Vavuniya in mass-creating certificates for various events. There are two scripts:
- certificate-filler-batch.py
- certificate-filler.py

## Features

- Supports processing .png, .jpg, and .jpeg files. Should work on other image formats as well, but I haven't tested it.

## Installation

The application only uses the Pillow library.

```bash
pip install -r requirements.txt
```

## Usage

The batch application takes in an image template and a .csv file. Enter the various certificate details in the CSV file. The file MUST have a header row which matche the headers specified in the config-batch.json, which you can configure with the appropriate fonts, font sizes, and positions.

```bash
python certificate-filler-batch.py -d /path/to/your/data.csv -t /path/to/your/template.png --save headerNameToSaveBy
```

The regular application takes in an image template file, and an output file name. Similar to the batch application, you can configure it in config.json, but make sure to enter the data to be overlaid in the config file itself.

```bash
python certificate-filler.py -t /path/to/your/template.png -o outputFileName.png
```

## License

