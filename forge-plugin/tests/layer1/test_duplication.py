"""Test content duplication detection from forge-duplication-detector workflow.

Validates:
- Content block similarity across skill/context/hook files
- Reports clusters of >70% similar content blocks (using difflib.SequenceMatcher)
- Scans SKILL.md, context .md files, and hook scripts

Migrated from .github/workflows/forge-duplication-detector.md as part of Phase 2 optimization.
"""

import difflib
import sys
from pathlib import Path
from typing import List, Tuple

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from conftest import FORGE_DIR


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SIMILARITY_THRESHOLD = 0.7  # 70% similarity threshold
MIN_BLOCK_LENGTH = 200  # Minimum characters for a content block to be considered


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_scannable_files() -> List[Tuple[str, Path]]:
    """Return (category/name, path) for all files to scan for duplication."""
    files = []
    
    # Scan 1: Skills (SKILL.md files)
    skills_dir = FORGE_DIR / "skills"
    for skill_dir in sorted(skills_dir.iterdir()):
        if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                files.append((f"skill/{skill_dir.name}", skill_md))
    
    # Scan 2: Context files (all .md files in domain directories)
    context_dir = FORGE_DIR / "context"
    for domain_dir in sorted(context_dir.iterdir()):
        if domain_dir.is_dir() and not domain_dir.name.startswith('.'):
            for md_file in sorted(domain_dir.rglob("*.md")):
                if md_file.name not in ["index.md"]:
                    rel_path = md_file.relative_to(context_dir)
                    files.append((f"context/{rel_path}", md_file))
    
    # Scan 3: Hook scripts (.sh files)
    hooks_dir = FORGE_DIR / "hooks"
    for hook_file in sorted(hooks_dir.glob("*.sh")):
        files.append((f"hook/{hook_file.name}", hook_file))
    
    # Scan 4: Command files
    commands_dir = FORGE_DIR / "commands"
    for cmd_file in sorted(commands_dir.glob("*.md")):
        if cmd_file.name not in ["index.md"]:
            files.append((f"command/{cmd_file.stem}", cmd_file))
    
    return files


def _extract_content_blocks(file_path: Path) -> List[str]:
    """Extract meaningful content blocks from a file.
    
    Splits on double newlines and filters out very short blocks.
    """
    try:
        content = file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return []
    
    # Remove YAML frontmatter if present
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[2]
    
    # Split into blocks (paragraphs, code blocks, etc.)
    blocks = content.split('\n\n')
    
    # Filter out very short blocks and normalize whitespace
    meaningful_blocks = []
    for block in blocks:
        normalized = ' '.join(block.split())
        if len(normalized) >= MIN_BLOCK_LENGTH:
            meaningful_blocks.append(normalized)
    
    return meaningful_blocks


def _find_similar_blocks(files: List[Tuple[str, Path]]) -> List[Tuple[str, str, float, str]]:
    """Find similar content blocks across files.
    
    Returns list of (file1, file2, similarity_ratio, similar_content_preview).
    """
    similar_pairs = []
    
    # Build content blocks for each file
    file_blocks = {}
    for name, path in files:
        blocks = _extract_content_blocks(path)
        if blocks:
            file_blocks[name] = blocks
    
    # Compare all pairs of files
    file_names = list(file_blocks.keys())
    for i, file1 in enumerate(file_names):
        for file2 in file_names[i+1:]:
            # Compare all blocks between the two files
            for block1 in file_blocks[file1]:
                for block2 in file_blocks[file2]:
                    ratio = difflib.SequenceMatcher(None, block1, block2).ratio()
                    
                    if ratio >= SIMILARITY_THRESHOLD:
                        # Create preview (first 100 chars)
                        preview = block1[:100] + "..." if len(block1) > 100 else block1
                        similar_pairs.append((file1, file2, ratio, preview))
    
    return similar_pairs


# ---------------------------------------------------------------------------
# Test Class
# ---------------------------------------------------------------------------

class TestContentDuplication:
    """Detect duplicated content across Forge components."""

    def test_no_high_duplication_in_skills(self):
        """Skills should not have >70% similar content blocks."""
        files = _get_scannable_files()
        skill_files = [(name, path) for name, path in files if name.startswith('skill/')]
        
        if len(skill_files) < 2:
            pytest.skip("Not enough skill files to compare")
        
        similar = _find_similar_blocks(skill_files)
        
        if similar:
            report_lines = [f"\nFound {len(similar)} high-similarity content blocks between skills:"]
            for file1, file2, ratio, preview in similar[:10]:  # Show first 10
                report_lines.append(
                    f"\n  {file1} ←→ {file2} ({ratio:.0%} similar)\n"
                    f"    Preview: {preview}"
                )
            if len(similar) > 10:
                report_lines.append(f"\n  ... and {len(similar) - 10} more")
            
            pytest.fail('\n'.join(report_lines))

    def test_no_high_duplication_in_context(self):
        """Context files should not have >70% similar content blocks."""
        files = _get_scannable_files()
        context_files = [(name, path) for name, path in files if name.startswith('context/')]
        
        if len(context_files) < 2:
            pytest.skip("Not enough context files to compare")
        
        similar = _find_similar_blocks(context_files)
        
        if similar:
            report_lines = [f"\nFound {len(similar)} high-similarity content blocks between context files:"]
            for file1, file2, ratio, preview in similar[:10]:
                report_lines.append(
                    f"\n  {file1} ←→ {file2} ({ratio:.0%} similar)\n"
                    f"    Preview: {preview}"
                )
            if len(similar) > 10:
                report_lines.append(f"\n  ... and {len(similar) - 10} more")
            
            pytest.fail('\n'.join(report_lines))

    def test_no_high_duplication_in_hooks(self):
        """Hook scripts should not have >70% similar content blocks."""
        files = _get_scannable_files()
        hook_files = [(name, path) for name, path in files if name.startswith('hook/')]
        
        if len(hook_files) < 2:
            pytest.skip("Not enough hook files to compare")
        
        similar = _find_similar_blocks(hook_files)
        
        if similar:
            report_lines = [f"\nFound {len(similar)} high-similarity content blocks between hooks:"]
            for file1, file2, ratio, preview in similar[:10]:
                report_lines.append(
                    f"\n  {file1} ←→ {file2} ({ratio:.0%} similar)\n"
                    f"    Preview: {preview}"
                )
            if len(similar) > 10:
                report_lines.append(f"\n  ... and {len(similar) - 10} more")
            
            pytest.fail('\n'.join(report_lines))

    def test_duplication_report(self):
        """Generate comprehensive duplication report across all file types."""
        files = _get_scannable_files()
        
        if len(files) < 2:
            pytest.skip("Not enough files to compare")
        
        similar = _find_similar_blocks(files)
        
        # This test is informational - it always passes but logs findings
        if similar:
            report_lines = [
                f"\n{'='*70}",
                f"DUPLICATION REPORT: Found {len(similar)} high-similarity pairs",
                f"{'='*70}"
            ]
            
            # Group by similarity level
            critical = [s for s in similar if s[2] >= 0.9]  # 90%+
            warning = [s for s in similar if 0.8 <= s[2] < 0.9]  # 80-89%
            info = [s for s in similar if 0.7 <= s[2] < 0.8]  # 70-79%
            
            if critical:
                report_lines.append(f"\n🔴 CRITICAL (≥90% similar): {len(critical)} pairs")
                for file1, file2, ratio, _ in critical[:5]:
                    report_lines.append(f"  • {file1} ←→ {file2} ({ratio:.0%})")
            
            if warning:
                report_lines.append(f"\n🟡 WARNING (80-89% similar): {len(warning)} pairs")
                for file1, file2, ratio, _ in warning[:5]:
                    report_lines.append(f"  • {file1} ←→ {file2} ({ratio:.0%})")
            
            if info:
                report_lines.append(f"\n🔵 INFO (70-79% similar): {len(info)} pairs")
                for file1, file2, ratio, _ in info[:5]:
                    report_lines.append(f"  • {file1} ←→ {file2} ({ratio:.0%})")
            
            report_lines.append(f"\n{'='*70}\n")
            
            # Print report to stdout (visible in pytest output with -v)
            print('\n'.join(report_lines))
