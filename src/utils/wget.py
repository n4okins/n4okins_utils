import hashlib
from pathlib import Path

import requests
from tqdm.auto import tqdm


def wget(url: str, save_to: Path) -> None:
    """Download a file from the URL and save it to the path.

    Args:
        url (str): The URL of the file.
        save_to (Path): The path to save the file.
    """
    if not save_to.exists():
        save_to.parent.mkdir(parents=True, exist_ok=True)
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total = int(r.headers.get("content-length", 0))
            with save_to.open("wb") as f:
                for chunk in tqdm(
                    r.iter_content(chunk_size=2**12), total=total // (2**12), unit="KB"
                ):
                    f.write(chunk)


def get_hash(path: str, algo: str = "sha256") -> str:
    """Get the hash of the file.

    Args:
        path (str): The path to the file.
        algo (str, optional): The hash algorithm. Defaults to "sha256".

    Returns:
        str: The hash of the file.
    """
    hasher = hashlib.new(algo)
    chunk = hasher.block_size * 0x800
    with open(path, "rb") as f:
        data = f.read(chunk)
        while data:
            hasher.update(data)
            data = f.read(chunk)
    return hasher.hexdigest()
