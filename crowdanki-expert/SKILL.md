---
name: crowdanki-expert
description: Expert guidance for generating Anki decks using the CrowdAnki JSON format. Use when creating or updating music theory, language, or technical flashcard decks that require stable updates and specific formatting.
---

# CrowdAnki Expert

This skill provides procedural knowledge for creating and maintaining Anki decks using the CrowdAnki JSON export format.

## Core Lessons Learned

### 1. JSON Structure and Types
CrowdAnki uses a strictly typed JSON structure. Every major object must have a `__type__` field:
- `Deck`
- `Note`
- `NoteModel` (contains the card template and field definitions)
- `DeckConfig`

### 2. Stable Updates via UUIDs
To prevent duplicate cards when re-importing an updated deck, you must use stable UUIDs:
- **Hardcode** `crowdanki_uuid` for the `Deck`, `NoteModel`, and `DeckConfig`.
- **Note-Level UUIDs**: Each note must have a `crowdanki_uuid` that is **stored in your source data**.
  - **Do NOT** hash the `Front` field of the card (e.g., using `uuid.uuid5`). If you fix a typo or reword the card's front, the UUID will change, and CrowdAnki will create a duplicate.
  - **Instead**, generate a random UUID once for each card and keep it in your script or data file forever. This ensures the card stays stable even if its content is completely rewritten.

### 3. Required Fields
Missing fields can cause silent failures or explicit errors during import:
- In `NoteModel.flds`, the `sticky: false` property is often required.
- Ensure `note_model_uuid` in each `Note` matches the `crowdanki_uuid` of a `NoteModel` defined in the same file.

### 4. File and Directory Naming
For CrowdAnki to recognize a folder for import:
- The JSON file should ideally be named the same as the parent directory (e.g., `my_deck/my_deck.json`).
- Anki's "Import from JSON" expects you to select the *directory* containing the JSON file.

### 5. Media and SVGs
- **SVGs**: Small SVGs can be embedded directly into fields as HTML string literals (e.g., `'<svg>...</svg>'`). This is excellent for musical notation or mathematical symbols.
- **Unicode**: Use standard Unicode symbols where possible (e.g., `𝄞`, `𝄢`).

### 6. GitHub Import Requirements
The "Import from GitHub" feature in the CrowdAnki add-on has specific expectations for the repository structure:
- The main JSON file **must** be located in the root directory of the repository.
- The JSON file **must** be named exactly the same as the repository (e.g., a repository named `my-anki-deck` must have a `my-anki-deck.json` file in the root).
- If these conditions are not met, the import will fail with an error indicating the file was not found.

## Workflow

1. **Initialize UUIDs**: Generate 3 random UUIDs for the Deck, Model, and Config. Save these in your generation script.
2. **Define Schema**: Create a `NoteModel` with the desired fields (e.g., Front, Back, Category, Tags).
3. **Automate Generation**: Use a script to map your data to the CrowdAnki JSON structure.
4. **Validation**: Verify that `len(notes)` matches your expected count and that all UUIDs are correctly linked.

## Reference Script
A template Python script for generating compatible JSON is available in `scripts/generate_crowdanki.py`.
