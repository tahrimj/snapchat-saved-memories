import json
import webbrowser
import sys

# --- Configuration ---
# 1. This is the main key containing the LIST of items.
PRIMARY_LIST_KEY = 'Saved Media'
# 2. This is the key inside EACH item that holds the actual URL you want to open.
URL_KEY_IN_ITEM = 'Media Download Url'
# ---------------------

def open_links_from_json(json_file_path):
    """Parses a JSON file and opens all links found."""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at '{json_file_path}'")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{json_file_path}'")
        return
    except Exception as e:
        print(f"An unexpected error occurred during file reading: {e}")
        return

    # 1. Check if the primary list key exists and is a list
    if PRIMARY_LIST_KEY not in data or not isinstance(data[PRIMARY_LIST_KEY], list):
        print(f"Error: Could not find a list under the key '{PRIMARY_LIST_KEY}'.")
        print("Please check your JSON structure and update the PRIMARY_LIST_KEY variable.")
        return

    media_items = data[PRIMARY_LIST_KEY]
    
    # List to store the actual URLs for processing
    links_to_open = []

    # 2. Iterate through the list of objects and extract the URL
    for item in media_items:
        if isinstance(item, dict) and URL_KEY_IN_ITEM in item:
            url = item[URL_KEY_IN_ITEM]
            # Basic validation: ensure it's a string and looks like a URL
            if isinstance(url, str) and url.startswith(('http://', 'https://')):
                links_to_open.append(url)
            else:
                 # Skip items where the "Media Download Url" is not a valid URL
                pass 
        else:
            # Skip items that are not dictionaries or lack the URL key
            pass

    if not links_to_open:
        print("No valid links found after parsing the file.")
        return

    print(f"Found **{len(links_to_open)}** valid links to open.")
    
    # 3. Open each extracted link
    for i, url in enumerate(links_to_open):
        print(f"Opening link {i+1}/{len(links_to_open)}")
        webbrowser.open_new_tab(url)

    print("\n✅ All valid links have been opened in new browser tabs.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python open_links.py <path_to_your_json_file>")
        print("\nExample: python open_links.py your_data.json")
    else:
        json_file = sys.argv[1]
        open_links_from_json(json_file)
