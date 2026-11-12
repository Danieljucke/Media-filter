# Media Duplicate Finder

**A Python desktop application for detecting and managing duplicate images and videos using perceptual hashing and media analysis.**

Media Duplicate Finder scans directories recursively, identifies potentially duplicate media files, and provides an interactive interface for reviewing results and managing redundant files.

The application is designed to help users organize their image and video collections, identify unnecessary copies, and recover storage space.

> **Looking for a newer music management application?**
>
> Explore [MeloShelf](https://github.com/Danieljucke/MeloShelf), my newer local-first music library organizer.
>
> MeloShelf focuses on audio identification, metadata enrichment, artist and album organization, and safe file operations. It is a separate project and does not currently replace Media Duplicate Finder's image and video duplicate detection features.

---

## Features

### Video Duplicate Detection

- Detect visually similar videos using perceptual hashing.
- Sample frames at multiple positions throughout each video.
- Compare video duration alongside frame similarity.
- Identify predominantly dark frames and apply an alternative comparison strategy.
- Support common video formats, including MP4, MKV, AVI, MOV, WMV, FLV, and WebM.

### Image Duplicate Detection

- Identify visually similar images through perceptual hashing.
- Compare images based on their visual content instead of filenames.
- Detect potential duplicates despite some compression or resizing differences.
- Configure the similarity threshold to control detection sensitivity.
- Support formats including JPEG, PNG, BMP, GIF, TIFF, and WebP.

### Duplicate Management

- Display detected duplicates in organized groups.
- Review file paths, sizes, modification dates, and media metadata.
- Choose which files to preserve.
- Mark files for deletion manually.
- Estimate how much disk space can be recovered.
- Require confirmation before deleting selected files.

### Desktop Interface

- Tkinter-based graphical interface.
- Dark color scheme inspired by Catppuccin.
- Adjustable similarity threshold.
- Background scanning with progress updates.
- Context menus for file management.
- Direct access to media files from the results list.

---

## Project Status

Media Duplicate Finder is an earlier standalone project in my media management work.
Its installation and platform compatibility have not been recently verified; review
the detected groups carefully and test with copies before using deletion on important files.

For a newer application focused specifically on organizing music libraries, see [MeloShelf](https://github.com/Danieljucke/MeloShelf).

The two projects currently serve different purposes:

| Media Duplicate Finder | MeloShelf |
|---|---|
| Detects duplicate images and videos | Organizes music libraries |
| Uses visual perceptual hashing | Uses audio fingerprints and metadata |
| Offers manual duplicate review and deletion | Offers identification, metadata review, and verified file moves |
| Uses a Tkinter desktop interface | Uses a local web interface |
| Focuses on duplicate detection | Focuses on audio library organization |

MeloShelf does not currently provide duplicate detection.

---

## Requirements

- Python 3.7 or newer, as originally documented.
- Tkinter support for the desktop interface.
- OpenCV for video processing.
- Pillow for image processing.
- ImageHash for perceptual hashing.

The application is written in Python and uses desktop libraries available on multiple operating systems. Platform-specific compatibility has not been fully verified.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Danieljucke/Media-filter.git
cd Media-filter
```

### 2. Create a Virtual Environment

**Windows:**

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

Or install the main dependencies manually:

```bash
python -m pip install opencv-python Pillow ImageHash
```

### 4. Start the Application

```bash
python main.py
```

The desktop interface will open.

---

## Usage Guide

### Step 1: Select a Folder

Click **Browse** and select the folder containing your media files.

The application scans the selected directory and its subdirectories.

### Step 2: Choose Media Types

Enable the file types you want to analyze:

- Videos
- Images

You can scan either category independently or both together.

### Step 3: Configure Detection Settings

Adjust the similarity threshold according to your needs.

| Threshold | Behavior |
|---|---|
| 0 | Strictest comparison |
| 4–6 | Conservative matching |
| 8 | Default balanced setting |
| 12–15 | More permissive matching |
| 20 | Most permissive setting |

Higher thresholds may increase false positives. Review every result carefully before deleting files.

### Step 4: Scan for Duplicates

Click **Start Scan**.

The application will process supported files, calculate hashes, compare media information, and group possible duplicates.

A progress indicator shows scanning activity.

### Step 5: Review Results

Review the duplicate groups and their metadata.

Each file is marked as either:

- **KEEP:** The file will be preserved.
- **DELETE:** The file is selected for removal.

Use the right-click menu to change the action assigned to a file.

### Step 6: Remove Selected Duplicates

Click **Delete Marked** after reviewing the results.

A confirmation dialog displays the number of selected files and the estimated storage space to be recovered.

**Warning: Deletion is permanent. The application uses direct file deletion and does not provide a recycle-bin or undo mechanism. Back up important files before proceeding.**

---

## File Retention Strategies

The application includes four retention strategies.

| Strategy | Description |
|---|---|
| Keep Largest | Preserves the file with the largest size |
| Keep Smallest | Preserves the file with the smallest size |
| Keep Newest | Preserves the most recently modified file |
| Keep Oldest | Preserves the oldest file |

File size does not always indicate visual quality. The selected file should be reviewed before deletion.

---

## Detection Methods

### Video Analysis

The application extracts frames at five relative positions:

```python
THUMB_SAMPLE_POSITIONS = [
    0.05,
    0.20,
    0.40,
    0.60,
    0.80
]
```

These frames are processed with perceptual hashing.

Video comparisons also consider duration differences.

For videos dominated by dark frames, the implementation may fall back to duration-only comparison.

This fallback can incorrectly classify unrelated videos of similar duration as duplicates.

### Image Analysis

Images are processed using perceptual hashes.

The application compares these hashes to identify visually similar files according to the configured threshold.

Perceptual similarity is not proof that two files are identical.

### Duplicate Grouping

Potential duplicates are grouped by media type.

Only groups containing at least two matched files are displayed.

The grouping approach is heuristic and does not guarantee that every file in a group is mutually identical.

---

## Configuration

The main configuration settings are located in `main.py`.

```python
HASH_SIMILARITY_THRESHOLD = 8
IMAGE_HASH_THRESHOLD = 6

THUMB_SAMPLE_POSITIONS = [
    0.05, 0.20, 0.40, 0.60, 0.80
]

THUMB_SIZE = (64, 64)

DARK_FRAME_BRIGHTNESS = 15
DARK_FRAME_MIN_RATIO = 0.6

DURATION_TOLERANCE_SEC = 2
```

Some values can be adjusted through the application interface.

Changes to internal constants should be tested before use on important media collections.

---

## Limitations

- Perceptual hashing can produce false positives and false negatives.
- Visually similar media files are not necessarily identical.
- Duration-only video comparisons are less reliable than combined visual and duration analysis.
- Large libraries can require substantial processing time.
- Performance depends on file sizes, codecs, storage speed, and hardware.
- Some video or image formats may require additional codec support.
- The current application does not offer a built-in undo function.
- Deleted files are not moved to the recycle bin.
- Platform compatibility and performance benchmarks have not been independently verified.

---

## Documentation

Additional documentation is available in the repository:

- [Quick Start](QUICKSTART.md)
- [Configuration Reference](CONFIG_REFERENCE.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Contributing](CONTRIBUTING.md)
- [Documentation Index](DOCS_INDEX.md)

## Related Project: MeloShelf

[MeloShelf](https://github.com/Danieljucke/MeloShelf) is my newer open-source music library organizer.

It provides features such as:

- Audio identification using Chromaprint and AcoustID.
- Music metadata enrichment through MusicBrainz.
- Artist and album folder organization.
- Album artwork management.
- Manual review of unidentified recordings.
- Verified file moves and recovery from interrupted operations.
- A local-first interface for managing music collections.

MeloShelf is designed for music organization rather than image and video duplicate cleanup.

**Repository:** https://github.com/Danieljucke/MeloShelf

---

## Contributing

Contributions, bug reports, and suggestions are welcome.

To contribute:

1. Open an issue describing the problem or proposed improvement.
2. Fork the repository.
3. Implement and test your changes.
4. Submit a pull request with a description of the changes.

For more information, see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is distributed under the MIT License.

See the [LICENSE](LICENSE) file for details.

## Disclaimer

This software is provided as-is, without any warranty.

Duplicate detection relies on similarity algorithms and may produce incorrect results. Users are responsible for verifying files before deletion.

Always maintain backups of important data.
