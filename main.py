import os
from barcode import Code128
from barcode.writer import SVGWriter
import random
import string
import openpyxl

# Function to generate random numeric characters


def generate_random_numeric(length):
    return ''.join(random.choice(string.digits) for _ in range(length))

# Function to generate barcode images with custom pattern


def generate_custom_barcode_images(start, end):
    # Create the folder if it doesn't exist
    if not os.path.exists("barcodes"):
        os.makedirs("barcodes")

    # Create a workbook and select the active worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Barcodes"

    # Add headers to the worksheet
    ws.append(["ID", "Name"])

    for i in range(start, end+1):
        # Generate random numeric characters for the barcode
        random_numeric = generate_random_numeric(8)

        # Generate barcode value with custom pattern
        barcode_value = f"MSS-{random_numeric}"

        # Generate barcode SVG
        code128 = Code128(barcode_value, writer=SVGWriter())
        filepath = os.path.join("barcodes", barcode_value)
        code128.save(filepath, options={'width': 163, 'height': 77})

        # Add barcode details to the worksheet
        ws.append([f"{str(i).zfill(4)}", f"{barcode_value}"])

        print(f"Barcode generated for {barcode_value}")

    # Save the workbook
    wb.save("barcodes.xlsx")


# Generate custom barcode images and create Excel file
generate_custom_barcode_images(1, 5000)
