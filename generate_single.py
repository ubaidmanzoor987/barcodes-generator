from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os

# Parameters for layout
barcodes_per_row = 8
barcodes_per_column = 20  # Adjust this based on actual requirements and SVG sizes
left_right_margin = 5 * mm  # Margin at the left and right
top_bottom_margin = 10 * mm  # Margin at the top and bottom
horizontal_padding = 2.5 * mm  # Space between barcodes horizontally
vertical_padding = 2.5 * mm  # Space between barcodes vertically
inner_padding = 0 * mm  # Padding between the barcode and the dotted box

# Calculate the barcode dimensions including padding
barcode_width = (A4[0] - 2 * left_right_margin -
                 (barcodes_per_row - 1) * horizontal_padding) / barcodes_per_row
barcode_height = (A4[1] - 2 * top_bottom_margin -
                  (barcodes_per_column - 1) * vertical_padding) / barcodes_per_column

# Function to draw dotted boxes around barcodes


def drawDottedBox(c, x, y, width, height, dash=[1, 2]):
    c.saveState()
    c.setDash(dash)
    c.rect(x, y, width, height, stroke=1, fill=0)
    c.restoreState()


# Setup the canvas
c = canvas.Canvas("barcodes_sheet_final.pdf", pagesize=A4)

# List all SVG files
svg_files = [f for f in os.listdir("barcodes") if f.endswith('.svg')]
svg_files.sort()  # Make sure the files are sorted in order

# Calculate number of pages needed
num_pages = len(svg_files) // (barcodes_per_row * barcodes_per_column) + \
    (1 if len(svg_files) % (barcodes_per_row * barcodes_per_column) else 0)

# Draw the barcodes and boxes on each page
for page in range(num_pages):
    # Start a new page
    if page > 0:
        c.showPage()
    for row in range(barcodes_per_column):
        for col in range(barcodes_per_row):
            index = page * (barcodes_per_row * barcodes_per_column) + \
                row * barcodes_per_row + col
            if index < len(svg_files):
                barcode_file = svg_files[index]
                x = left_right_margin + col * \
                    (barcode_width + horizontal_padding)
                y = A4[1] - top_bottom_margin - \
                    (row + 1) * (barcode_height + vertical_padding)

                # Load the SVG file, convert to a drawing, and scale it
                drawing = svg2rlg(f"barcodes/{barcode_file}")
                scale_w = (barcode_width - 2 * inner_padding) / drawing.width
                scale_h = (barcode_height - 2 * inner_padding) / drawing.height
                scale = min(scale_w, scale_h)
                drawing.width, drawing.height = drawing.width * scale, drawing.height * scale
                drawing.scale(scale, scale)

                # Calculate the position to center the barcode within the dotted box
                x_pos = x + (barcode_width - drawing.width) / 2
                y_pos = y + (barcode_height - drawing.height) / 2

                # Draw the barcode drawing at the specified centered position
                renderPDF.draw(drawing, c, x_pos, y_pos)

                # Draw a dotted box around the barcode with inner padding
                drawDottedBox(c, x, y, barcode_width + 2, barcode_height + 4)

# Save the PDF
c.save()

print("PDF generated with barcodes.")
