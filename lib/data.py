from __future__ import annotations
import json
from typing import Any, Dict

LOCKER_PATH = "your_projects/locker.json"

DEFAULT_PROFILE = {
    "name": "Lance",
    "tagline": "Manufacturing & Mechanical Engineering Portfolio",
    "chips": ["CNC • Fixtures • DFM", "SolidWorks • GD&T • CAM"],
    "links": [
        {"label":"Resume (PDF)", "url":"#"},
        {"label":"Email", "url":"mailto:lance@example.com"},
        {"label":"LinkedIn", "url":"https://www.linkedin.com/"},
        {"label":"GitHub", "url":"https://github.com/"},
    ]
}

DEFAULT_DATA = {
    "profile": DEFAULT_PROFILE,
    "projects": [
        {
            "id": "example_project",
            "title": "CNC Fixture Design",
            "tagline": "Workholding solution for aluminum machining",
            "model": "your_projects/example_project.glb",
            "images": ["your_projects/example_image.png"],
            "links": [
                {"label":"Process Doc (PDF)", "url":"#"},
                {"label":"Manufacturing Plan", "url":"#"}
            ],
            "facts": [
                ["Role","Manufacturing Engineer"],
                ["Highlights","Doweling scheme, quick swap jaws, op1→op2 repeatability"]
            ],
            "tags": ["Fixture", "CNC"],
            "summary": "Designed, machined, and validated a modular fixture for small-batch aluminum parts with a focus on rigidity, chip evacuation, and rapid changeover."
        }
    ]
}

def load_data() -> Dict[str, Any]:
    try:
        # stlite mounts locker.json into the in-memory FS at this path via index.html
        with open(LOCKER_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = DEFAULT_DATA

    # normalize
    data.setdefault("profile", DEFAULT_PROFILE)
    data.setdefault("projects", [])
    for p in data["projects"]:
        p.setdefault("id", p.get("title","").lower().replace(" ","_"))
        p.setdefault("images", [])
        p.setdefault("links", [])
        p.setdefault("facts", [])
        p.setdefault("tags", [])
        p.setdefault("summary", "")
    return data
