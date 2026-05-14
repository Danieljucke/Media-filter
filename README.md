# Media Duplicate Finder

A powerful desktop application that recursively scans folders for duplicate media files (videos and images) using perceptual hashing and intelligent comparison algorithms.

## Features

- **🎥 Video Duplicate Detection**
  - Samples frames at 5 strategic positions (5%, 20%, 40%, 60%, 80%)
  - Uses perceptual hashing for frame comparison
  - Detects dark/blank frames (credits, intros) and handles them intelligently
  - Matches videos by hash similarity + duration tolerance

- **🖼️ Image Duplicate Detection**
  - Perceptual hash-based comparison (content-aware, not pixel-by-pixel)
  - Detects visually similar images even after compression or minor edits
  - Customizable similarity threshold

- **💾 Smart File Management**
  - Interactive GUI with file list and metadata
  - Multiple deletion strategies:
    - Keep largest file
    - Keep smallest file
    - Keep newest file
    - Keep oldest file
  - Adjustable similarity thresholds (0=exact only, 20=very loose)
  - Preview space that will be freed before deletion

- **🎨 Modern Dark UI**
  - Catppuccin-inspired color scheme
  - Responsive layout
  - Right-click context menu for file management
  - Double-click to open files in explorer/default app
  - Progress bar with real-time scanning updates

## System Requirements

### Python Version
- Python 3.7+

### Dependencies
```
opencv-python       # Video frame extraction
Pillow             # Image processing
imagehash          # Perceptual hashing
```

### OS Support
- ✅ Windows
- ✅ macOS
- ✅ Linux

## Installation

### 1. Clone or Download
```bash
git clone <repository-url>
cd media-duplicate-finder
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install opencv-python Pillow imagehash
```

## Usage

### Running the Application
```bash
python main.py
```

### Step-by-Step Guide

1. **Select Folder**: Click "Browse..." to choose the folder to scan
   - The app will recursively scan all subfolders

2. **Configure Scan Options**:
   - Check/uncheck "Videos" and "Images" to specify what types to scan
   - Choose a deletion strategy under "Keep:" (default: Largest file)
   - Adjust "Similarity threshold" slider (8 is recommended):
     - 0 = Exact matches only (very strict)
     - 8 = Similar items (default, balanced)
     - 20 = Loose matching (may find false positives)

3. **Start Scan**: Click "Start Scan"
   - Progress bar shows scanning progress
   - Status bar displays file counts and comparison method

4. **Review Results**:
   - Duplicate groups are organized hierarchically
   - Files marked "KEEP" (green) and "DELETE" (red)
   - See file size, duration/resolution, and modification date
   - Right-click to manually mark files as KEEP or DELETE
   - Double-click to open file in explorer/default app

5. **Delete Files**: Click "Delete Marked" to permanently remove duplicates
   - Confirmation dialog shows space that will be freed
   - **Warning**: Deletion cannot be undone

## Configuration

Edit these constants in `main.py` to customize behavior:

```python
# Hash Thresholds (lower = stricter)
HASH_SIMILARITY_THRESHOLD = 8      # Videos (0-20)
IMAGE_HASH_THRESHOLD = 6            # Images (0-20)

# Video Processing
THUMB_SAMPLE_POSITIONS = [0.05, 0.20, 0.40, 0.60, 0.80]  # Frame sample positions
THUMB_SIZE = (64, 64)               # Hash resolution
DARK_FRAME_BRIGHTNESS = 15          # Dark frame detection threshold
DARK_FRAME_MIN_RATIO = 0.6          # Use duration-only if 60%+ frames are dark
DURATION_TOLERANCE_SEC = 2          # Acceptable duration difference (seconds)

# Supported Formats
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ...}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ...}
```

## How It Works

### Video Detection Algorithm

1. **Frame Sampling**: Extracts 5 frames at strategic positions throughout the video
2. **Dark Frame Detection**: Identifies blank/credit frames (average pixel brightness < 15)
3. **Perceptual Hashing**: Converts each frame to a 64x64 perceptual hash
4. **Dual Comparison Strategy**:
   - If both videos have ≥60% dark frames → Compare by duration only (handles black frames/intros)
   - Otherwise → Compare hash similarity + duration tolerance

### Image Detection Algorithm

1. **Perceptual Hashing**: Converts image to 64x64 perceptual hash
2. **Hash Comparison**: Measures Hamming distance between hashes
3. **Similarity Matching**: Files with distance ≤ threshold are marked as duplicates

### Duplicate Grouping

Uses a greedy clustering approach:
- Videos grouped separately from images
- Each file compared against all others
- Once matched, file is marked as visited (prevents duplicates in groups)
- Only groups with 2+ files are returned

## Example Workflows

### Find Duplicate Photos
1. Uncheck "Videos", keep "Images" checked
2. Select threshold 4-6 for strict matching
3. Choose "Keep Largest" to retain best quality
4. Scan and review

### Find Duplicate Video Clips
1. Uncheck "Images", keep "Videos" checked
2. Use default threshold 8 for balanced matching
3. Choose strategy based on preference
4. Review dark frame detection (shown in results)

### Find Very Similar But Not Identical Files
1. Check both "Videos" and "Images"
2. Increase threshold to 12-15
3. Review results carefully for false positives
4. Manually adjust selections as needed

## File Info Display

| Column | Description |
|--------|-------------|
| Action | KEEP (green) or DELETE (red) |
| Type | Video or Image |
| File path | Full file path (videos show "[dark]" flag if mostly dark) |
| Size | File size in human-readable format |
| Duration / Resolution | Video duration (HH:MM:SS) or image resolution (WxH) |
| Modified | Last modification date and time |

## Deletion Strategies Explained

- **Keep Largest**: Preserves highest quality/complete files, saves disk space
  - Best for: Redundant copies, downloads
  - Tiebreaker: Newer file

- **Keep Smallest**: Removes high-quality duplicates, keeps compressed versions
  - Best for: Archives, backups where size matters
  - Tiebreaker: Newer file

- **Keep Newest**: Preserves most recent files, removes old duplicates
  - Best for: Video projects, photo libraries with versioning
  - Tiebreaker: Larger file

- **Keep Oldest**: Preserves original files, removes modifications
  - Best for: Projects where original version is preferred
  - Tiebreaker: Larger file

## Performance Tips

- **Large Libraries** (1000+ files): Scan in batches by folder
- **Network Drives**: Copy files locally first (scanning is I/O intensive)
- **High Similarity Threshold**: Use ≤10 to reduce false positives
- **Video Processing**: Slower than images; consider scanning videos/images separately

## Troubleshooting

### "Please select a valid folder first"
- Folder path may be invalid or moved
- Ensure path exists and has read permissions

### Scan is very slow
- Video processing is computationally intensive
- Large videos take longer to hash
- Try reducing folder size or using a faster storage device

### FFmpeg/OpenCV warnings
- Normal - errors are suppressed but warnings may appear
- Video processing still works correctly
- Ensure FFmpeg is installed (usually bundled with OpenCV)

### High false positive rate
- Reduce similarity threshold (e.g., 8 → 6)
- Threshold of 4-6 is stricter, 12-15 is looser
- Manually verify before deletion

## Technical Details

### Perceptual Hashing
- Uses pHash (Perceptual Hash) algorithm
- Converts images to frequency domain to detect structural similarities
- Robust to compression, scaling, and color changes
- 64-bit hash allows quick Hamming distance comparison

### Hamming Distance
- Counts bit differences between two hashes
- Lower value = more similar
- Normalized by hash length for consistent thresholds

### Threading
- GUI remains responsive during scanning
- Scan runs in background thread
- Progress updates in real-time without blocking UI

## License

MIT License - Feel free to use, modify, and distribute

## Contributing

Found a bug? Have a feature request? Feel free to:
1. Open an issue
2. Submit a pull request
3. Provide feedback

## Performance Benchmarks

| Task | Performance |
|------|-------------|
| Scan 1000 images | ~2-5 seconds |
| Scan 100 videos (avg 5MB) | ~30-60 seconds |
| Find groups of 100 duplicates | ~5 seconds |
| Delete 50 files | ~2 seconds |

*Times vary based on hardware and file sizes*

## Future Enhancements

- [ ] Batch processing for multiple folders
- [ ] CSV export of duplicate groups
- [ ] Undo functionality for deleted files
- [ ] Advanced filters (by date range, file size)
- [ ] Command-line interface
- [ ] Exclude patterns (regex support)
- [ ] Move to recycle bin instead of permanent delete

---

**Questions or issues?** Please open an issue on the repository.
