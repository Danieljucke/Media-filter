# Troubleshooting Guide

Comprehensive solutions for common issues.

## Installation Issues

### "python: command not found" or "python is not recognized"

**Windows:**
- Python may not be installed or not in PATH
- Download Python from https://www.python.org/
- ✅ Check "Add Python to PATH" during installation
- Restart Command Prompt after installing
- Verify: `python --version`

**macOS:**
```bash
# Install Python via Homebrew
brew install python3
python3 --version
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip
```

### "ModuleNotFoundError: No module named 'cv2'"

**Solution:**
```bash
# Ensure virtual environment is activated (if using one)
python -m pip install --upgrade pip
pip install opencv-python Pillow ImageHash
```

**Windows:** May require Visual C++ redistributables
- Download: https://support.microsoft.com/en-us/help/2977003

### "ModuleNotFoundError: No module named 'imagehash'"

**Solution:**
```bash
pip install ImageHash
# Note: It's "ImageHash" not "imagehash"
```

### "Permission denied" when installing packages

**Windows:**
```bash
# Run Command Prompt as Administrator
python -m pip install --user opencv-python Pillow ImageHash
```

**macOS/Linux:**
```bash
# Use --user flag instead of sudo
pip install --user opencv-python Pillow ImageHash
```

## Application Won't Start

### GUI window doesn't appear

**Problem:** Application runs but no window shows

**Solutions:**
1. Wait 5-10 seconds (Tkinter can be slow on first launch)
2. Check terminal for error messages
3. Ensure display server is available (Linux)
4. Try with different Python version: `python3 main.py`

### "ImportError: No module named 'tkinter'"

Tkinter is missing (comes with Python but sometimes not installed)

**Windows:**
- Reinstall Python
- ✅ Make sure "tcl/tk and IDLE" is checked

**macOS:**
```bash
brew install python-tk@3.11
# or your Python version
```

**Ubuntu/Debian:**
```bash
sudo apt install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

## Scanning Issues

### "Please select a valid folder first"

**Causes:**
- Path field is empty
- Path doesn't exist or is invalid
- Path contains invalid characters
- User doesn't have read permissions

**Solutions:**
1. Click "Browse..." instead of typing path
2. Ensure folder exists: `ls /path/to/folder` (macOS/Linux) or `dir C:\path` (Windows)
3. Try with a different folder
4. Check permissions: Right-click folder → Properties → Security

### Scan never completes / hangs

**Possible causes:**
- Processing very large files
- Network drive latency
- Corrupted media files
- Insufficient RAM

**Solutions:**
1. **Wait longer** - Video processing is slow
   - ~100-200 videos take 30-60 seconds
   - Large files (>1GB) take longer

2. **Try a smaller folder first**
   - Test with 10-20 files
   - Gradually increase

3. **Close other applications**
   - Free up RAM and CPU
   - Close browser tabs, etc.

4. **Use local storage, not network drives**
   - Copy files to local SSD first
   - Network latency slows scanning significantly

5. **Disable dark frame detection** (advanced)
   - Modify `DARK_FRAME_BRIGHTNESS` in main.py to 0
   - This skips some processing

### Scan is very slow

**This is normal!** Video processing is computationally intensive.

**Performance expectations:**
- Images: ~500/second
- Small videos (<100MB): 10-20 seconds each
- Large videos (>1GB): 30+ seconds each

**To speed up:**
1. Reduce `THUMB_SAMPLE_POSITIONS` (fewer frames sampled)
2. Reduce `THUMB_SIZE` (smaller hashes)
3. Separate video and image scans
4. Use faster storage (SSD vs HDD)
5. Close other applications

**Example fast configuration:**
```python
THUMB_SAMPLE_POSITIONS = [0.25, 0.75]  # Only 2 frames
THUMB_SIZE = (32, 32)  # Smaller
```

### "Scan error" message appears

**Generic error shown**

**What to do:**
1. Note the error message
2. Check the terminal for detailed error
3. Try with a smaller folder
4. Restart the application
5. Update Python and dependencies

**Common file-level errors (ignored automatically):**
- Corrupted video file (can't read frames)
- Unreadable image file (permission issue)
- Unsupported format or codec
- File deleted during scanning

These files are automatically skipped.

### No duplicates found, but I know there are some

**Solutions:**

1. **Lower the similarity threshold**
   ```
   Current: 8
   Try: 4-6 (stricter)
   ```
   - Slide to the left for stricter matching
   - Check "0 = exact only | 8 = similar | 20 = loose"

2. **Check file types are enabled**
   - Make sure "Videos" or "Images" is checked
   - Matching media type

3. **Ensure files meet minimum quality**
   - Videos need readable frames
   - Images need to open successfully
   - Severely corrupted files are skipped

4. **Videos might be too different**
   - Different duration (beyond tolerance)
   - Very different quality/resolution
   - Different codecs or compression

## Results Issues

### Files appear in wrong groups

**This means matching was too loose**

**Solution:**
1. Start scan again
2. Reduce threshold (move slider left)
3. Verify false positives manually

**Example:**
- Threshold 15: "Twilight" might match "Twilight: Breaking Dawn"
- Threshold 8: More accurate matching
- Threshold 4: Very strict

### One group has too many files

**Threshold might be too loose**

**Or:** Multiple versions of same file

**Solutions:**
1. Reduce threshold for next scan
2. Right-click to manually adjust selections
3. Choose different delete strategy

### Files don't show duration or resolution

**Might be corrupted or unreadable**

**Check:**
- Can you open the file manually?
- Is it a supported format?
- Is there sufficient disk space?

## Deletion Issues

### "Cannot delete file" or permission error

**Causes:**
- File is open in another application
- You don't have write permissions
- File is read-only
- File is in use (especially videos)

**Solutions:**
1. **Close the file** if open in another app
   - Close media player, image viewer, etc.
   - Don't just minimize - fully close

2. **Check write permissions**
   ```
   Windows: Right-click → Properties → unceck "Read-only"
   macOS: Get Info → check if writable
   Linux: chmod u+w filename
   ```

3. **Run as Administrator (Windows)**
   - Right-click main.py → "Run as administrator"

4. **Disable antivirus temporarily**
   - Some AV software locks files
   - Test if this is the issue

### "Confirm deletion" dialog won't appear

**Causes:**
- No files are marked for deletion
- All files marked as "KEEP"
- Application issue

**Solutions:**
1. **Mark files for deletion**
   - Right-click files
   - Select "Mark as DELETE"
   - Make sure status shows "DELETE" (red)

2. **Verify marking worked**
   - Check that files are red, not green

3. **Restart and try again**
   - Close and reopen application

### Accidentally deleted files

**Deletion cannot be undone!**

**If file was important:**
1. Stop using the disk immediately
2. Use data recovery software:
   - Windows: Recuva (free)
   - macOS: EaseUS Data Recovery
   - Linux: extundelete, testdisk
3. Recovery rate depends on:
   - How long ago file was deleted
   - Disk activity since deletion
   - File size

**Prevention for next time:**
- Make backups before running
- Use "Keep Largest" if unsure
- Manually verify selections
- Start with dry runs (don't delete)

## Performance Issues

### High CPU/RAM usage

**This is normal during scanning!**

**Expected resource usage:**
- CPU: 30-100% (one core maxed)
- RAM: 100-500MB
- Network: Active during file access

**If excessive:**
1. Close other applications
2. Reduce THUMB_SIZE and THUMB_SAMPLE_POSITIONS
3. Scan smaller folders

### Application becomes unresponsive

**GUI freezes during scan**

**This is normal!** Scanning runs in background thread but:
- Heavy computation might cause brief freezes
- Should become responsive as scan progresses

**If frozen for >1 minute:**
1. Try clicking window again
2. Wait for file I/O to complete
3. Force quit if truly stuck
4. Reduce folder size or complexity

## Platform-Specific Issues

### macOS Issues

**"App is damaged and can't be opened"**
- Not a codesigned app
- Simply run: `python main.py`
- Or remove quarantine: `xattr -d com.apple.quarantine main.py`

**Window styling looks odd**
- Tkinter on macOS doesn't support all styles
- Functionality unchanged
- Consider using PyQt/PySide for better macOS integration

### Linux Issues

**Display issues on headless/remote systems**
```bash
# Set display
export DISPLAY=:0
python main.py
```

**Wayland compatibility issues**
```bash
# Force X11
QT_QPA_PLATFORM=offscreen python main.py
```

**Missing dependencies on specific distros**

Ubuntu/Debian:
```bash
sudo apt install python3-dev python3-tk libopencv-dev
```

Fedora:
```bash
sudo dnf install python3-devel python3-tkinter opencv-devel
```

### Windows Issues

**"OpenCV not found" or video processing fails**
- Reinstall OpenCV
```bash
pip install --force-reinstall opencv-python
```

**Video files won't process**
- Install FFmpeg: https://ffmpeg.org/download.html
- Add to PATH or place in same folder as main.py

**App window is tiny / scaling issues**
- Windows 10/11 scaling issue
- Open with "Change high DPI settings"
- Check "Override high DPI"

## Advanced Debugging

### Enable verbose logging

Add to main.py after imports:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check terminal for detailed errors
```bash
# Windows: Open Command Prompt with admin
python main.py 2>&1 | tee log.txt

# macOS/Linux
python3 main.py 2>&1 | tee log.txt
```

### Test individual functions

```python
# Test video hashing
from main import get_video_hashes
hashes, dark, duration = get_video_hashes("path/to/video.mp4")
print(f"Hashes: {len(hashes)}, Dark: {dark:.2%}, Duration: {duration}s")

# Test image hashing
from main import get_image_hash
hashes, resolution = get_image_hash("path/to/image.jpg")
print(f"Hashes: {len(hashes)}, Resolution: {resolution}")
```

## Getting More Help

If the above doesn't solve your issue:

1. **Check README.md** → Full documentation
2. **Check CONFIG_REFERENCE.md** → Settings explanation
3. **Search GitHub Issues** → Others might have reported
4. **Post new issue** with:
   - OS and Python version (`python --version`)
   - Error message (full text from terminal)
   - Steps to reproduce
   - Folder size and file types
   - Output of: `pip list`

## Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| Slow scan | Reduce THUMB_SAMPLE_POSITIONS |
| Too few matches | Lower threshold |
| Too many matches | Raise threshold |
| Can't delete | Close file, check permissions |
| No window appears | Wait 10 seconds, check terminal |
| Module not found | `pip install -r requirements.txt` |
| Program hangs | Ctrl+C, try smaller folder |

---

Still stuck? Double-check:
- ✅ All dependencies installed (`pip list | grep -E "(opencv\|Pillow\|ImageHash)"`)
- ✅ Correct Python version (3.7+)
- ✅ Folder path is valid and readable
- ✅ Sufficient disk space
- ✅ No antivirus blocking
