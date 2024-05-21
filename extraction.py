# Contains functions that deal with the extraction of documents from a text file (see PR01)

import json

from document import Document


def extract_collection(source_file_path: str) -> list[Document]:
    """
    Loads a text file (aesopa10.txt) and extracts each of the listed fables/stories from the file.
    :param source_file_name: File name of the file that contains the fables
    :return: List of Document objects
    """
    catalog = []  # List to store Document objects
    doc = Document()
    document_id = 0  # Unique document ID counter

    with open(source_file_path, "r", encoding="utf-8") as file:
        # Skip lines until reaching line 308
        for _ in range(307):
            file.readline()

        current_title = None  # Temporary variable to store current fable title
        current_text = ""  # String to accumulate fable text
        inside_raw_text = False
        blank_line_count = 0
        blank_line_inside_raw_text = 0

        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            if line == "" and not inside_raw_text:
                blank_line_count += 1
                continue
            if blank_line_count == 2:
                inside_raw_text = True
                if line == "":
                    blank_line_inside_raw_text += 1
                else:
                    current_text += line + " "
                    blank_line_inside_raw_text = 0
            if blank_line_inside_raw_text == 3:
                blank_line_count = 3

            # Empty line (end of current fable or blank lines)
            if blank_line_count == 3:
                all_terms = current_text.split()
                doc = Document()  # Create a new Document instance
                doc.document_id = document_id
                doc.title = current_title
                doc.raw_text = current_text.strip()
                doc.terms = all_terms
                catalog.append(doc)
                document_id += 1  # Increment document ID
                current_title = None
                current_text = ""
                blank_line_count = 0
                blank_line_inside_raw_text = 0
                inside_raw_text = False
                continue

            if line and not inside_raw_text:  # Line with fable title
                current_title = line

        # Handle the last document if the file ends without enough blank lines
        if current_text or current_title:
            all_terms = current_text.split()
            doc = Document()
            doc.document_id = document_id
            doc.title = current_title
            doc.raw_text = current_text.strip()
            doc.terms = all_terms
            print(doc.terms)
            catalog.append(doc)

    return catalog


def save_collection_as_json(collection: list[Document], file_path: str) -> None:
    """
    Saves the collection to a JSON file.
    :param collection: The collection to store (= a list of Document objects)
    :param file_path: Path of the JSON file
    """

    serializable_collection = []
    for document in collection:
        serializable_collection += [
            {
                "document_id": document.document_id,
                "title": document.title,
                "raw_text": document.raw_text,
                "terms": document.terms,
                "filtered_terms": document.filtered_terms,
                "stemmed_terms": document.stemmed_terms,
            }
        ]

    with open(file_path, "w") as json_file:
        json.dump(serializable_collection, json_file)


def load_collection_from_json(file_path: str) -> list[Document]:
    """
    Loads the collection from a JSON file.
    :param file_path: Path of the JSON file
    :return: list of Document objects
    """
    try:
        with open(file_path, "r") as json_file:
            json_collection = json.load(json_file)

        collection = []
        for doc_dict in json_collection:
            document = Document()
            document.document_id = doc_dict.get("document_id")
            document.title = doc_dict.get("title")
            document.raw_text = doc_dict.get("raw_text")
            document.terms = doc_dict.get("terms")
            document.filtered_terms = doc_dict.get("filtered_terms")
            document.stemmed_terms = doc_dict.get("stemmed_terms")
            collection += [document]

        return collection
    except FileNotFoundError:
        print("No collection was found. Creating empty one.")
        return []
