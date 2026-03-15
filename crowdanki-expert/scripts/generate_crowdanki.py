import json
import uuid
import datetime
import argparse

def generate_crowdanki_json(deck_name, cards, deck_uuid=None, model_uuid=None, config_uuid=None):
    """
    Generates a CrowdAnki-compatible JSON file.
    
    :param deck_name: Name of the Anki deck.
    :param cards: List of dicts or tuples: (UUID, Front, Back, Category, Tags).
    :param deck_uuid: Optional stable UUID for the deck.
    :param model_uuid: Optional stable UUID for the note model.
    :param config_uuid: Optional stable UUID for the deck configuration.
    """
    # Use provided UUIDs or generate random ones (not recommended for production updates)
    deck_uuid = deck_uuid or str(uuid.uuid4())
    model_uuid = model_uuid or str(uuid.uuid4())
    config_uuid = config_uuid or str(uuid.uuid4())
    
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    notes = []
    for card_uuid, front, back, category, tags in cards:
        notes.append({
            "__type__": "Note",
            "crowdanki_uuid": card_uuid,
            "fields": [front, back, category, current_date],
            "note_model_uuid": model_uuid,
            "tags": tags
        })
        
    deck = {
        "__type__": "Deck",
        "children": [],
        "crowdanki_uuid": deck_uuid,
        "deck_configurations": [
            {
                "__type__": "DeckConfig",
                "crowdanki_uuid": config_uuid,
                "name": "Default",
                "new": {"perDay": 20},
                "rev": {"perDay": 200}
            }
        ],
        "deck_config_uuid": config_uuid,
        "desc": f"{len(notes)} cards generated for {deck_name}.",
        "media_files": [],
        "name": deck_name,
        "note_models": [
            {
                "__type__": "NoteModel",
                "crowdanki_uuid": model_uuid,
                "flds": [
                    {"name": "Front", "ord": 0, "sticky": False, "rtl": False, "font": "Arial", "size": 20, "media": []},
                    {"name": "Back", "ord": 1, "sticky": False, "rtl": False, "font": "Arial", "size": 20, "media": []},
                    {"name": "Category", "ord": 2, "sticky": False, "rtl": False, "font": "Arial", "size": 20, "media": []},
                    {"name": "Last Updated", "ord": 3, "sticky": False, "rtl": False, "font": "Arial", "size": 20, "media": []}
                ],
                "name": f"{deck_name} Card Model",
                "css": ".card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n",
                "type": 0,
                "sortf": 0,
                "tmpls": [
                    {
                        "name": "Card 1",
                        "ord": 0,
                        "qfmt": '<div style="font-family: Arial; font-size: 14px; color: gray; margin-bottom: 10px;">{{Category}}</div><div style="font-family: Arial; font-size: 32px; text-align: center;">{{Front}}</div>',
                        "afmt": '{{FrontSide}}\n\n<hr id=answer>\n\n<div style="font-family: Arial; font-size: 20px; text-align: center;">{{Back}}</div>\n<div style="font-family: Arial; font-size: 12px; color: gray; text-align: center; margin-top: 20px;">Updated: {{Last Updated}}</div>'
                    }
                ]
            }
        ],
        "notes": notes
    }
    return deck

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate CrowdAnki JSON")
    parser.add_argument("--name", required=True, help="Deck name")
    parser.add_argument("--output", default="deck.json", help="Output JSON file")
    # In a real scenario, you'd pass card data via file or other means.
    # This is a template script.
    print("This is a template script for generating CrowdAnki JSON.")
