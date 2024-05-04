#EyeSpy.py is a Python script designed to transform user inputs into visually appealing ASCII tables. 
#With its versatile functionality, EyeSpy.py allows you to create a variety of applications, including interactive games, 
#calendars, or even card and board games, using text-based visuals. Whether you're building a quick game 
#or a structured application, EyeSpy.py provides a simple yet effective way 
#to display your content in an organized and visually engaging manner using ASCII art.
##########################################################################################################################################################################
import json
import os
import time
##########################################################################################################################################################################
# CLASSES
class Header:
    def __init__(self, header_content, cell_count_per_row, border_style):
        self.content = header_content
        self.width = cell_count_per_row * 7
        self.border_style = border_styles.get(
            border_style, border_styles.get("border_style_default", {})
        )

    def get_header(self):
        header_left = self.border_style.get("header_left", "+")
        header_middle = self.border_style.get("header_middle", "-")
        header_right = self.border_style.get("header_right", "+")
        wall = self.border_style.get("wall", "|")
        inner_width = self.width - len(header_left) - len(header_right)
        total_padding = inner_width - len(self.content)
        left_padding = total_padding // 2
        right_padding = total_padding - left_padding
        header_top = f"{header_left}{header_middle * inner_width}{header_right}"
        header_body = f"{wall}{' ' * left_padding}{self.content}{' ' * right_padding}{wall}"
        bottom_left = self.border_style.get("bottom_left", "+")
        bottom_middle = self.border_style.get("bottom_middle", "-")
        bottom_right = self.border_style.get("bottom_right", "+")
        header_bottom = f"{bottom_left}{bottom_middle * inner_width}{bottom_right}"
        return [header_top, header_body, header_bottom]
    def print_header(self):
        header_parts = self.get_header()
        for part in header_parts:
            print(part)


class Cell:
    def __init__(self, content="", width=7, border_style=None):
        self.border_style = border_styles.get(
            border_style, border_styles.get("border_style_default", {})
        )
        self.width = width
        self.content = content

    def get_cell(self):
        header_left = self.border_style.get("header_left", "+")
        header_middle = self.border_style.get("header_middle", "-")
        header_right = self.border_style.get("header_right", "+")
        wall = self.border_style.get("wall", "|")
        inner_width = self.width - len(header_left) - len(header_right)
        cell_top = f"{header_left}{header_middle * inner_width}{header_right}"
        cell_body = f"{wall}{self.content:^5}{wall}" 
        bottom_left = self.border_style.get("bottom_left", "+")
        bottom_middle = self.border_style.get("bottom_middle", "-")
        bottom_right = self.border_style.get("bottom_right", "+")
        cell_bottom = f"{bottom_left}{bottom_middle * inner_width}{bottom_right}"  
        return [cell_top, cell_body, cell_bottom]


class Row:
    def __init__(self, row_id, cells, table_border_style):
        self.row_id = row_id
        self.cells = [
            Cell(cells[i], width=7, border_style=table_border_style)
            for i in range(len(cells))
        ]
    def get_row(self):
        cell_outputs = [cell.get_cell() for cell in self.cells]
        transposed = zip(*cell_outputs)
        row_strings = ["".join(parts) for parts in transposed]
        return row_strings

class Table:
    def __init__(self, row_count, cell_count_per_row, content, table_border_style):
        self.rows = [Row(i, content[i], table_border_style) for i in range(row_count)]
    def print_table(self):
        for row in self.rows:
            row_strings = row.get_row()
            for line in row_strings:
                print(line)


class Screen:
    def __init__(self, screen_data):
        self.header = Header(
            screen_data["header_text"],
            screen_data["cell_count_per_row"],
            screen_data["header_border_style"],
        )
        self.table = Table(
            screen_data["row_count"],
            screen_data["cell_count_per_row"],
            screen_data["table_content"],
            screen_data["table_border_style"],
        )

    def print_screen(self):
        self.header.print_header()
        self.table.print_table()

##########################################################################################################################################################################
#FUNCTIONS
#Load Jsons
def load_json(json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: '{json_path}' file not found.")
    except json.JSONDecodeError:
        print(f"Error: The file contains invalid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

# Styles Setup
def style_setup():
    global border_styles
    script_dir = os.path.dirname(__file__)
    json_path = os.path.join(script_dir, "border_styles.json")
    border_styles = load_json(json_path)  # Use the new JSON loader

# Live Monitoring
def json_monitoring(data_path):
    script_dir = os.path.dirname(__file__)
    json_path = os.path.join(script_dir, data_path)
    screen_data = load_json(json_path)  # Use the new JSON loader
    if screen_data:
        screen = Screen(screen_data)
        screen.print_screen()

def live_monitoring(data_path):
    while True:
        json_monitoring(data_path)
        time.sleep(2)

# Mini Dashboard
def define_dashboard():
    global dashboard
    screen_data = {
        "header_text": "EYESPY DASHBOARD",
        "cell_count_per_row": 3,
        "row_count": 2,
        "header_border_style": "border_style_curved_corners",
        "table_border_style": "border_style_curved_corners",
        "table_content": [
            ["1:", "2:", "3:"],
            ["LOAD", "LIVE", "EXIT"],
        ],
    }
    dashboard = Screen(screen_data)

# Dashboard
def run_dashboard():
    dashboard.header.print_header()
    dashboard.table.print_table()
    option = input("OPTION: ")
    while True:
        if option == '1':
            user_input = input("INPUT DATA PATH: ")
            json_monitoring(user_input)  
            run_dashboard() 
        elif option == '2':
            user_input = input("INPUT DATA PATH: ")
            live_monitoring(user_input) 
            run_dashboard() 
        elif option == '3':
            print("EXITING...")
            break
        else:
            print("Invalid choice, please try again.")
            run_dashboard()

##########################################################################################################################################################################
#SCRIPT 
style_setup()
define_dashboard()
run_dashboard()