def clean_text(text: str) -> str:
    return " ".join(text.lower().replace("’", "'").split())


def clean_path_piece(piece: str) -> str :
    return piece.lower().replace("'", "").replace("_", "-")