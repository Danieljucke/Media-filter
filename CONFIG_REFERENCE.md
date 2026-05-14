"""
Configuration Reference for Media Duplicate Finder

This file documents all configurable parameters in main.py.
Copy and modify these constants in main.py to customize behavior.
"""

# ═══════════════════════════════════════════════════════════════════════
# SIMILARITY THRESHOLDS
# ═══════════════════════════════════════════════════════════════════════
# Lower values = stricter matching (fewer false positives)
# Higher values = looser matching (more potential duplicates)

HASH_SIMILARITY_THRESHOLD = 8      # Videos: 0-20 range (default: 8)
IMAGE_HASH_THRESHOLD = 6            # Images: 0-20 range (default: 6)

# Threshold Guidelines:
# 0-2   = Exact or nearly identical (very strict)
# 3-6   = High similarity (recommended for critical files)
# 7-10  = Balanced (default, good balance of accuracy/recall)
# 11-15 = Loose (finds more variations, higher false positive rate)
# 16-20 = Very loose (very permissive, check results carefully)


# ═══════════════════════════════════════════════════════════════════════
# VIDEO PROCESSING PARAMETERS
# ═══════════════════════════════════════════════════════════════════════

# Frame sampling strategy: sample video at these relative positions
# Values: 0.0 (start) to 1.0 (end)
# Example: [0.25, 0.50, 0.75] samples 3 frames at 25%, 50%, 75%
THUMB_SAMPLE_POSITIONS = [0.05, 0.20, 0.40, 0.60, 0.80]  # 5 samples (default)

# Resolution for perceptual hash computation
# Higher = more detail but slower
# Lower = faster but less accurate
# Recommended: 64x64 or 32x32
THUMB_SIZE = (64, 64)

# Brightness threshold for dark frame detection
# Frames with average pixel value < this are considered "dark"
# Used to detect intros, credits, or black frames
# Range: 0-255
DARK_FRAME_BRIGHTNESS = 15

# If this ratio of sampled frames are dark, use duration-only matching
# Example: 0.6 = if 60% of frames are dark, match by duration only
# This handles videos with black intros/credits/encoding artifacts
DARK_FRAME_MIN_RATIO = 0.6

# Acceptable duration difference between videos (in seconds)
# Videos with durations within this range are considered compatible
DURATION_TOLERANCE_SEC = 2


# ═══════════════════════════════════════════════════════════════════════
# FILE EXTENSIONS
# ═══════════════════════════════════════════════════════════════════════
# Add or remove extensions to customize detection

VIDEO_EXTENSIONS = {
    # Common formats
    ".mp4", ".mkv", ".avi", ".mov", ".wmv",
    # Streaming/web formats
    ".flv", ".webm", ".m4v", 
    # MPEG family
    ".mpg", ".mpeg",
    # Mobile/device formats
    ".3gp", 
    # Broadcast formats
    ".ts", ".mts", ".m2ts", 
    # DVD
    ".vob",
}

IMAGE_EXTENSIONS = {
    # Standard raster formats
    ".jpg", ".jpeg", ".png", ".bmp", ".gif",
    # TIFF formats
    ".tiff", ".tif",
    # Modern formats
    ".webp",
    # Apple formats
    ".heic", ".heif",
}


# ═══════════════════════════════════════════════════════════════════════
# ADVANCED TUNING
# ═══════════════════════════════════════════════════════════════════════

# Examples of advanced configurations for specific use cases:

# ─────────────────────────────────────────────────────────────────────
# STRICT MODE: Minimize false positives
# ─────────────────────────────────────────────────────────────────────
STRICT_VIDEO_THRESHOLD = 4
STRICT_IMAGE_THRESHOLD = 3
STRICT_DURATION_TOLERANCE = 1
# Use case: Verifying actual duplicates, archival quality control


# ─────────────────────────────────────────────────────────────────────
# LOOSE MODE: Maximum duplicate detection
# ─────────────────────────────────────────────────────────────────────
LOOSE_VIDEO_THRESHOLD = 12
LOOSE_IMAGE_THRESHOLD = 10
LOOSE_DURATION_TOLERANCE = 5
# Use case: Finding all variations, aggressive cleanup


# ─────────────────────────────────────────────────────────────────────
# VIDEO LIBRARY MODE: Optimized for TV shows/movies
# ─────────────────────────────────────────────────────────────────────
# Sample more frames for better accuracy
VIDEO_LIBRARY_SAMPLES = [0.02, 0.1, 0.25, 0.50, 0.75, 0.90, 0.98]  # 7 samples
VIDEO_LIBRARY_THRESHOLD = 5
VIDEO_LIBRARY_DURATION_TOLERANCE = 3
# Use case: Large video collections with similar content


# ─────────────────────────────────────────────────────────────────────
# PHOTO LIBRARY MODE: Optimized for photographs
# ─────────────────────────────────────────────────────────────────────
# Photos are more sensitive to minor differences
PHOTO_HASH_THRESHOLD = 5
PHOTO_THUMB_SIZE = (128, 128)  # Higher resolution for better accuracy
# Use case: Photo collections with slight variations


# ═══════════════════════════════════════════════════════════════════════
# PERFORMANCE OPTIMIZATION
# ═══════════════════════════════════════════════════════════════════════

# For large libraries (1000+ files), consider:
# 1. Reduce sample positions: [0.25, 0.75] instead of [0.05, 0.20, ...]
# 2. Reduce hash size: (32, 32) instead of (64, 64)
# 3. Increase threshold: more forgiving matching
# 4. Scan in batches: process folder by folder

# For network drives or slow storage:
# - Copy files locally first
# - Increase dark frame threshold for faster processing
# - Use smaller sample sets


# ═══════════════════════════════════════════════════════════════════════
# UI CUSTOMIZATION
# ═══════════════════════════════════════════════════════════════════════

# Color scheme (Catppuccin palette)
COLOR_BG = "#1e1e2e"
COLOR_FG = "#cdd6f4"
COLOR_ACCENT = "#89b4fa"
COLOR_ERROR = "#f38ba8"
COLOR_SUCCESS = "#a6e3a1"

# Window size
DEFAULT_WIDTH = 980
DEFAULT_HEIGHT = 720
MIN_WIDTH = 820
MIN_HEIGHT = 560


# ═══════════════════════════════════════════════════════════════════════
# USAGE EXAMPLES
# ═══════════════════════════════════════════════════════════════════════

"""
Example 1: Strict photo duplicate detection
    HASH_SIMILARITY_THRESHOLD = 3  # Very strict
    IMAGE_HASH_THRESHOLD = 2
    DURATION_TOLERANCE_SEC = 1

Example 2: Video cleanup with variants allowed
    HASH_SIMILARITY_THRESHOLD = 12  # Loose
    DURATION_TOLERANCE_SEC = 5

Example 3: Performance mode (large library)
    THUMB_SAMPLE_POSITIONS = [0.25, 0.50, 0.75]  # 3 samples
    THUMB_SIZE = (32, 32)  # Smaller
    HASH_SIMILARITY_THRESHOLD = 10  # More forgiving

Example 4: Archive verification (no false positives)
    HASH_SIMILARITY_THRESHOLD = 2
    IMAGE_HASH_THRESHOLD = 2
    DURATION_TOLERANCE_SEC = 1
"""
