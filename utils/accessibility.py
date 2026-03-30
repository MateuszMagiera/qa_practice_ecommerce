"""
Accessibility (a11y) audit helper powered by axe-core.

Injects the axe-core engine into a Playwright page, runs a WCAG audit,
and attaches the results to the Allure report.

Usage:
    from utils.accessibility import run_axe_audit

    violations = run_axe_audit(page, page_name="Login Page")
    assert len(violations) == 0, f"Found {len(violations)} accessibility violations"
"""

import json
from typing import Optional

import allure
from playwright.sync_api import Page

# axe-core CDN — pinned version for deterministic results.
AXE_CORE_CDN = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js"


def _inject_axe(page: Page) -> None:
    """Inject the axe-core library into the current page."""
    page.add_script_tag(url=AXE_CORE_CDN)
    page.wait_for_function("typeof window.axe !== 'undefined'")


def _format_violation(violation: dict) -> str:
    """Format a single violation into a human-readable string."""
    nodes_info = []
    for node in violation.get("nodes", []):
        target = ", ".join(str(t) for t in node.get("target", []))
        failure = "; ".join(
            msg.get("message", "")
            for msg in node.get("any", []) + node.get("all", []) + node.get("none", [])
        )
        nodes_info.append(f"    → {target}\n      {failure}")

    return (
        f"[{violation['impact'].upper()}] {violation['id']}: {violation['description']}\n"
        f"  Help: {violation['helpUrl']}\n"
        f"  Affected nodes ({len(violation.get('nodes', []))}):\n"
        + "\n".join(nodes_info)
    )


def run_axe_audit(
    page: Page,
    page_name: str = "Page",
    tags: Optional[list[str]] = None,
) -> list[dict]:
    """
    Run an axe-core accessibility audit on the current page.

    Args:
        page: Playwright Page object (must already be navigated).
        page_name: Human-readable name for Allure reporting.
        tags: WCAG rule tags to audit against (default: WCAG 2.1 Level A & AA).

    Returns:
        List of violation dicts from axe-core (empty = fully accessible).
    """
    if tags is None:
        tags = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]

    with allure.step(f"Inject axe-core into {page_name}"):
        _inject_axe(page)

    with allure.step(f"Run WCAG accessibility audit on {page_name}"):
        axe_options = json.dumps({"runOnly": {"type": "tag", "values": tags}})
        results = page.evaluate(f"axe.run(document, {axe_options})")

    violations = results.get("violations", [])
    passes = results.get("passes", [])
    incomplete = results.get("incomplete", [])

    # --- Allure: attach summary ---
    summary = (
        f"Accessibility audit: {page_name}\n"
        f"{'=' * 50}\n"
        f"  ✅ Passed rules:     {len(passes)}\n"
        f"  ❌ Violations:       {len(violations)}\n"
        f"  ⚠️  Incomplete:      {len(incomplete)}\n"
        f"  📋 WCAG tags tested: {', '.join(tags)}\n"
    )
    allure.attach(summary, name=f"a11y summary — {page_name}", attachment_type=allure.attachment_type.TEXT)

    # --- Allure: attach violations detail ---
    if violations:
        report_lines = [_format_violation(v) for v in violations]
        full_report = f"Found {len(violations)} violation(s) on {page_name}:\n\n" + "\n\n".join(report_lines)
        allure.attach(full_report, name=f"a11y violations — {page_name}", attachment_type=allure.attachment_type.TEXT)

        allure.attach(
            json.dumps(violations, indent=2),
            name=f"a11y violations (raw JSON) — {page_name}",
            attachment_type=allure.attachment_type.JSON,
        )

    return violations


def filter_by_impact(violations: list[dict], levels: tuple[str, ...] = ("critical",)) -> list[dict]:
    """Filter violations by impact level(s). Default: critical only."""
    return [v for v in violations if v.get("impact") in levels]

