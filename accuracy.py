def compare_files(source_file, interpreted_file):
    with open(source_file, 'r') as src, open(interpreted_file, 'r') as interp:
        src_text = src.read()
        interp_text = interp.read()

    total_characters = len(src_text)

    if total_characters == 0:
        print("Source file is empty.")
        return

    matching_characters = sum(1 for src_char, interp_char in zip(src_text, interp_text) if src_char == interp_char)

    # If the interpreted text is shorter than the source text, count the extra source text characters as mismatches
    if len(interp_text) < len(src_text):
        matching_characters -= (len(src_text) - len(interp_text))

    document_accuracy = (matching_characters / total_characters) * 100 if total_characters > 0 else 0

    print(f"Document Accuracy: {document_accuracy:.2f}%")