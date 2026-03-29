# One-off generator for AZ-400 path study pages. Run: python _generate_az400_paths.py
import html
import os

from build_az400_all import module_block

STYLE_AND_HEAD = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <script>
    (function() {{
      try {{
        var t = localStorage.getItem("az400-theme");
        if (t === "dark") document.documentElement.setAttribute("data-theme", "dark");
      }} catch (e) {{}}
    }})();
  </script>
  <style>
    :root {{
      --bg: #f8f9fa;
      --text: #1a1a1a;
      --border: #dee2e6;
      --accent: #0078d4;
      --accent-soft: #e3f2fd;
      --nav-bg: #fff;
      --muted: #666;
      --code-bg: #e9ecef;
      --code-border: #ced4da;
      --code-text: #c41e3a;
      --table-header-bg: #e3f2fd;
      --table-border: #bbdefb;
    }}
    [data-theme="dark"] {{
      --bg: #1a1a1a;
      --text: #e8e8e8;
      --border: #404040;
      --accent: #58a6ff;
      --accent-soft: #1e3a5f;
      --nav-bg: #252525;
      --muted: #a0a0a0;
      --code-bg: #2d2d2d;
      --code-border: #404040;
      --code-text: #f97583;
      --table-header-bg: #1e3a5f;
      --table-border: #2d4a6a;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-size: 16px; line-height: 1.6; color: var(--text); background: var(--bg); }}
    .top-nav {{ position: sticky; top: 0; z-index: 100; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.75rem; padding: 0.75rem 1.5rem; background: var(--nav-bg); border-bottom: 1px solid var(--border); box-shadow: 0 1px 3px rgba(0,0,0,0.06); }}
    .top-nav .site-title {{ font-size: 1.25rem; font-weight: 700; color: var(--text); text-decoration: none; margin-right: 1rem; }}
    .top-nav .site-title:hover {{ color: var(--accent); }}
    .top-nav .nav-links {{ display: flex; align-items: center; flex-wrap: wrap; gap: 0.25rem; list-style: none; margin: 0; padding: 0; }}
    .top-nav .nav-links a {{ display: block; padding: 0.5rem 0.75rem; font-size: 0.95rem; color: var(--text); text-decoration: none; border-radius: 6px; transition: background 0.15s ease, color 0.15s ease; }}
    .top-nav .nav-links a:hover {{ background: var(--accent-soft); color: var(--accent); }}
    .top-nav .nav-right {{ display: flex; align-items: center; gap: 0.5rem; }}
    .top-nav .nav-wrap {{ display: flex; align-items: center; gap: 0.75rem; }}
    .top-nav .back-link {{ font-size: 0.9rem; color: var(--muted); }}
    .top-nav .back-link:hover {{ color: var(--accent); }}
    .menu-toggle {{ display: none; align-items: center; justify-content: center; width: 44px; height: 44px; padding: 0; border: 1px solid var(--border); border-radius: 6px; background: var(--nav-bg); color: var(--text); cursor: pointer; font-size: 1.25rem; }}
    .theme-toggle {{ display: inline-flex; align-items: center; justify-content: center; width: 36px; height: 36px; padding: 0; border: 1px solid var(--border); border-radius: 6px; background: var(--bg); color: var(--text); cursor: pointer; font-size: 1.1rem; }}
    .main-wrap {{ min-height: 100vh; padding: 2rem 1.5rem 3rem; }}
    main {{ max-width: 800px; margin: 0 auto; }}
    main section {{ margin-bottom: 3rem; padding-bottom: 2rem; border-bottom: 1px solid var(--border); }}
    main section:last-child {{ border-bottom: none; }}
    main h2 {{ font-size: 1.5rem; margin-top: 0; margin-bottom: 0.5rem; color: var(--accent); }}
    main .weight {{ font-size: 0.9rem; color: var(--muted); margin-bottom: 1rem; }}
    main h4 {{ font-size: 1.05rem; margin: 1.25rem 0 0.5rem; color: var(--accent); font-weight: 600; }}
    main ul, main ol {{ margin: 0.5rem 0 1rem; padding-left: 1.35rem; }}
    main li {{ margin: 0.35rem 0; }}
    main code {{ font-family: ui-monospace, "Cascadia Code", Menlo, Consolas, monospace; font-size: 0.9em; padding: 0.2em 0.4em; background: var(--code-bg); border: 1px solid var(--code-border); border-radius: 4px; color: var(--code-text); }}
    main table {{ margin: 0.75rem 0; border: 1px solid var(--table-border); border-radius: 6px; overflow: hidden; }}
    main table th {{ background: var(--table-header-bg); color: var(--accent); font-weight: 600; }}
    main table td, main table th {{ padding: 0.5rem 0.75rem; border-bottom: 1px solid var(--table-border); }}
    main table tr:last-child td, main table tr:last-child th {{ border-bottom: none; }}
    .collapsible-block {{ margin-bottom: 0.5rem; border: 1px solid var(--border); border-radius: 6px; overflow: hidden; }}
    .collapsible-block .block-title {{ display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; margin: 0; padding: 0.65rem 1rem; font-size: 1.1rem; cursor: pointer; user-select: none; background: var(--accent-soft); border-bottom: 1px solid var(--border); }}
    .collapsible-block .block-title:hover {{ background: var(--border); }}
    .collapsible-block.collapsed .block-title {{ border-bottom: none; }}
    .collapsible-block .block-toggle {{ flex-shrink: 0; margin: 0; padding: 0.2rem 0.4rem; border: none; background: transparent; color: var(--accent); font-size: 0.75rem; cursor: pointer; transition: transform 0.2s ease; }}
    .collapsible-block.collapsed .block-toggle {{ transform: rotate(-90deg); }}
    .collapsible-block .block-content {{ padding: 1rem 1.25rem; background: var(--bg); }}
    .collapsible-block.collapsed .block-content {{ display: none; }}
    .fold-unfold {{ display: flex; gap: 0.5rem; margin-bottom: 1rem; flex-wrap: wrap; }}
    .fold-unfold button {{ padding: 0.4rem 0.75rem; font-size: 0.875rem; border: 1px solid var(--border); border-radius: 6px; background: var(--nav-bg); color: var(--text); cursor: pointer; }}
    @media (max-width: 768px) {{
      .menu-toggle {{ display: flex; }}
      .top-nav .nav-wrap {{ display: none; width: 100%; flex-direction: column; align-items: stretch; padding-top: 0.5rem; border-top: 1px solid var(--border); margin-top: 0.25rem; }}
      .top-nav.nav-open .nav-wrap {{ display: flex; }}
      .top-nav .nav-links {{ flex-direction: column; padding: 0; }}
      .main-wrap {{ padding: 1.25rem 1rem 2rem; }}
    }}
    @media print {{
      .menu-toggle, .theme-toggle, .fold-unfold, .top-nav {{ display: none !important; }}
      .collapsible-block.collapsed .block-content {{ display: block !important; }}
      .main-wrap {{ padding: 0; }}
    }}
  </style>
</head>
<body>
'''

SCRIPT = r'''
  <script>
    (function() {
      var THEME_KEY = "az400-theme";
      var themeToggle = document.getElementById("themeToggle");
      function getTheme() { return document.documentElement.getAttribute("data-theme") || "light"; }
      function setTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        try { localStorage.setItem(THEME_KEY, theme); } catch (e) {}
        themeToggle.setAttribute("aria-label", theme === "dark" ? "Switch to light mode" : "Switch to dark mode");
        themeToggle.setAttribute("title", theme === "dark" ? "Switch to light mode" : "Switch to dark mode");
        themeToggle.textContent = theme === "dark" ? "☀" : "🌙";
      }
      function initTheme() {
        var saved = null;
        try { saved = localStorage.getItem(THEME_KEY); } catch (e) {}
        setTheme(saved === "dark" || saved === "light" ? saved : "light");
      }
      initTheme();
      themeToggle.addEventListener("click", function() { setTheme(getTheme() === "dark" ? "light" : "dark"); });
      var topNav = document.getElementById("topNav");
      var menuToggle = document.getElementById("menuToggle");
      menuToggle.addEventListener("click", function() {
        topNav.classList.toggle("nav-open");
        menuToggle.setAttribute("aria-label", topNav.classList.contains("nav-open") ? "Close menu" : "Open menu");
      });
      document.querySelectorAll(".top-nav .nav-links a").forEach(function(link) {
        link.addEventListener("click", function() {
          if (window.innerWidth <= 768) {
            topNav.classList.remove("nav-open");
            menuToggle.setAttribute("aria-label", "Open menu");
          }
        });
      });
      var blocks = document.querySelectorAll(".collapsible-block");
      function toggleBlock(block) {
        block.classList.toggle("collapsed");
        var btn = block.querySelector(".block-toggle");
        if (btn) btn.setAttribute("aria-label", block.classList.contains("collapsed") ? "Expand section" : "Collapse section");
      }
      blocks.forEach(function(block) {
        var title = block.querySelector(".block-title");
        var toggleBtn = block.querySelector(".block-toggle");
        if (title) title.addEventListener("click", function(e) { if (e.target !== toggleBtn) toggleBlock(block); });
        if (toggleBtn) toggleBtn.addEventListener("click", function(e) { e.stopPropagation(); toggleBlock(block); });
      });
      var foldAll = document.getElementById("foldAll");
      var unfoldAll = document.getElementById("unfoldAll");
      if (foldAll) foldAll.addEventListener("click", function() {
        blocks.forEach(function(block) { block.classList.add("collapsed"); });
        document.querySelectorAll(".block-toggle").forEach(function(btn) { btn.setAttribute("aria-label", "Expand section"); });
      });
      if (unfoldAll) unfoldAll.addEventListener("click", function() {
        blocks.forEach(function(block) { block.classList.remove("collapsed"); });
        document.querySelectorAll(".block-toggle").forEach(function(btn) { btn.setAttribute("aria-label", "Collapse section"); });
      });
    })();
  </script>
</body>
</html>
'''

PATHS = [
    {
        "file": "az400-ci.html",
        "short": "AZ-400: CI",
        "title": "AZ-400: CI with Azure Pipelines & GitHub Actions",
        "desc": "Study guide: Implement CI with Azure Pipelines and GitHub Actions (Microsoft Learn).",
        "url": "https://learn.microsoft.com/en-us/training/paths/az-400-implement-ci-azure-pipelines-github-actions/",
        "blurb": "Continuous integration with Azure Pipelines and GitHub Actions: agents, concurrency, pipeline strategy, integration patterns, and container builds.",
        "mods": [
            ("m-ci-1", "Explore Azure Pipelines", "explore-azure-pipelines"),
            ("m-ci-2", "Manage Azure Pipeline agents and pools", "manage-azure-pipeline-agents-pools"),
            ("m-ci-3", "Describe pipelines and concurrency", "describe-pipelines-concurrency"),
            ("m-ci-4", "Design and implement a pipeline strategy", "implement-pipeline-strategy"),
            ("m-ci-5", "Integrate with Azure Pipelines", "integrate-azure-pipelines"),
            ("m-ci-6", "Introduction to GitHub Actions", "introduction-to-github-actions"),
            ("m-ci-7", "Learn continuous integration with GitHub Actions", "learn-continuous-integration-github-actions"),
            ("m-ci-8", "Design a container build strategy", "design-container-build-strategy"),
        ],
    },
    {
        "file": "az400-release.html",
        "short": "AZ-400: Release",
        "title": "AZ-400: Design and implement a release strategy",
        "desc": "Study guide: Release pipelines, environments, templates, and health checks (Microsoft Learn).",
        "url": "https://learn.microsoft.com/en-us/training/paths/az-400-design-implement-release-strategy/",
        "blurb": "Continuous delivery: release pipelines, approvals, gates, environments, modular tasks, and automated health inspection.",
        "mods": [
            ("m-rel-1", "Create a Release Pipeline", "create-release-pipeline-devops"),
            ("m-rel-2", "Explore release strategy recommendations", "explore-release-strategy-recommendations"),
            ("m-rel-3", "Configure and provision environments", "configure-provision-environments"),
            ("m-rel-4", "Manage and modularize tasks and templates", "manage-modularize-tasks-templates"),
            ("m-rel-5", "Automate inspection of health", "automate-inspection-health"),
        ],
    },
    {
        "file": "az400-secure-deploy.html",
        "short": "AZ-400: Secure CD",
        "title": "AZ-400: Secure continuous deployment",
        "desc": "Study guide: Deployment patterns, progressive delivery, identity, and configuration (Microsoft Learn).",
        "url": "https://learn.microsoft.com/en-us/training/paths/az-400-implement-secure-continuous-deployment/",
        "blurb": "Secure CD: deployment patterns, blue-green and feature flags, canary and dark launching, A/B and progressive exposure, identity integration, app configuration.",
        "mods": [
            ("m-sd-1", "Introduction to deployment patterns", "introduction-to-deployment-patterns"),
            ("m-sd-2", "Blue-green deployment and feature toggles", "implement-blue-green-deployment-feature-toggles"),
            ("m-sd-3", "Canary releases and dark launching", "implement-canary-releases-dark-launching"),
            ("m-sd-4", "A/B testing and progressive exposure", "implement-test-progressive-exposure-deployment"),
            ("m-sd-5", "Integrate with identity management systems", "integrate-identity-management-systems"),
            ("m-sd-6", "Manage application configuration data", "manage-application-configuration-data"),
        ],
    },
    {
        "file": "az400-iac.html",
        "short": "AZ-400: IaC",
        "title": "AZ-400: Infrastructure as Code & DSC",
        "desc": "Study guide: IaC on Azure, ARM, Bicep, CLI, Automation, DSC (Microsoft Learn).",
        "url": "https://learn.microsoft.com/en-us/training/paths/az-400-manage-infrastructure-as-code-using-azure/",
        "blurb": "Declarative infrastructure: IaC concepts, ARM/Bicep, Azure CLI, Azure Automation, Desired State Configuration.",
        "mods": [
            ("m-iac-1", "Explore IaC and configuration management", "explore-infrastructure-code-configuration-management"),
            ("m-iac-2", "Create Azure resources using ARM templates", "create-azure-resources-using-azure-resource-manager-templates"),
            ("m-iac-3", "Create Azure resources using Azure CLI", "create-azure-resources-by-using-azure-cli"),
            ("m-iac-4", "Explore Azure Automation with DevOps", "explore-azure-automation-devops"),
            ("m-iac-5", "Implement Desired State Configuration (DSC)", "implement-desired-state-configuration-dsc"),
            ("m-iac-6", "Implement Bicep", "implement-bicep"),
        ],
    },
    {
        "file": "az400-dependencies.html",
        "short": "AZ-400: Dependencies",
        "title": "AZ-400: Dependency management strategy",
        "desc": "Study guide: Packages, feeds, security, versioning, GitHub Packages (Microsoft Learn).",
        "url": "https://learn.microsoft.com/en-us/training/paths/az-400-design-implement-dependency-management-strategy/",
        "blurb": "Dependencies: identification, feeds, Azure Artifacts, migration, security, semantic versioning, GitHub Packages.",
        "mods": [
            ("m-dep-1", "Explore package dependencies", "explore-package-dependencies"),
            ("m-dep-2", "Understand package management", "understand-package-management"),
            ("m-dep-3", "Migrate, consolidate, and secure artifacts", "migrate-consolidating-secure-artifacts"),
            ("m-dep-4", "Implement a versioning strategy", "implement-versioning-strategy"),
            ("m-dep-5", "Introduction to GitHub Packages", "introduction-github-packages"),
        ],
    },
    {
        "file": "az400-feedback.html",
        "short": "AZ-400: Feedback",
        "title": "AZ-400: Continuous feedback",
        "desc": "Study guide: Monitoring, dashboards, knowledge sharing, analytics, culture (Microsoft Learn).",
        "url": "https://learn.microsoft.com/en-us/training/paths/az-400-implement-continuous-feedback/",
        "blurb": "Feedback loops: Azure Monitor, Application Insights, dashboards, wikis, automated analytics, alerts and blameless culture.",
        "mods": [
            ("m-fb-1", "Implement tools to track usage and flow", "implement-tools-track-usage-flow"),
            ("m-fb-2", "Develop monitoring and status dashboards", "develop-monitor-status-dashboards"),
            ("m-fb-3", "Share knowledge within teams", "share-knowledge-within-teams"),
            ("m-fb-4", "Design processes to automate application analytics", "design-processes-automate-application-analytics"),
            ("m-fb-5", "Manage alerts, blameless retrospectives, just culture", "manage-alerts-blameless-retrospectives-just-culture"),
        ],
    },
    {
        "file": "az400-devsecops.html",
        "short": "AZ-400: DevSecOps",
        "title": "AZ-400: Security & compliance for code bases",
        "desc": "Study guide: DevSecOps, OSS, SCA, Defender and governance (Microsoft Learn).",
        "url": "https://learn.microsoft.com/en-us/training/paths/az-400-implement-security-validate-code-bases-compliance/",
        "blurb": "DevSecOps: secure pipelines, OSS licenses, software composition analysis, Defender for Cloud, Policy, GitHub Advanced Security.",
        "mods": [
            ("m-sec-1", "Introduction to Secure DevOps", "introduction-to-secure-devops"),
            ("m-sec-2", "Implement open-source software", "implement-open-source-software-azure"),
            ("m-sec-3", "Software Composition Analysis", "software-composition-analysis"),
            ("m-sec-4", "Security monitoring and governance", "security-monitoring-and-governance"),
        ],
    },
]


def path_page(p):
    nav_nums = "".join(f'        <li><a href="#{m[0]}">{i}</a></li>\n' for i, m in enumerate(p["mods"], 1))
    blocks = "".join(module_block(m[0], m[1], m[2]) for m in p["mods"])
    head = STYLE_AND_HEAD.format(title=html.escape(p["title"]), desc=html.escape(p["desc"]))
    site_link = p["file"]
    nav_title = html.escape(p.get("short", p["title"]))
    return head + f'''  <header class="top-nav" id="topNav">
    <a href="{site_link}" class="site-title">{nav_title}</a>
    <button type="button" class="menu-toggle" id="menuToggle" aria-label="Open menu">☰</button>
    <div class="nav-wrap">
      <ul class="nav-links">
        <li><a href="../index.html" class="back-link">← Back to portfolio</a></li>
        <li><a href="az400-index.html">AZ-400 paths</a></li>
        <li><a href="az104.html">AZ-104</a></li>
        <li><a href="#path-overview">Path</a></li>
{nav_nums}      </ul>
      <div class="nav-right">
        <button type="button" class="theme-toggle" id="themeToggle" aria-label="Toggle theme">☀</button>
      </div>
    </div>
  </header>
  <div class="layout">
    <div class="main-wrap">
      <main>
        <div class="fold-unfold">
          <button type="button" id="foldAll" aria-label="Collapse all sections">Fold all</button>
          <button type="button" id="unfoldAll" aria-label="Expand all sections">Unfold all</button>
        </div>
        <section id="path-overview">
          <h2>{html.escape(p["title"])}</h2>
          <p class="weight">Microsoft Learn learning path · Advanced</p>
          <p>Official path: <a href="{p["url"]}" target="_blank" rel="noopener">{html.escape(p["title"])}</a>. {html.escape(p["blurb"])} Use the module links below for full units, labs, and assessments.</p>
        </section>
        <section id="modules">
          <h2>Modules</h2>
{blocks}        </section>
      </main>
    </div>
  </div>
''' + SCRIPT


def index_page():
    rows = [
        ("Git & Enterprise DevOps", "az400.html", "8", "Repositories, branching, PRs, hooks, inner source, technical debt."),
    ]
    for p in PATHS:
        rows.append((p["title"].replace("AZ-400: ", ""), p["file"], str(len(p["mods"])), p["blurb"]))
    trs = ""
    for name, fn, count, desc in rows:
        trs += f"            <tr><td><a href=\"{html.escape(fn)}\">{html.escape(name)}</a></td><td>{count}</td><td>{html.escape(desc)}</td></tr>\n"
    head = STYLE_AND_HEAD.format(
        title="AZ-400 Study Guides — Index",
        desc="Index of Microsoft Learn AZ-400 study guide pages.",
    )
    return head + r'''  <header class="top-nav" id="topNav">
    <a href="az400-index.html" class="site-title">AZ-400 Study Guides</a>
    <button type="button" class="menu-toggle" id="menuToggle" aria-label="Open menu">☰</button>
    <div class="nav-wrap">
      <ul class="nav-links">
        <li><a href="../index.html" class="back-link">← Back to portfolio</a></li>
        <li><a href="az104.html">AZ-104</a></li>
        <li><a href="#paths">Paths</a></li>
      </ul>
      <div class="nav-right">
        <button type="button" class="theme-toggle" id="themeToggle" aria-label="Toggle theme">☀</button>
      </div>
    </div>
  </header>
  <div class="layout">
    <div class="main-wrap">
      <main>
        <section id="paths">
          <h2>AZ-400 Microsoft Learn paths</h2>
          <p class="weight">Each page summarizes modules with links to official training.</p>
          <p>These guides align with the <a href="https://learn.microsoft.com/en-us/certifications/exams/az-400/" target="_blank" rel="noopener">AZ-400 Designing and Implementing Microsoft DevOps Solutions</a> exam skills and Microsoft Learn collections.</p>
          <table>
            <tr><th>Path</th><th>Modules</th><th>Topics</th></tr>
''' + trs + r'''          </table>
        </section>
      </main>
    </div>
  </div>
''' + SCRIPT


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "az400-index.html"), "w", encoding="utf-8") as f:
        f.write(index_page())
    for p in PATHS:
        with open(os.path.join(base, p["file"]), "w", encoding="utf-8") as f:
            f.write(path_page(p))
    print("Wrote az400-index.html and", len(PATHS), "path pages.")


if __name__ == "__main__":
    main()
