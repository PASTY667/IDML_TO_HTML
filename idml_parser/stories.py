import os
import pathlib as path
import logging as log
import xml.etree.ElementTree as ET
import json

def parse_stories(temp_folder):
    p = path.Path(".")
    stories_path = p / "temp" / "stories"

    log.info("Searching stories folder...")
    if not stories_path.exists():
        log.error(f"Stories folder not found at {stories_path}")
        return False, None
    else:
        log.info(f"Found stories folder at {stories_path}")

    stories_data = {}

    for file in os.listdir(stories_path):
        if not file.endswith(".xml"):
            continue

        story_id = file.rsplit(".", 1)[0]
        log.info(f"Parsing story {file}...")

        try:
            arbre = ET.parse(stories_path / file)
            racine = arbre.getroot()

            success, story_data = detect_story_elements(racine)
            if not success:
                log.warning(f"Failed to extract story elements from {file}")
                continue

            story_data["id"] = story_id
            stories_data[story_id] = story_data

            paragraph_count = len(story_data["paragraphs"])
            log.info(f"Parsed story {story_id} with {paragraph_count} paragraphs.")

        except FileNotFoundError:
            log.error(f"File {file} not found")
            return False, None
        except Exception as e:
            log.error(f"Unexpected error during extraction of {file}: {e}")
            return False, None

    # ✅ Écrire le JSON ici (une seule fois)
    preview_path = p / "temp" / "stories_preview.json"
    with open(preview_path, "w", encoding="utf-8") as f:
        json.dump(stories_data, f, indent=4, ensure_ascii=False)

    log.info(f"Saved stories preview to {preview_path}")
    log.info(f"Parsed {len(stories_data)} stories successfully.")
    return True, stories_data


def detect_story_elements(xml_root):
    data = {"paragraphs": []}

    try:
        for paragraph in xml_root.iter("ParagraphStyleRange"):
            paragraph_style = paragraph.attrib.get("AppliedParagraphStyle")
            paragraph_data = {
                "style": paragraph_style,
                "spans": []
            }

            for span in paragraph.iter("CharacterStyleRange"):
                character_style = span.attrib.get("AppliedCharacterStyle")
                text_content = ""
                for content in span.iter("Content"):
                    if content.text:
                        text_content += content.text
                paragraph_data["spans"].append({
                    "style": character_style,
                    "text": text_content
                })

            data["paragraphs"].append(paragraph_data)

        return True, data

    except Exception as e:
        log.error(f"Error extracting story elements: {e}")
        return False, None
