from pathlib import Path
from typing import Union

import obsidiantools.api as otools

ATTACHMENTS = True


def extract_vault(path_voult_folder: Union[Path, str]):
    path_voult_folder = Path(path_voult_folder)

    assert path_voult_folder.exists(), f"Directory {path_voult_folder} does not exsist"

    vault = otools.Vault(path_voult_folder).connect(attachments=ATTACHMENTS).gather()
    df = vault.get_all_file_metadata()
    print(df.info())

    return vault
