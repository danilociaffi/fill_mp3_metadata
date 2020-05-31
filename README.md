# Fill Metadata

## How to use
1. Copy the MP3 files in `Input/Tracks/`;
2. Copy the `.png` cover art in `Input/Artwork/`;
3. Populate `metadata.csv` with the tags to apply to the MP3 files;
4. Double click on `fill_metadata.exe` (Windows only) or from command line inside the directory run `python3 fill_metadata.py` (any OS);
5. Click the `Start` button;
6. If the track files are not named consistently with the metadata, an error is shown, otherwise all is fine. (*Note*: the filenames must be in the format `Track title [other info]`).

## Dependancies
No dependancy is required to use the executable.<br>
To run the source, you will need Python 3 and the `eyed3` module.