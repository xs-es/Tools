import json
from html import escape
import tkinter as tk
from tkinter import filedialog

def chrome_bookmarks_to_html(input_file, output_file):
    # Read the Chrome bookmarks file
    with open(input_file, 'r', encoding='utf-8') as f:
        bookmarks_data = json.load(f)

    # Start the HTML output
    html_output = '''<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
'''

    # Recursive function to process bookmark folders and items
    def process_bookmarks(node, indent=''):
        nonlocal html_output
        
        if 'children' in node:
            html_output += f'{indent}<DT><H3>{escape(node["name"])}</H3>\n{indent}<DL><p>\n'
            for child in node['children']:
                process_bookmarks(child, indent + '    ')
            html_output += f'{indent}</DL><p>\n'
        elif 'url' in node:
            html_output += f'{indent}<DT><A HREF="{escape(node["url"])}">{escape(node["name"])}</A>\n'

    # Process the bookmarks
    process_bookmarks(bookmarks_data['roots']['bookmark_bar'])
    process_bookmarks(bookmarks_data['roots']['other'])

    # Close the HTML structure
    html_output += '</DL><p>'

    # Write the HTML output to a file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_output)

def select_input_file():
    filename = filedialog.askopenfilename(filetypes=[("Chrome Bookmark files", "*.*")])
    input_path.set(filename)

def select_output_file():
    filename = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
    output_path.set(filename)

def convert_bookmarks():
    input_file = input_path.get()
    output_file = output_path.get()
    if input_file and output_file:
        try:
            chrome_bookmarks_to_html(input_file, output_file)
            status_label.config(text="Conversion successful!")
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")
    else:
        status_label.config(text="Please select both input and output files.")

# Create the main window
root = tk.Tk()
root.title("Chrome Bookmarks Converter")

# Create StringVar to hold file paths
input_path = tk.StringVar()
output_path = tk.StringVar()

# Create and place widgets
tk.Label(root, text="Input JSON file:").grid(row=0, column=0, sticky="e")
tk.Entry(root, textvariable=input_path, width=50).grid(row=0, column=1)
tk.Button(root, text="Browse", command=select_input_file).grid(row=0, column=2)

tk.Label(root, text="Output HTML file:").grid(row=1, column=0, sticky="e")
tk.Entry(root, textvariable=output_path, width=50).grid(row=1, column=1)
tk.Button(root, text="Browse", command=select_output_file).grid(row=1, column=2)

convert_button = tk.Button(root, text="Convert", command=convert_bookmarks)
convert_button.grid(row=2, column=1)

status_label = tk.Label(root, text="")
status_label.grid(row=3, column=1)

# Start the GUI event loop
root.mainloop()# Usage
