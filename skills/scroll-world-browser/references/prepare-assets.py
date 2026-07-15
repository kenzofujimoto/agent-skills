#!/usr/bin/env python3
"""Prepare browser-generated assets for the scroll-world skill.

This script does not call any AI provider. It creates prompts, validates manually downloaded
files, extracts boundary frames, encodes site assets, and emits the scrub-engine config.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def load_project(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Project file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc

    sections = data.get("sections")
    if not isinstance(sections, list) or not sections:
        raise SystemExit("project.json must contain a non-empty sections array")
    ids = [s.get("id") for s in sections]
    if any(not isinstance(value, str) or not value for value in ids):
        raise SystemExit("Every section must have a non-empty string id")
    if len(ids) != len(set(ids)):
        raise SystemExit("Section ids must be unique")
    architecture = data.get("architecture", "extend")
    if architecture not in {"extend", "bridge", "crossfade"}:
        raise SystemExit("architecture must be extend, bridge, or crossfade")
    return data


def run(cmd: list[str]) -> None:
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError as exc:
        raise SystemExit(f"Required executable not found: {cmd[0]}") from exc
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f"Command failed ({exc.returncode}): {' '.join(cmd)}") from exc


def ensure_dirs(work: Path) -> dict[str, Path]:
    paths = {
        "prompts": work / "prompts",
        "source": work / "source",
        "frames": work / "frames",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def style_preamble(project: dict[str, Any]) -> str:
    style = project.get("style")
    if isinstance(style, str) and style.strip():
        return style.strip()
    brand = project.get("brand", {})
    palette = ", ".join(brand.get("palette", []))
    bg = brand.get("background", "#F5EDE0")
    return (
        f"Isometric low-poly 3D diorama floating as a small rounded island on a plain "
        f"solid {bg} background with a soft contact shadow beneath it. Soft matte clay "
        f"render, rounded toy-model shapes, gentle warm studio lighting, soft long shadows "
        f"and a tilt-shift miniature look. Cohesive palette of {palette}. Highly detailed, "
        f"centered composition, absolutely no text, letters, numbers or logos."
    )


def prompt_files(project: dict[str, Any], work: Path) -> None:
    paths = ensure_dirs(work)
    prompts = paths["prompts"]
    brand = project.get("brand", {})
    subject = brand.get("subject", "the requested brand journey")
    style = style_preamble(project)
    anchor_subject = project.get("anchor_subject", project["sections"][0].get("subject", subject))

    anchor = f"""{style}
Create the visual style anchor for one connected world about {subject}. Show {anchor_subject}.
This image defines the camera angle, materials, lighting, palette and level of detail for
every later scene. Landscape 3:2, centered with comfortable margins.
"""
    (prompts / "style-anchor.txt").write_text(anchor, encoding="utf-8")

    sections = project["sections"]
    architecture = project.get("architecture", "extend")
    for index, section in enumerate(sections):
        sid = section["id"]
        still = f"""Use the attached approved style-anchor image as the authoritative reference.
Preserve its camera angle, lens feel, materials, lighting, palette, background and detail density.

{style}

Create a new scene in that exact same world.
Scene: {section.get('subject', sid)}
Focal point: {section.get('focal_point', 'the central subject')}
Keep the focal point horizontally centered with headroom for a 16:9 video crop and a narrow
portrait center crop. Change only the subject matter required for this scene. No text,
letters, numbers, logos or captions. Landscape 3:2.
"""
        (prompts / f"still_{sid}.txt").write_text(still, encoding="utf-8")

        next_direction = section.get("next_direction", "the opening toward the next scene")
        focal = section.get("focal_point", "the central subject")
        scene_subject = section.get("subject", sid)
        if architecture == "extend":
            if index == 0:
                video = f"""Create one continuous cinematic camera move with no cuts, starting from the
attached scene image. Begin with a slow, steady forward glide toward {focal}. Reveal
{scene_subject} as one coherent space. In the final second, settle into a slow, steady
forward drift toward {next_direction}. Preserve the attached image's art direction,
materials, palette and lighting. Smooth motion, subtle parallax, no text or captions.
Landscape 16:9. Do not generate audio.
"""
            else:
                video = f"""Continue the attached video as the same uninterrupted camera shot. Do not restart
the shot, change lens, jump position, reverse direction or introduce a cut. Continue the
exact camera velocity and visual treatment from the final moment of the source video.
The camera travels into {scene_subject} toward {focal}. In the final second, settle back
into a slow, steady forward drift toward {next_direction}. Preserve the same world,
materials, palette, lighting and camera language. No text or captions. Landscape 16:9.
Do not generate audio.
"""
            (prompts / f"leg_{sid}.txt").write_text(video, encoding="utf-8")
        else:
            dive = f"""Create one continuous cinematic camera move with no cuts, starting from the attached
scene image. Begin high and outside the scene, then glide forward and descend toward
{focal}, revealing {scene_subject}. Preserve the attached image's exact art direction,
palette, materials and lighting. End in a calm, low-motion composition suitable for a
transition. Smooth motion, subtle parallax, no text or captions. Landscape 16:9.
"""
            (prompts / f"dive_{sid}.txt").write_text(dive, encoding="utf-8")

    if architecture == "bridge":
        for index in range(len(sections) - 1):
            left = sections[index]
            right = sections[index + 1]
            bridge = f"""Attach the actual last frame of {left['id']} first and the actual first frame of
{right['id']} second. Create a single continuous transition between the two attached
boundary frames. Begin as close as possible to reference image 1, continuing its camera
direction and velocity. Move through the connected world toward {right.get('subject', right['id'])},
and arrive as close as possible to reference image 2 without a hard cut. Keep the same art
direction, palette, lighting and lens language. Smooth slow motion, subtle parallax, no text
or captions. Landscape 16:9.
"""
            (prompts / f"bridge_{index + 1:02d}.txt").write_text(bridge, encoding="utf-8")

    checklist = expected_files(project, work)
    (work / "expected-files.txt").write_text("\n".join(str(p) for p in checklist) + "\n", encoding="utf-8")
    print(f"Wrote prompts to {prompts}")
    print(f"Wrote checklist to {work / 'expected-files.txt'}")


def expected_files(project: dict[str, Any], work: Path) -> list[Path]:
    source = work / "source"
    expected: list[Path] = [source / "style-anchor.png"]
    sections = project["sections"]
    for section in sections:
        sid = section["id"]
        expected.append(source / f"still_{sid}.png")
        if project.get("architecture", "extend") == "extend":
            expected.append(source / f"leg_{sid}.mp4")
        else:
            expected.append(source / f"dive_{sid}.mp4")
    if project.get("architecture") == "bridge":
        for index in range(len(sections) - 1):
            expected.append(source / f"conn_{index + 1:02d}.mp4")
    return expected


def validate(project: dict[str, Any], work: Path) -> None:
    missing: list[Path] = []
    empty: list[Path] = []
    for path in expected_files(project, work):
        if not path.exists():
            missing.append(path)
        elif path.stat().st_size == 0:
            empty.append(path)
    if missing or empty:
        if missing:
            print("Missing:", file=sys.stderr)
            for path in missing:
                print(f"  {path}", file=sys.stderr)
        if empty:
            print("Empty:", file=sys.stderr)
            for path in empty:
                print(f"  {path}", file=sys.stderr)
        raise SystemExit(1)
    print("All expected source assets exist and are non-empty.")


def source_clip(project: dict[str, Any], work: Path, sid: str) -> Path:
    prefix = "leg" if project.get("architecture", "extend") == "extend" else "dive"
    return work / "source" / f"{prefix}_{sid}.mp4"


def extract_frames(project: dict[str, Any], work: Path) -> None:
    paths = ensure_dirs(work)
    frames = paths["frames"]
    for section in project["sections"]:
        sid = section["id"]
        clip = source_clip(project, work, sid)
        if not clip.exists():
            raise SystemExit(f"Missing source clip: {clip}")
        run(["ffmpeg", "-v", "error", "-y", "-ss", "0", "-i", str(clip),
             "-frames:v", "1", "-q:v", "2", str(frames / f"first_{sid}.png")])
        run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.15", "-i", str(clip),
             "-frames:v", "1", "-q:v", "2", str(frames / f"last_{sid}.png")])
    print(f"Boundary frames written to {frames}")


def encode_video(src: Path, dst: Path, mobile: bool) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    vf = "scale='min(iw,1280)':-2,unsharp=5:5:0.6:5:5:0.0" if mobile else "unsharp=5:5:0.8:5:5:0.0"
    crf = "23" if mobile else "20"
    gop = "4" if mobile else "8"
    run([
        "ffmpeg", "-v", "error", "-y", "-i", str(src), "-an", "-vf", vf,
        "-c:v", "libx264", "-preset", "slow", "-crf", crf,
        "-pix_fmt", "yuv420p", "-g", gop, "-keyint_min", gop,
        "-sc_threshold", "0", "-movflags", "+faststart", str(dst),
    ])


def encode_stills(project: dict[str, Any], work: Path, assets: Path) -> None:
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg is required")
    assets.mkdir(parents=True, exist_ok=True)
    for section in project["sections"]:
        sid = section["id"]
        src = work / "source" / f"still_{sid}.png"
        if not src.exists():
            raise SystemExit(f"Missing still: {src}")
        dst = assets / f"{sid}.webp"
        run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf",
             "scale='min(iw,1800)':-2", "-c:v", "libwebp", "-quality", "84", str(dst)])
        print(dst)


def encode_videos(project: dict[str, Any], work: Path, assets: Path, mobile: bool) -> None:
    vid = assets / "vid"
    vid.mkdir(parents=True, exist_ok=True)
    for section in project["sections"]:
        sid = section["id"]
        src = source_clip(project, work, sid)
        if not src.exists():
            raise SystemExit(f"Missing source clip: {src}")
        encode_video(src, vid / f"{sid}.mp4", mobile=False)
        print(vid / f"{sid}.mp4")
        if mobile:
            encode_video(src, vid / f"{sid}-m.mp4", mobile=True)
            print(vid / f"{sid}-m.mp4")

    if project.get("architecture") == "bridge":
        for index in range(len(project["sections"]) - 1):
            src = work / "source" / f"conn_{index + 1:02d}.mp4"
            if not src.exists():
                raise SystemExit(f"Missing connector: {src}")
            encode_video(src, vid / f"conn{index + 1}.mp4", mobile=False)
            print(vid / f"conn{index + 1}.mp4")
            if mobile:
                encode_video(src, vid / f"conn{index + 1}-m.mp4", mobile=True)
                print(vid / f"conn{index + 1}-m.mp4")

    encode_stills(project, work, assets)


def js(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def emit_config(project: dict[str, Any], assets: Path) -> None:
    brand = project.get("brand", {})
    mobile = bool(project.get("mobile"))
    sections_out: list[dict[str, Any]] = []
    for section in project["sections"]:
        sid = section["id"]
        item: dict[str, Any] = {
            "id": sid,
            "label": section.get("label", sid),
            "still": f"{assets.as_posix()}/{sid}.webp",
            "clip": f"{assets.as_posix()}/vid/{sid}.mp4",
            "accent": section.get("accent", brand.get("accent")),
            "eyebrow": section.get("eyebrow", ""),
            "title": section.get("title", ""),
            "body": section.get("body", ""),
            "tags": section.get("tags", []),
        }
        if mobile:
            item["clipMobile"] = f"{assets.as_posix()}/vid/{sid}-m.mp4"
        for key in ("scroll", "linger", "cta"):
            if key in section:
                item[key] = section[key]
        sections_out.append({k: v for k, v in item.items() if v is not None})

    connectors: list[str] = []
    connectors_mobile: list[str] = []
    if project.get("architecture") == "bridge":
        for index in range(len(project["sections"]) - 1):
            connectors.append(f"{assets.as_posix()}/vid/conn{index + 1}.mp4")
            if mobile:
                connectors_mobile.append(f"{assets.as_posix()}/vid/conn{index + 1}-m.mp4")

    config: dict[str, Any] = {
        "brand": {"name": brand.get("name", "Scroll World")},
        "sections": sections_out,
        "connectors": connectors,
    }
    if mobile:
        config["connectorsMobile"] = connectors_mobile
    print("mountScrollWorld(document.getElementById('world'), " + json.dumps(config, ensure_ascii=False, indent=2) + ");")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version="prepare-assets 0.3.0-browser")
    sub = parser.add_subparsers(dest="command", required=True)

    def common(name: str) -> argparse.ArgumentParser:
        p = sub.add_parser(name)
        p.add_argument("--project", type=Path, required=True)
        p.add_argument("--work", type=Path, default=Path(".scroll-world"))
        return p

    common("prompts")
    common("validate")
    common("extract-frames")

    p_stills = common("encode-stills")
    p_stills.add_argument("--assets", type=Path, default=Path("assets"))

    p_encode = common("encode-videos")
    p_encode.add_argument("--assets", type=Path, default=Path("assets"))
    p_encode.add_argument("--mobile", action="store_true")

    p_config = sub.add_parser("emit-config")
    p_config.add_argument("--project", type=Path, required=True)
    p_config.add_argument("--assets", type=Path, default=Path("assets"))

    args = parser.parse_args()
    project = load_project(args.project)

    if args.command == "prompts":
        prompt_files(project, args.work)
    elif args.command == "validate":
        validate(project, args.work)
    elif args.command == "extract-frames":
        extract_frames(project, args.work)
    elif args.command == "encode-stills":
        encode_stills(project, args.work, args.assets)
    elif args.command == "encode-videos":
        encode_videos(project, args.work, args.assets, args.mobile)
    elif args.command == "emit-config":
        emit_config(project, args.assets)


if __name__ == "__main__":
    main()
