import os
import xml.etree.ElementTree as ET
import pathlib as path
import sys
import logging as log
import json

def parse_spreads(temp_folder):
    p = path.Path(".")
    spreads_path = p / "temp" / "spreads"

    log.info("Searching spreads folder...")
    if not spreads_path.exists():
        log.error("Spreads folder not found")
        sys.exit()
    else:
        log.info("Spreads folder found")

    spreads_data = []

    for file in os.listdir(spreads_path):
        if not file.endswith(".xml"):
            continue

        spread_id = file.rsplit('.', 1)[0]
        spread_info = {
            "id": spread_id,
            "elements": []
        }

        try:
            arbre = ET.parse(spreads_path / file)
            racine = arbre.getroot()
            element_count = {
                "TextFrame": 0,
                "Rectangle": 0,
                "Image": 0
            }

            for element in racine.iter():
                if element.tag not in {"TextFrame", "Rectangle", "Image"}:
                    continue
                success, element_data = detect_store_attributes(element)
                if success:
                    spread_info["elements"].append(element_data)
                    type_element = element_data["type"]
                    if type_element in element_count:
                        element_count[type_element] += 1

            spreads_data.append(spread_info)
            log.info(f"Parsed spread {spread_id} with {len(spread_info['elements'])} elements.")
            log.info(f"Spread {spread_id} parsed successfully: "
                     f"{element_count['TextFrame']} TextFrames, "
                     f"{element_count['Rectangle']} Rectangles, "
                     f"{element_count['Image']} Images.")


        except FileNotFoundError:
            log.error(f"File {file} not found")
            return False, None
        except Exception as e:
            log.error(f"Unexpected error during extraction of {file}: {e}")
            return False, None

    with open("temp/spreads_preview.json", "w") as f:
        json.dump(spreads_data, f, indent=4)

    return (True, spreads_data) if spreads_data else (False, None)


def detect_store_attributes(xml_element):
    data = {}
    type_element = xml_element.tag
    data["type"] = type_element
    data["id"] = xml_element.attrib.get("Self")

    # GeometricBounds
    bounds_str = xml_element.attrib.get("GeometricBounds")
    if bounds_str:
        try:
            y1, x1, y2, x2 = map(float, bounds_str.split())
            width = x2 - x1
            height = y2 - y1
            data["GeometricBounds"] = {
                "x": x1,
                "y": y1,
                "width": width,
                "height": height
            }
        except Exception:
            log.warning(f"Invalid GeometricBounds format in {xml_element}")
            data["GeometricBounds"] = None
    else:
        data["GeometricBounds"] = None
        log.warning(f"No GeometricBounds found in {xml_element}")

    # Type-specific attributes
    if type_element == "TextFrame":
        data["story_id"] = xml_element.attrib.get("ParentStory")
    elif type_element == "Image":
        data["image_href"] = xml_element.attrib.get("LinkResourceURI")
    elif type_element == "Rectangle":
        data["style"] = xml_element.attrib.get("AppliedObjectStyle")

    if data["id"] is None:
        log.debug(f"Ignored {type_element} without ID")
        return False, None

    return True, data
