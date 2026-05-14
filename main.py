"""
Media Duplicate Finder - Videos & Images

A desktop application that recursively scans folders for duplicate media files
(videos and images) using perceptual hashing algorithms combined with file metadata.

Features:
    - Detect duplicate videos using thumbnail hashing and duration matching
    - Detect duplicate images using perceptual hash matching
    - Interactive GUI with file preview and deletion options
    - Customizable similarity thresholds
    - Multiple deletion strategies (keep largest, smallest, newest, oldest)
    - Non-destructive marking before deletion

Author: Media Duplicate Finder
License: MIT
"""

import os
import sys
import cv2
import imagehash
import threading
from PIL import Image
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Suppress OpenCV/FFmpeg console spam
os.environ["OPENCV_LOG_LEVEL"] = "SILENT"

# ─────────────────────────────────────────────
# CONFIG - Application Configuration Constants
# ─────────────────────────────────────────────
# Defines supported file extensions, hashing thresholds, and processing parameters
# Supported file extensions for detection
VIDEO_EXTENSIONS = {
    ".mp4", ".mkv", ".avi", ".mov", ".wmv",
    ".flv", ".webm", ".m4v", ".mpg", ".mpeg",
    ".3gp", ".ts", ".mts", ".m2ts", ".vob",
}
IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".gif",
    ".tiff", ".tif", ".webp", ".heic", ".heif",
}

# Hash similarity thresholds - lower values = stricter matching
HASH_SIMILARITY_THRESHOLD = 8      # For videos (0=exact, 20=loose)
IMAGE_HASH_THRESHOLD      = 6      # For images (0=exact, 20=loose)

# Video processing parameters
THUMB_SAMPLE_POSITIONS    = [0.05, 0.20, 0.40, 0.60, 0.80]  # Frame positions to sample (5 frames)
THUMB_SIZE                = (64, 64)  # Resize frames to this size for hashing
DARK_FRAME_BRIGHTNESS     = 15     # Threshold to detect dark/blank frames
DARK_FRAME_MIN_RATIO      = 0.6    # If 60%+ frames are dark, use duration-only matching
DURATION_TOLERANCE_SEC    = 2      # Acceptable duration difference for videos


# ─────────────────────────────────────────────
# SHARED HELPERS - Common utility functions
# ─────────────────────────────────────────────

def hash_similarity(h1: list, h2: list) -> float:
    """
    Calculate similarity between two perceptual hashes.
    
    Uses Hamming distance to compare hashes. Lower values indicate more similar images.
    
    Args:
        h1: First perceptual hash
        h2: Second perceptual hash
        
    Returns:
        float: Similarity score (lower = more similar). Returns inf if hashes are invalid.
    """
    if not h1 or not h2 or len(h1) != len(h2):
        return float("inf")
    return sum(a - b for a, b in zip(h1, h2)) / len(h1)


def get_file_info(path: str) -> dict:
    """
    Extract basic file information including size, modification time, and metadata.
    
    Args:
        path: Full file path
        
    Returns:
        dict: File metadata including:
            - path: File path
            - size: File size in bytes
            - mtime: Modification timestamp
            - mtime_str: Formatted modification time
            - kind: Media type (video/image, initially empty)
            - hashes: List of perceptual hashes (initially empty)
            - dark_ratio: Ratio of dark frames (videos only)
            - duration: Video duration in seconds
            - resolution: Image resolution as (width, height) tuple
    """
    stat = os.stat(path)
    return {
        "path":       path,
        "size":       stat.st_size,
        "mtime":      stat.st_mtime,
        "mtime_str":  datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
        "kind":       "",
        "hashes":     [],
        "dark_ratio": 0.0,
        "duration":   0.0,
        "resolution": (0, 0),
    }


def format_size(size_bytes: int) -> str:
    """
    Convert byte size to human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        str: Formatted size string (e.g., "1.5 MB", "2.3 GB")
    """
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def format_duration(seconds: float) -> str:
    """
    Convert seconds to HH:MM:SS format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        str: Formatted duration string (e.g., "1:23:45" or "5:30")
    """
    seconds = int(round(seconds))
    h, rem = divmod(seconds, 3600)
    m, s   = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def format_resolution(res: tuple) -> str:
    """
    Convert resolution tuple to string format.
    
    Args:
        res: Tuple of (width, height)
        
    Returns:
        str: Formatted resolution string (e.g., "1920x1080") or empty string if invalid
    """
    w, h = res
    return f"{w}x{h}" if w and h else ""


# ─────────────────────────────────────────────
# VIDEO LOGIC - Video processing and comparison
# ─────────────────────────────────────────────

def get_video_hashes(path: str) -> tuple:
    """
    Extract perceptual hashes and metadata from a video file.
    
    Samples frames at multiple positions throughout the video and generates
    perceptual hashes. Tracks dark frames to detect blank/credits sections.
    
    Args:
        path: Full path to video file
        
    Returns:
        tuple: (hashes_list, dark_frame_ratio, duration_seconds)
            - hashes_list: List of perceptual hashes from sampled frames
            - dark_frame_ratio: Fraction of sampled frames that are dark (0.0-1.0)
            - duration_seconds: Total video duration in seconds
    """
    hashes, dark_count, duration_sec = [], 0, 0.0
    try:
        cap   = cv2.VideoCapture(path)
        if not cap.isOpened():
            return [], 1.0, 0.0
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps   = cap.get(cv2.CAP_PROP_FPS) or 1
        duration_sec = total / fps if total > 0 else 0.0
        if total <= 0:
            cap.release()
            return [], 1.0, 0.0
        for pos_ratio in THUMB_SAMPLE_POSITIONS:
            cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, int(total * pos_ratio)))
            ret, frame = cap.read()
            if ret and frame is not None:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if float(gray.mean()) < DARK_FRAME_BRIGHTNESS:
                    dark_count += 1
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                hashes.append(imagehash.phash(img.resize(THUMB_SIZE, Image.LANCZOS)))
        cap.release()
    except Exception:
        pass
    dark_ratio = dark_count / len(THUMB_SAMPLE_POSITIONS)
    return hashes, dark_ratio, duration_sec


def are_video_duplicates(a: dict, b: dict) -> bool:
    """
    Determine if two videos are duplicates using dual-strategy comparison.
    
    Strategy:
    1. If both videos have high dark frame ratios (likely credits/blank sections),
       compare using duration only
    2. Otherwise, use perceptual hash similarity + duration tolerance
    
    Args:
        a: File info dict for first video
        b: File info dict for second video
        
    Returns:
        bool: True if videos are considered duplicates
    """
    a_dark    = a["dark_ratio"] >= DARK_FRAME_MIN_RATIO
    b_dark    = b["dark_ratio"] >= DARK_FRAME_MIN_RATIO
    dur_match = abs(a["duration"] - b["duration"]) <= DURATION_TOLERANCE_SEC
    if a_dark and b_dark:
        return dur_match
    sim = hash_similarity(a["hashes"], b["hashes"])
    return sim <= HASH_SIMILARITY_THRESHOLD and dur_match


# ─────────────────────────────────────────────
# IMAGE LOGIC - Image processing and comparison
# ─────────────────────────────────────────────

def get_image_hash(path: str) -> tuple:
    """
    Extract perceptual hash and resolution from an image file.
    
    Args:
        path: Full path to image file
        
    Returns:
        tuple: (hashes_list, resolution_tuple)
            - hashes_list: Single-element list with perceptual hash
            - resolution_tuple: (width, height) in pixels
    """
    try:
        img = Image.open(path)
        resolution = img.size
        h = imagehash.phash(img.convert("RGB").resize(THUMB_SIZE, Image.LANCZOS))
        return [h], resolution
    except Exception:
        return [], (0, 0)


def are_image_duplicates(a: dict, b: dict) -> bool:
    """
    Determine if two images are duplicates using perceptual hash similarity.
    
    Args:
        a: File info dict for first image
        b: File info dict for second image
        
    Returns:
        bool: True if images are considered duplicates (hash similarity <= threshold)
    """
    sim = hash_similarity(a["hashes"], b["hashes"])
    return sim <= IMAGE_HASH_THRESHOLD


# ─────────────────────────────────────────────
# SCAN & FIND - Folder scanning and duplicate detection
# ─────────────────────────────────────────────

def scan_folder(folder: str, scan_videos: bool, scan_images: bool,
                progress_cb=None) -> list:
    """
    Recursively scan a folder for media files and extract their hashes.
    
    Args:
        folder: Root folder path to scan
        scan_videos: Whether to scan for video files
        scan_images: Whether to scan for image files
        progress_cb: Optional callback function(current, total, current_filename)
                    for progress updates
        
    Returns:
        list: List of file info dicts with extracted hashes and metadata
    """
    all_paths = []
    for root, dirs, files in os.walk(folder):
        dirs[:] = sorted(dirs)
        for f in sorted(files):
            ext = Path(f).suffix.lower()
            if (scan_videos and ext in VIDEO_EXTENSIONS) or \
               (scan_images and ext in IMAGE_EXTENSIONS):
                all_paths.append(os.path.join(root, f))

    items, total = [], len(all_paths)
    for i, path in enumerate(all_paths):
        if progress_cb:
            progress_cb(i + 1, total, path)
        ext  = Path(path).suffix.lower()
        info = get_file_info(path)
        if ext in VIDEO_EXTENSIONS:
            info["kind"] = "video"
            h, dr, dur   = get_video_hashes(path)
            info["hashes"]     = h
            info["dark_ratio"] = dr
            info["duration"]   = dur
            if h or dur > 0:
                items.append(info)
        else:
            info["kind"] = "image"
            h, res = get_image_hash(path)
            info["hashes"]     = h
            info["resolution"] = res
            if h:
                items.append(info)

    return items


def find_duplicates(items: list) -> list:
    """
    Identify and group duplicate files from a list of scanned items.
    
    Uses a greedy clustering approach that groups media files by type, then
    compares each file with all others to find duplicates. Once a file is
    assigned to a duplicate group, it's marked as visited.
    
    Args:
        items: List of file info dicts from scan_folder()
        
    Returns:
        list: List of duplicate groups. Each group is a list of 2+ file info dicts
              that are duplicates of each other. Single files are excluded.
    """
    videos = [x for x in items if x["kind"] == "video"]
    images = [x for x in items if x["kind"] == "image"]
    groups = []

    for pool, dup_fn in [(videos, are_video_duplicates),
                         (images, are_image_duplicates)]:
        n       = len(pool)
        visited = [False] * n
        for i in range(n):
            if visited[i]:
                continue
            group = [pool[i]]
            visited[i] = True
            for j in range(i + 1, n):
                if not visited[j] and dup_fn(pool[i], pool[j]):
                    group.append(pool[j])
                    visited[j] = True
            if len(group) > 1:
                groups.append(group)

    return groups


def choose_keeper(group: list, strategy: str) -> dict:
    """
    Select which file to keep in a duplicate group based on the specified strategy.
    
    Strategies:
        - keep_smallest: Prefer smaller files, use newer as tiebreaker
        - keep_largest: Prefer larger files, use newer as tiebreaker
        - keep_newest: Prefer newer (by modification time)
        - keep_oldest: Prefer older (by modification time)
    
    Args:
        group: List of duplicate file info dicts
        strategy: One of ("keep_smallest", "keep_largest", "keep_newest", "keep_oldest")
        
    Returns:
        dict: The selected file info dict to keep
    """
    if strategy == "keep_smallest":
        key = lambda v: (v["size"],  -v["mtime"])
    elif strategy == "keep_largest":
        key = lambda v: (-v["size"], -v["mtime"])
    elif strategy == "keep_newest":
        key = lambda v: -v["mtime"]
    elif strategy == "keep_oldest":
        key = lambda v: v["mtime"]
    else:
        key = lambda v: -v["mtime"]
    return sorted(group, key=key)[0]


# ─────────────────────────────────────────────
# GUI
# ─────────────────────────────────────────────

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Media Duplicate Finder")
        self.geometry("980x720")
        self.minsize(820, 560)
        self.configure(bg="#1e1e2e")
        self.resizable(True, True)

        self.scan_folder_var  = tk.StringVar()
        self.strategy_var     = tk.StringVar(value="keep_largest")
        self.threshold_var    = tk.IntVar(value=HASH_SIMILARITY_THRESHOLD)
        self.scan_videos_var  = tk.BooleanVar(value=True)
        self.scan_images_var  = tk.BooleanVar(value=True)
        self.duplicate_groups: list = []

        self._build_ui()
        self._style()

    def _style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        bg, fg, sel = "#1e1e2e", "#cdd6f4", "#313244"
        accent, red = "#89b4fa", "#f38ba8"
        s.configure("TFrame",       background=bg)
        s.configure("TLabel",       background=bg, foreground=fg, font=("Segoe UI", 10))
        s.configure("Header.TLabel",background=bg, foreground=accent,
                    font=("Segoe UI", 13, "bold"))
        s.configure("TButton",      background=sel, foreground=fg,
                    font=("Segoe UI", 10), relief="flat", padding=6)
        s.map("TButton",
              background=[("active", accent)], foreground=[("active", "#1e1e2e")])
        s.configure("Accent.TButton", background=accent, foreground="#1e1e2e",
                    font=("Segoe UI", 10, "bold"))
        s.map("Accent.TButton", background=[("active", "#74c7ec")])
        s.configure("Danger.TButton", background=red, foreground="#1e1e2e",
                    font=("Segoe UI", 10, "bold"))
        s.map("Danger.TButton", background=[("active", "#eba0ac")])
        s.configure("TEntry",       fieldbackground=sel, foreground=fg,
                    insertcolor=fg, font=("Segoe UI", 10))
        s.configure("TProgressbar", troughcolor=sel, background=accent)
        s.configure("Treeview",     background=sel, foreground=fg,
                    fieldbackground=sel, font=("Segoe UI", 9), rowheight=24)
        s.configure("Treeview.Heading", background="#181825", foreground=accent,
                    font=("Segoe UI", 9, "bold"))
        s.map("Treeview",
              background=[("selected", accent)], foreground=[("selected", "#1e1e2e")])
        s.configure("TRadiobutton",  background=bg, foreground=fg, font=("Segoe UI", 10))
        s.configure("TCheckbutton",  background=bg, foreground=fg, font=("Segoe UI", 10))
        s.configure("TScale",        background=bg, troughcolor=sel)
        s.configure("TLabelframe",       background=bg, foreground=fg)
        s.configure("TLabelframe.Label", background=bg, foreground=accent,
                    font=("Segoe UI", 10, "bold"))

    def _build_ui(self):
        pad = {"padx": 16, "pady": 8}

        # Header
        top = ttk.Frame(self)
        top.pack(fill="x", **pad)
        ttk.Label(top, text="Media Duplicate Finder  (Videos + Images)",
                  style="Header.TLabel").pack(side="left")

        # Folder
        ff = ttk.LabelFrame(self, text="  Folder to scan")
        ff.pack(fill="x", padx=16, pady=(0, 6))
        ttk.Entry(ff, textvariable=self.scan_folder_var, width=70).pack(
            side="left", padx=8, pady=8, fill="x", expand=True)
        ttk.Button(ff, text="Browse...", command=self._browse_folder).pack(
            side="left", padx=(0, 8), pady=8)

        # Options
        opt = ttk.LabelFrame(self, text="  Options")
        opt.pack(fill="x", padx=16, pady=(0, 6))

        # Scan type
        scan_type = ttk.Frame(opt)
        scan_type.pack(side="left", padx=12, pady=6)
        ttk.Label(scan_type, text="Scan for:").pack(anchor="w")
        ttk.Checkbutton(scan_type, text="Videos",
                        variable=self.scan_videos_var).pack(anchor="w")
        ttk.Checkbutton(scan_type, text="Images",
                        variable=self.scan_images_var).pack(anchor="w")

        ttk.Separator(opt, orient="vertical").pack(side="left", fill="y", padx=8, pady=6)

        # Strategy
        strat = ttk.Frame(opt)
        strat.pack(side="left", padx=4, pady=6)
        ttk.Label(strat, text="Keep:").pack(anchor="w")
        for label, value in [
            ("Largest file",  "keep_largest"),
            ("Smallest file", "keep_smallest"),
            ("Newest file",   "keep_newest"),
            ("Oldest file",   "keep_oldest"),
        ]:
            ttk.Radiobutton(strat, text=label, variable=self.strategy_var,
                            value=value).pack(anchor="w")

        ttk.Separator(opt, orient="vertical").pack(side="left", fill="y", padx=8, pady=6)

        # Threshold
        thresh = ttk.Frame(opt)
        thresh.pack(side="left", padx=4, pady=6, fill="x", expand=True)
        ttk.Label(thresh, text="Similarity threshold (lower = stricter):").pack(anchor="w")
        trow = ttk.Frame(thresh)
        trow.pack(fill="x")
        self._thresh_lbl = ttk.Label(trow, text=str(self.threshold_var.get()),
                                     width=3, font=("Segoe UI", 11, "bold"))
        self._thresh_lbl.pack(side="right", padx=4)
        ttk.Scale(trow, from_=0, to=20, orient="horizontal",
                  variable=self.threshold_var,
                  command=lambda v: self._thresh_lbl.config(
                      text=str(int(float(v))))).pack(fill="x", expand=True)
        ttk.Label(thresh, text="0 = exact only   |   8 = similar   |   20 = loose",
                  foreground="#6c7086", font=("Segoe UI", 8)).pack(anchor="w")

        # Buttons
        btn_row = ttk.Frame(self)
        btn_row.pack(fill="x", padx=16, pady=(0, 6))
        ttk.Button(btn_row, text="Start Scan", style="Accent.TButton",
                   command=self._start_scan).pack(side="left", padx=(0, 8))
        self._delete_btn = ttk.Button(btn_row, text="Delete Marked",
                                      style="Danger.TButton",
                                      command=self._confirm_delete, state="disabled")
        self._delete_btn.pack(side="left", padx=(0, 8))
        self._status_lbl = ttk.Label(btn_row, text="", foreground="#a6e3a1")
        self._status_lbl.pack(side="left", padx=8)

        # Progress
        self._progress_var = tk.DoubleVar()
        ttk.Progressbar(self, variable=self._progress_var,
                        maximum=100, mode="determinate").pack(
            fill="x", padx=16, pady=(0, 4))
        self._progress_lbl = ttk.Label(self, text="", foreground="#6c7086",
                                       font=("Segoe UI", 8))
        self._progress_lbl.pack(anchor="w", padx=16)

        # Tree
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=16, pady=(4, 16))

        cols = ("keep", "type", "path", "size", "extra", "modified")
        self._tree = ttk.Treeview(tree_frame, columns=cols, show="headings",
                                  selectmode="extended")
        self._tree.heading("keep",     text="Action")
        self._tree.heading("type",     text="Type")
        self._tree.heading("path",     text="File path")
        self._tree.heading("size",     text="Size")
        self._tree.heading("extra",    text="Duration / Resolution")
        self._tree.heading("modified", text="Modified")
        self._tree.column("keep",     width=80,  anchor="center", stretch=False)
        self._tree.column("type",     width=60,  anchor="center", stretch=False)
        self._tree.column("path",     width=430, anchor="w")
        self._tree.column("size",     width=75,  anchor="e",      stretch=False)
        self._tree.column("extra",    width=130, anchor="center", stretch=False)
        self._tree.column("modified", width=115, anchor="center", stretch=False)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical",   command=self._tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self._tree.xview)
        self._tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right",  fill="y")
        hsb.pack(side="bottom", fill="x")
        self._tree.pack(fill="both", expand=True)

        self._tree.tag_configure("keep",   foreground="#a6e3a1")
        self._tree.tag_configure("delete", foreground="#f38ba8")
        self._tree.tag_configure("group",  background="#313244", foreground="#89b4fa")

        # Right-click menu
        self._ctx = tk.Menu(self, tearoff=0, bg="#313244", fg="#cdd6f4",
                            activebackground="#89b4fa", activeforeground="#1e1e2e")
        self._ctx.add_command(label="Mark as KEEP",
                              command=lambda: self._toggle_item("keep"))
        self._ctx.add_command(label="Mark as DELETE",
                              command=lambda: self._toggle_item("delete"))
        self._tree.bind("<Button-3>", self._show_ctx)
        self._tree.bind("<Double-1>", self._open_file)

    def _browse_folder(self):
        path = filedialog.askdirectory(title="Select folder to scan")
        if path:
            self.scan_folder_var.set(path)

    def _start_scan(self):
        folder = self.scan_folder_var.get().strip()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder first.")
            return
        if not self.scan_videos_var.get() and not self.scan_images_var.get():
            messagebox.showerror("Error", "Select at least Videos or Images to scan.")
            return
        self._clear_results()
        self._delete_btn.config(state="disabled")
        self._status_lbl.config(text="Scanning...", foreground="#89b4fa")
        threading.Thread(target=self._scan_worker, args=(folder,), daemon=True).start()

    def _scan_worker(self, folder):
        global HASH_SIMILARITY_THRESHOLD, IMAGE_HASH_THRESHOLD
        HASH_SIMILARITY_THRESHOLD = self.threshold_var.get()
        IMAGE_HASH_THRESHOLD      = self.threshold_var.get()

        def progress(current, total, path):
            pct = (current / total) * 100 if total else 0
            self.after(0, self._update_progress, pct, current, total,
                       os.path.basename(path))
        try:
            items = scan_folder(folder,
                                scan_videos=self.scan_videos_var.get(),
                                scan_images=self.scan_images_var.get(),
                                progress_cb=progress)
            n_vid = sum(1 for x in items if x["kind"] == "video")
            n_img = sum(1 for x in items if x["kind"] == "image")
            self.after(0, self._progress_lbl.config,
                       {"text": f"Found {n_vid} videos, {n_img} images. Comparing..."})
            groups = find_duplicates(items)
            self.after(0, self._show_results, groups)
        except Exception as e:
            self.after(0, messagebox.showerror, "Scan error", str(e))
            self.after(0, self._status_lbl.config,
                       {"text": "Error during scan.", "foreground": "#f38ba8"})

    def _update_progress(self, pct, current, total, filename):
        self._progress_var.set(pct)
        self._progress_lbl.config(text=f"[{current}/{total}]  {filename}")

    def _clear_results(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
        self._progress_var.set(0)
        self._progress_lbl.config(text="")
        self._status_lbl.config(text="")
        self.duplicate_groups = []

    def _show_results(self, groups: list):
        self.duplicate_groups = groups
        strategy = self.strategy_var.get()

        if not groups:
            self._status_lbl.config(text="No duplicates found!", foreground="#a6e3a1")
            self._progress_lbl.config(text="")
            return

        total_delete, total_saved = 0, 0

        for g_idx, group in enumerate(groups):
            keeper = choose_keeper(group, strategy)
            kind   = group[0]["kind"]

            if kind == "video":
                any_dark = any(v["dark_ratio"] >= DARK_FRAME_MIN_RATIO for v in group)
                method   = "duration fallback (dark)" if any_dark else "thumbnail hash + duration"
                icon     = "[VIDEO]"
            else:
                method = "perceptual hash"
                icon   = "[IMAGE]"

            g_label = f"  -- {icon} Group {g_idx + 1}  ({len(group)} files)  [{method}] --"
            self._tree.insert("", "end", iid=f"group_{g_idx}",
                              values=("", "", g_label, "", "", ""), tags=("group",))

            for item in group:
                is_keep   = item["path"] == keeper["path"]
                action    = "KEEP"   if is_keep else "DELETE"
                tag       = "keep"   if is_keep else "delete"
                type_lbl  = "Video"  if item["kind"] == "video" else "Image"

                if item["kind"] == "video":
                    dark_flag    = " [dark]" if item["dark_ratio"] >= DARK_FRAME_MIN_RATIO else ""
                    extra        = format_duration(item["duration"])
                    display_path = item["path"] + dark_flag
                else:
                    extra        = format_resolution(item["resolution"])
                    display_path = item["path"]

                iid = f"item_{g_idx}_{item['path']}"
                self._tree.insert("", "end", iid=iid, values=(
                    action, type_lbl, display_path,
                    format_size(item["size"]), extra, item["mtime_str"],
                ), tags=(tag,))

                if not is_keep:
                    total_delete += 1
                    total_saved  += item["size"]

        self._delete_btn.config(state="normal")
        self._status_lbl.config(
            text=f"Found {len(groups)} duplicate group(s). "
                 f"{total_delete} file(s) marked for deletion "
                 f"({format_size(total_saved)} saved).",
            foreground="#fab387")
        self._progress_var.set(100)
        self._progress_lbl.config(text="Scan complete.")

    def _show_ctx(self, event):
        item = self._tree.identify_row(event.y)
        if item and not item.startswith("group_"):
            self._tree.selection_set(item)
            self._ctx.post(event.x_root, event.y_root)

    def _toggle_item(self, action: str):
        for item in self._tree.selection():
            vals = list(self._tree.item(item, "values"))
            if action == "keep":
                vals[0] = "KEEP"
                self._tree.item(item, values=vals, tags=("keep",))
            else:
                vals[0] = "DELETE"
                self._tree.item(item, values=vals, tags=("delete",))

    def _open_file(self, event):
        item = self._tree.identify_row(event.y)
        if item and not item.startswith("group_"):
            path = self._tree.item(item, "values")[2]
            path = path.replace(" [dark]", "")
            if os.path.exists(path):
                if sys.platform == "win32":
                    os.startfile(path)
                else:
                    os.system(f'xdg-open "{path}" &')

    def _confirm_delete(self):
        to_delete = []
        for item in self._tree.get_children():
            if item.startswith("group_"):
                continue
            vals = self._tree.item(item, "values")
            if vals and vals[0] == "DELETE":
                path = vals[2].replace(" [dark]", "")
                to_delete.append(path)

        if not to_delete:
            messagebox.showinfo("Nothing to delete", "No files are marked for deletion.")
            return

        total_size = sum(os.path.getsize(p) for p in to_delete if os.path.exists(p))
        if not messagebox.askyesno(
            "Confirm deletion",
            f"Permanently delete {len(to_delete)} file(s)?\n"
            f"Space freed: {format_size(total_size)}\n\n"
            f"This CANNOT be undone.",
            icon="warning"
        ):
            return

        errors, deleted = [], 0
        for path in to_delete:
            try:
                os.remove(path)
                deleted += 1
            except Exception as e:
                errors.append(f"{path}: {e}")

        if errors:
            messagebox.showerror("Errors", "\n".join(errors[:10]))
        messagebox.showinfo("Done",
                            f"{deleted} file(s) deleted.\n"
                            f"{format_size(total_size)} freed.")
        self._start_scan()


if __name__ == "__main__":
    App().mainloop()