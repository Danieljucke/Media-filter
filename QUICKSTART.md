# Quick Start Guide

Get Media Duplicate Finder up and running in 5 minutes!

## Installation (2 minutes)

### Windows
```bash
# 1. Open Command Prompt or PowerShell
# 2. Navigate to the application folder
cd "path\to\media-duplicate-finder"

# 3. Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
python main.py
```

### macOS / Linux
```bash
# 1. Open Terminal
# 2. Navigate to the application folder
cd path/to/media-duplicate-finder

# 3. Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
python main.py
```

## Your First Scan (3 minutes)

1. **Click "Browse..."** and select a folder with duplicate media
   - Example: Your Downloads folder, Pictures folder, or Video library

2. **Check the options:**
   - ✅ Videos (if you want to find duplicate videos)
   - ✅ Images (if you want to find duplicate images)

3. **Keep settings default:**
   - Keep: "Largest file" (best quality)
   - Similarity: 8 (balanced accuracy)

4. **Click "Start Scan"**
   - Watch the progress bar
   - Results appear automatically

5. **Review results:**
   - Green "KEEP" files will be saved
   - Red "DELETE" files will be removed
   - Right-click to change any selection

6. **Click "Delete Marked"**
   - Confirm the action
   - Done! You've freed up disk space

## Common Scenarios

### Clean Up Photos
```
1. Uncheck "Videos"
2. Set threshold to 4-6 (stricter)
3. Choose "Keep Largest" (best resolution)
4. Scan your Pictures folder
```

### Clean Up Videos
```
1. Uncheck "Images"
2. Keep threshold at 8 (default)
3. Choose "Keep Largest" or "Keep Newest"
4. Scan your Videos folder
```

### Find Any Similar Files
```
1. Check both "Videos" and "Images"
2. Set threshold to 12-15 (loose)
3. Choose preferred strategy
4. Scan entire media folder
5. Carefully review results
```

## Pro Tips

### Tip 1: Start Conservative
- Use threshold 4-6 first
- Manually verify before deleting
- Increase threshold if you're missing duplicates

### Tip 2: Scan by Type
- Scan images and videos separately for better control
- Fine-tune thresholds for each type

### Tip 3: Check Modification Dates
- Choose "Keep Newest" for version-controlled files
- Choose "Keep Oldest" to preserve originals

### Tip 4: Use "Keep Smallest"
- Best for archiving or backup to save space
- Trades quality for storage

### Tip 5: Preview Before Deleting
- Right-click files to mark as KEEP/DELETE
- Change marked files before clicking delete
- No undo after deletion!

## Understanding Results

### Video Results Show:
- **[VIDEO] Group 1**: Duplicate video files
- **[dark]**: File has mostly dark/black frames (credits, intros)
- Duration: How long the video is
- Method: How duplicates were detected (hash, duration, etc.)

### Image Results Show:
- **[IMAGE] Group 1**: Duplicate image files
- Resolution: Image dimensions (width × height)
- Method: Always "perceptual hash" for images

### Example:
```
[VIDEO] Group 1 (3 files) [thumbnail hash + duration]
  KEEP   | video | /path/to/Movie.mp4         | 150 MB  | 1:45:20  | 2024-01-15 14:30
  DELETE | video | /path/to/Movie.mp4 copy    | 148 MB  | 1:45:18  | 2024-01-10 09:15
  DELETE | video | /path/to/Movie (old).mp4   | 150 MB  | 1:45:20  | 2023-12-20 11:45
```

## Keyboard Shortcuts

- **Right-click on file** → Toggle KEEP/DELETE
- **Double-click on file** → Open in folder/default app
- **Scroll** → View more files in group

## When to Use Each Strategy

| Strategy | Best For | Example |
|----------|----------|---------|
| Keep Largest | Quality preservation | Keep HD, remove low-res copies |
| Keep Smallest | Space saving | Archive mode, budget backups |
| Keep Newest | Active projects | Work folders with versions |
| Keep Oldest | Original preservation | Document archives |

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| "Select a valid folder" | Browse again, ensure folder exists |
| Very slow scanning | Close other apps, try smaller folder |
| No duplicates found | Increase threshold (e.g., 8→12) |
| Too many false positives | Decrease threshold (e.g., 8→4) |
| FFmpeg errors | Normal, app still works |

## Next Steps

✅ **Basic usage**: You now know enough to find duplicates!

📚 **Learn more**: Read [README.md](README.md) for detailed documentation

⚙️ **Customize**: Check [CONFIG_REFERENCE.md](CONFIG_REFERENCE.md) for advanced settings

🔧 **Troubleshoot**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed help

## Need Help?

- Check [README.md](README.md) → How it Works section
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) → Common Issues
- Check [CONFIG_REFERENCE.md](CONFIG_REFERENCE.md) → Tuning Parameters

Happy deduplicating! 🎉
