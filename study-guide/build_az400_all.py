# Builds study-guide/az400-all.html (EN) or study-guide/fr/az400-all.html (FR).
# Run from repo root: python study-guide/build_az400_all.py
# French: python study-guide/build_az400_all.py --locale fr
# Regeneration (FR): python study-guide/fetch_az400_locale_data.py --locale fr-fr
#   then python study-guide/build_az400_all.py --locale fr
#   then python study-guide/_generate_az400_paths.py --locale fr
import argparse
import html
import os
import re

DIR = os.path.dirname(os.path.abspath(__file__))

PATHS_EXTRA = [
    {
        "id": "path-ci",
        "num": 2,
        "h2": "CI with Azure Pipelines & GitHub Actions",
        "weight": "8 modules · Advanced · Microsoft Learn path",
        "url": "https://learn.microsoft.com/en-us/training/paths/az-400-implement-ci-azure-pipelines-github-actions/",
        "intro": "Continuous integration: Azure Pipelines fundamentals, agents and pools, concurrency, pipeline strategy, templates and multi-repo integration, GitHub Actions, CI workflows, container build strategy.",
        "mods": [
            ("Explore Azure Pipelines", "explore-azure-pipelines"),
            ("Manage Azure Pipeline agents and pools", "manage-azure-pipeline-agents-pools"),
            ("Describe pipelines and concurrency", "describe-pipelines-concurrency"),
            ("Design and implement a pipeline strategy", "implement-pipeline-strategy"),
            ("Integrate with Azure Pipelines", "integrate-azure-pipelines"),
            ("Introduction to GitHub Actions", "introduction-to-github-actions"),
            ("Learn continuous integration with GitHub Actions", "learn-continuous-integration-github-actions"),
            ("Design a container build strategy", "design-container-build-strategy"),
        ],
    },
    {
        "id": "path-release",
        "num": 3,
        "h2": "Design and implement a release strategy",
        "weight": "5 modules · Advanced",
        "url": "https://learn.microsoft.com/en-us/training/paths/az-400-design-implement-release-strategy/",
        "intro": "Release pipelines, artifact sources, approvals and gates, environment provisioning, task groups and variable groups, health checks and service hooks.",
        "mods": [
            ("Create a Release Pipeline", "create-release-pipeline-devops"),
            ("Explore release strategy recommendations", "explore-release-strategy-recommendations"),
            ("Configure and provision environments", "configure-provision-environments"),
            ("Manage and modularize tasks and templates", "manage-modularize-tasks-templates"),
            ("Automate inspection of health", "automate-inspection-health"),
        ],
    },
    {
        "id": "path-securecd",
        "num": 4,
        "h2": "Secure continuous deployment",
        "weight": "6 modules · Advanced",
        "url": "https://learn.microsoft.com/en-us/training/paths/az-400-implement-secure-continuous-deployment/",
        "intro": "Deployment patterns, blue-green and feature toggles, canary and dark launching, A/B and progressive exposure, identity for pipelines, application configuration.",
        "mods": [
            ("Introduction to deployment patterns", "introduction-to-deployment-patterns"),
            ("Blue-green deployment and feature toggles", "implement-blue-green-deployment-feature-toggles"),
            ("Canary releases and dark launching", "implement-canary-releases-dark-launching"),
            ("A/B testing and progressive exposure", "implement-test-progressive-exposure-deployment"),
            ("Integrate with identity management systems", "integrate-identity-management-systems"),
            ("Manage application configuration data", "manage-application-configuration-data"),
        ],
    },
    {
        "id": "path-iac",
        "num": 5,
        "h2": "Infrastructure as code & DSC",
        "weight": "6 modules · Advanced",
        "url": "https://learn.microsoft.com/en-us/training/paths/az-400-manage-infrastructure-as-code-using-azure/",
        "intro": "Declarative Azure: IaC concepts, ARM and Bicep, Azure CLI automation, Azure Automation runbooks, Desired State Configuration.",
        "mods": [
            ("Explore IaC and configuration management", "explore-infrastructure-code-configuration-management"),
            ("Create Azure resources using ARM templates", "create-azure-resources-using-azure-resource-manager-templates"),
            ("Create Azure resources using Azure CLI", "create-azure-resources-by-using-azure-cli"),
            ("Explore Azure Automation with DevOps", "explore-azure-automation-devops"),
            ("Implement Desired State Configuration (DSC)", "implement-desired-state-configuration-dsc"),
            ("Implement Bicep", "implement-bicep"),
        ],
    },
    {
        "id": "path-deps",
        "num": 6,
        "h2": "Dependency management strategy",
        "weight": "5 modules · Advanced",
        "url": "https://learn.microsoft.com/en-us/training/paths/az-400-design-implement-dependency-management-strategy/",
        "intro": "Package feeds, Azure Artifacts, migration and security, semantic versioning, GitHub Packages.",
        "mods": [
            ("Explore package dependencies", "explore-package-dependencies"),
            ("Understand package management", "understand-package-management"),
            ("Migrate, consolidate, and secure artifacts", "migrate-consolidating-secure-artifacts"),
            ("Implement a versioning strategy", "implement-versioning-strategy"),
            ("Introduction to GitHub Packages", "introduction-github-packages"),
        ],
    },
    {
        "id": "path-feedback",
        "num": 7,
        "h2": "Continuous feedback",
        "weight": "5 modules · Advanced",
        "url": "https://learn.microsoft.com/en-us/training/paths/az-400-implement-continuous-feedback/",
        "intro": "Monitoring, dashboards, knowledge sharing, automated analytics, alerts and blameless culture.",
        "mods": [
            ("Implement tools to track usage and flow", "implement-tools-track-usage-flow"),
            ("Develop monitoring and status dashboards", "develop-monitor-status-dashboards"),
            ("Share knowledge within teams", "share-knowledge-within-teams"),
            ("Design processes to automate application analytics", "design-processes-automate-application-analytics"),
            ("Manage alerts, blameless retrospectives, just culture", "manage-alerts-blameless-retrospectives-just-culture"),
        ],
    },
    {
        "id": "path-sec",
        "num": 8,
        "h2": "Security & compliance for code bases",
        "weight": "4 modules · Advanced",
        "url": "https://learn.microsoft.com/en-us/training/paths/az-400-implement-security-validate-code-bases-compliance/",
        "intro": "DevSecOps: secure pipelines, OSS licensing, software composition analysis, Defender for Cloud, Policy, GitHub Advanced Security.",
        "mods": [
            ("Introduction to Secure DevOps", "introduction-to-secure-devops"),
            ("Implement open-source software", "implement-open-source-software-azure"),
            ("Software Composition Analysis", "software-composition-analysis"),
            ("Security monitoring and governance", "security-monitoring-and-governance"),
        ],
    },
]

PATHS_EXTRA_FR = [
    {
        "id": "path-ci",
        "num": 2,
        "h2": "Intégration continue avec Azure Pipelines et GitHub Actions",
        "weight": "8 modules · Avancé · Parcours Microsoft Learn",
        "url": "https://learn.microsoft.com/fr-fr/training/paths/az-400-implement-ci-azure-pipelines-github-actions/",
        "intro": "Intégration continue : fondamentaux Azure Pipelines, agents et pools, concurrence, stratégie de pipeline, modèles et intégration multi-dépôt, GitHub Actions, workflows CI, stratégie de build de conteneurs.",
        "mods": [
            ("Explore Azure Pipelines", "explore-azure-pipelines"),
            ("Manage Azure Pipeline agents and pools", "manage-azure-pipeline-agents-pools"),
            ("Describe pipelines and concurrency", "describe-pipelines-concurrency"),
            ("Design and implement a pipeline strategy", "implement-pipeline-strategy"),
            ("Integrate with Azure Pipelines", "integrate-azure-pipelines"),
            ("Introduction to GitHub Actions", "introduction-to-github-actions"),
            ("Learn continuous integration with GitHub Actions", "learn-continuous-integration-github-actions"),
            ("Design a container build strategy", "design-container-build-strategy"),
        ],
    },
    {
        "id": "path-release",
        "num": 3,
        "h2": "Concevoir et implémenter une stratégie de mise en production",
        "weight": "5 modules · Avancé",
        "url": "https://learn.microsoft.com/fr-fr/training/paths/az-400-design-implement-release-strategy/",
        "intro": "Pipelines de mise en production, sources d’artefacts, approbations et portes, approvisionnement des environnements, groupes de tâches et groupes de variables, contrôles d’intégrité et hooks de service.",
        "mods": [
            ("Create a Release Pipeline", "create-release-pipeline-devops"),
            ("Explore release strategy recommendations", "explore-release-strategy-recommendations"),
            ("Configure and provision environments", "configure-provision-environments"),
            ("Manage and modularize tasks and templates", "manage-modularize-tasks-templates"),
            ("Automate inspection of health", "automate-inspection-health"),
        ],
    },
    {
        "id": "path-securecd",
        "num": 4,
        "h2": "Sécuriser le déploiement continu",
        "weight": "6 modules · Avancé",
        "url": "https://learn.microsoft.com/fr-fr/training/paths/az-400-implement-secure-continuous-deployment/",
        "intro": "Modèles de déploiement, bleu-vert et bascules de fonctionnalité, canary et lancement sombre, tests A/B et exposition progressive, identité pour les pipelines, configuration de l’application.",
        "mods": [
            ("Introduction to deployment patterns", "introduction-to-deployment-patterns"),
            ("Blue-green deployment and feature toggles", "implement-blue-green-deployment-feature-toggles"),
            ("Canary releases and dark launching", "implement-canary-releases-dark-launching"),
            ("A/B testing and progressive exposure", "implement-test-progressive-exposure-deployment"),
            ("Integrate with identity management systems", "integrate-identity-management-systems"),
            ("Manage application configuration data", "manage-application-configuration-data"),
        ],
    },
    {
        "id": "path-iac",
        "num": 5,
        "h2": "Infrastructure as code et DSC",
        "weight": "6 modules · Avancé",
        "url": "https://learn.microsoft.com/fr-fr/training/paths/az-400-manage-infrastructure-as-code-using-azure/",
        "intro": "Azure déclaratif : concepts IaC, ARM et Bicep, automatisation Azure CLI, runbooks Azure Automation, Desired State Configuration.",
        "mods": [
            ("Explore IaC and configuration management", "explore-infrastructure-code-configuration-management"),
            ("Create Azure resources using ARM templates", "create-azure-resources-using-azure-resource-manager-templates"),
            ("Create Azure resources using Azure CLI", "create-azure-resources-by-using-azure-cli"),
            ("Explore Azure Automation with DevOps", "explore-azure-automation-devops"),
            ("Implement Desired State Configuration (DSC)", "implement-desired-state-configuration-dsc"),
            ("Implement Bicep", "implement-bicep"),
        ],
    },
    {
        "id": "path-deps",
        "num": 6,
        "h2": "Stratégie de gestion des dépendances",
        "weight": "5 modules · Avancé",
        "url": "https://learn.microsoft.com/fr-fr/training/paths/az-400-design-implement-dependency-management-strategy/",
        "intro": "Flux de packages, Azure Artifacts, migration et sécurité, contrôle de version sémantique, GitHub Packages.",
        "mods": [
            ("Explore package dependencies", "explore-package-dependencies"),
            ("Understand package management", "understand-package-management"),
            ("Migrate, consolidate, and secure artifacts", "migrate-consolidating-secure-artifacts"),
            ("Implement a versioning strategy", "implement-versioning-strategy"),
            ("Introduction to GitHub Packages", "introduction-github-packages"),
        ],
    },
    {
        "id": "path-feedback",
        "num": 7,
        "h2": "Commentaires continus",
        "weight": "5 modules · Avancé",
        "url": "https://learn.microsoft.com/fr-fr/training/paths/az-400-implement-continuous-feedback/",
        "intro": "Supervision, tableaux de bord, partage des connaissances, analytique automatisée, alertes et culture sans blâme.",
        "mods": [
            ("Implement tools to track usage and flow", "implement-tools-track-usage-flow"),
            ("Develop monitoring and status dashboards", "develop-monitor-status-dashboards"),
            ("Share knowledge within teams", "share-knowledge-within-teams"),
            ("Design processes to automate application analytics", "design-processes-automate-application-analytics"),
            ("Manage alerts, blameless retrospectives, just culture", "manage-alerts-blameless-retrospectives-just-culture"),
        ],
    },
    {
        "id": "path-sec",
        "num": 8,
        "h2": "Sécurité et conformité des bases de code",
        "weight": "4 modules · Avancé",
        "url": "https://learn.microsoft.com/fr-fr/training/paths/az-400-implement-security-validate-code-bases-compliance/",
        "intro": "DevSecOps : pipelines sécurisés, licences OSS, analyse de composition logicielle, Microsoft Defender pour le cloud, Azure Policy, GitHub Advanced Security.",
        "mods": [
            ("Introduction to Secure DevOps", "introduction-to-secure-devops"),
            ("Implement open-source software", "implement-open-source-software-azure"),
            ("Software Composition Analysis", "software-composition-analysis"),
            ("Security monitoring and governance", "security-monitoring-and-governance"),
        ],
    },
]


def module_block(
    mid: str,
    title: str,
    slug: str,
    *,
    locale: str,
    learn: dict,
    unit_excerpts: dict,
) -> str:
    """AZ-104-style module body: one paragraph with link, prose, inline objectives/prerequisites."""
    base = "https://learn.microsoft.com/en-us" if locale == "en" else "https://learn.microsoft.com/fr-fr"
    mod_url = f"{base}/training/modules/{slug}/"
    info = learn.get(slug, {})
    display_title = title
    if locale == "fr":
        display_title = info.get("title") or title
    summary = info.get("summary") or (
        "Open the module on Microsoft Learn for the official outline, labs, and knowledge check."
        if locale == "en"
        else "Ouvrez le module sur Microsoft Learn pour le plan officiel, les labos et la vérification des connaissances."
    )
    objectives = info.get("objectives") or []
    prereq = info.get("prerequisites") or []

    link = f'<a href="{mod_url}" target="_blank" rel="noopener">{html.escape(display_title)}</a>'
    if locale == "en":
        body = f"{link} — Microsoft Learn module. {html.escape(summary)}"
        if objectives:
            body += " Learning objectives: " + html.escape("; ".join(objectives))
        if prereq:
            body += " Prerequisites: " + html.escape("; ".join(prereq))
        aria_collapse = "Collapse section"
    else:
        body = f"{link} — Module Microsoft Learn. {html.escape(summary)}"
        if objectives:
            body += " Objectifs d'apprentissage : " + html.escape("; ".join(objectives))
        if prereq:
            body += " Prérequis : " + html.escape("; ".join(prereq))
        aria_collapse = "Réduire la section"

    unit_ps = ""
    for ex in unit_excerpts.get(slug, []):
        u = ex.get("url", "")
        utitle = html.escape(ex.get("title", "Unit"))
        utext = html.escape(ex.get("text", ""))
        unit_ps += f"""          <p><a href="{html.escape(u)}" target="_blank" rel="noopener">{utitle}</a>. {utext}</p>
"""

    return f'''          <div class="collapsible-block" data-block="{mid}">
            <h3 id="{mid}" class="block-title">{html.escape(display_title)} <button type="button" class="block-toggle" aria-label="{aria_collapse}">▼</button></h3>
            <div class="block-content">
          <p>{body}</p>
{unit_ps}            </div>
          </div>
'''


def path_section(p: dict, *, locale: str, learn: dict, unit_excerpts: dict) -> str:
    rows = ""
    for i, (title, slug) in enumerate(p["mods"], 1):
        disp = (learn.get(slug, {}).get("title") or title) if locale == "fr" else title
        rows += f"            <tr><td>{i}</td><td><a href=\"#{p['id']}-m{i}\">{html.escape(disp)}</a></td></tr>\n"
    blocks = ""
    for i, (title, slug) in enumerate(p["mods"], 1):
        mid = f"{p['id']}-m{i}"
        blocks += module_block(mid, title, slug, locale=locale, learn=learn, unit_excerpts=unit_excerpts)
    if locale == "en":
        path_line = f"Official path: <a href=\"{p['url']}\" target=\"_blank\" rel=\"noopener\">{html.escape(p['h2'])}</a>. {html.escape(p['intro'])}"
        th_mod = "Module"
    else:
        path_line = f"Parcours officiel : <a href=\"{p['url']}\" target=\"_blank\" rel=\"noopener\">{html.escape(p['h2'])}</a>. {html.escape(p['intro'])}"
        th_mod = "Module"
    return f'''        <section id="{p['id']}">
          <h2>{p['num']}. {html.escape(p['h2'])}</h2>
          <p class="weight">{html.escape(p['weight'])}</p>
          <p>{path_line}</p>
          <table>
            <tr><th>#</th><th>{th_mod}</th></tr>
{rows}          </table>
{blocks}        </section>
'''


def extract_git_main(locale: str) -> str:
    src = os.path.join(DIR, "az400.html") if locale == "en" else os.path.join(DIR, "fr", "az400-git-source.html")
    with open(src, "r", encoding="utf-8") as f:
        s = f.read()
    m = re.search(
        r'<section id="path-overview">(.*?)</section>\s*<section id="modules">(.*?)</section>',
        s,
        re.DOTALL,
    )
    if not m:
        raise SystemExit(f"Could not parse {src} — expected path-overview and modules sections")
    overview_inner = m.group(1)
    modules_inner = m.group(2)
    modules_inner = re.sub(r"<h2>\s*Modules\s*</h2>\s*", "", modules_inner, count=1)
    if locale == "en":
        overview_inner = overview_inner.replace(
            "<h2>AZ-400: Development for Enterprise DevOps</h2>",
            "<h2>1. Git &amp; Enterprise DevOps</h2>",
            1,
        )
        overview_inner = overview_inner.replace(
            '<p class="weight">Learning path: Git, Azure DevOps, GitHub — 8 modules · Advanced</p>',
            '<p class="weight">Learning path: Development for Enterprise DevOps · 8 modules · Advanced</p>',
        )
    else:
        overview_inner = overview_inner.replace(
            "<h2>AZ-400 : développement pour le DevOps d’entreprise</h2>",
            "<h2>1. Git et DevOps d’entreprise</h2>",
            1,
        )
        overview_inner = overview_inner.replace(
            '<p class="weight">Parcours d’apprentissage : Git, Azure DevOps, GitHub — 8 modules · Avancé</p>',
            '<p class="weight">Parcours : développement pour le DevOps d’entreprise · 8 modules · Avancé</p>',
        )
    return f'''        <section id="path-git">
{overview_inner}
{modules_inner}
        </section>
'''


def guide_overview(locale: str, paths_extra: list) -> str:
    if locale == "en":
        rows = (
            '<tr><td>1</td><td><a href="#path-git">Git &amp; Enterprise DevOps</a></td><td>Repos, branching, PRs, hooks, inner source, technical debt</td></tr>\n'
        )
        for p in paths_extra:
            rows += f"            <tr><td>{p['num']}</td><td><a href=\"#{p['id']}\">{html.escape(p['h2'])}</a></td><td>{html.escape(p['intro'][:120])}…</td></tr>\n"
        return f'''        <section id="guide-overview">
          <h2>AZ-400 study guide (all paths)</h2>
          <p class="weight">Microsoft Learn · Designing and Implementing Microsoft DevOps Solutions</p>
          <p>This single page collects eight AZ-400 learning paths in the same style as the <a href="az104.html">AZ-104 study guide</a>: one section per path, collapsible modules, fold/unfold, and dark/light theme. Open the official path links for hands-on labs and knowledge checks.</p>
          <p>Exam reference: <a href="https://learn.microsoft.com/en-us/certifications/exams/az-400/" target="_blank" rel="noopener">AZ-400 exam</a>.</p>
          <p><a href="fr/az400-all.html">Version française</a></p>
          <table>
            <tr><th>#</th><th>Path</th><th>Topics (short)</th></tr>
{rows}          </table>
        </section>
'''
    rows = (
        '<tr><td>1</td><td><a href="#path-git">Git et DevOps d’entreprise</a></td><td>Référentiels, branches, PR, hooks, inner source, dette technique</td></tr>\n'
    )
    for p in paths_extra:
        rows += f"            <tr><td>{p['num']}</td><td><a href=\"#{p['id']}\">{html.escape(p['h2'])}</a></td><td>{html.escape(p['intro'][:120])}…</td></tr>\n"
    return f'''        <section id="guide-overview">
          <h2>Guide d’étude AZ-400 (tous les parcours)</h2>
          <p class="weight">Microsoft Learn · Concevoir et implémenter des solutions Microsoft DevOps</p>
          <p>Cette page unique regroupe huit parcours AZ-400 sur le même modèle que le <a href="az104.html">guide AZ-104</a> : une section par parcours, modules repliables, tout replier / tout déplier, thème clair ou sombre. Ouvrez les liens de parcours officiels pour les labos et les vérifications des connaissances.</p>
          <p>Référence examen : <a href="https://learn.microsoft.com/fr-fr/certifications/exams/az-400/" target="_blank" rel="noopener">examen AZ-400</a>.</p>
          <p><a href="../az400-all.html">English version</a></p>
          <table>
            <tr><th>#</th><th>Parcours</th><th>Sujets (résumé)</th></tr>
{rows}          </table>
        </section>
'''


def read_head(locale: str) -> str:
    with open(os.path.join(DIR, "az400.html"), "r", encoding="utf-8") as f:
        s = f.read()
    head = re.search(r"^(<!DOCTYPE.*?</head>)", s, re.DOTALL)
    if not head:
        raise SystemExit("no head")
    h = head.group(1)
    if locale == "en":
        h = h.replace(
            "<title>AZ-400: Git &amp; Enterprise DevOps — Study Guide</title>",
            "<title>AZ-400 complete study guide — Microsoft Learn paths</title>",
        )
        h = h.replace(
            'content="Study notes for the Microsoft Learn path AZ-400: Development for Enterprise DevOps (Git, Azure DevOps, GitHub)."',
            'content="AZ-400 DevOps: all Microsoft Learn paths in one page — Git, CI/CD, release, IaC, dependencies, feedback, security."',
        )
    else:
        h = h.replace("<html lang=\"en\">", "<html lang=\"fr\">")
        h = h.replace(
            "<title>AZ-400: Git &amp; Enterprise DevOps — Study Guide</title>",
            "<title>Guide d’étude AZ-400 complet — Parcours Microsoft Learn</title>",
        )
        h = h.replace(
            'content="Study notes for the Microsoft Learn path AZ-400: Development for Enterprise DevOps (Git, Azure DevOps, GitHub)."',
            'content="AZ-400 DevOps : tous les parcours Microsoft Learn sur une page — Git, CI/CD, mise en production, IaC, dépendances, commentaires, sécurité."',
        )
    return h


def read_script(locale: str) -> str:
    with open(os.path.join(DIR, "az400.html"), "r", encoding="utf-8") as f:
        s = f.read()
    m = re.search(
        r"(<script>\s*\(function\(\)\s*\{\s*var THEME_KEY = \"az400-theme\".*?</script>\s*</body>\s*</html>)",
        s,
        re.DOTALL,
    )
    if not m:
        raise SystemExit("no footer script in az400.html")
    script = m.group(1)
    if locale == "fr":
        script = script.replace("Switch to light mode", "Passer en mode clair")
        script = script.replace("Switch to dark mode", "Passer en mode sombre")
        script = script.replace("Close menu", "Fermer le menu")
        script = script.replace("Open menu", "Ouvrir le menu")
        script = script.replace("Expand section", "Développer la section")
        script = script.replace("Collapse section", "Réduire la section")
    return script


NAV = '''  <header class="top-nav" id="topNav">
    <a href="az400-all.html" class="site-title">AZ-400 Study Guide</a>
    <button type="button" class="menu-toggle" id="menuToggle" aria-label="Open menu">☰</button>
    <div class="nav-wrap">
      <ul class="nav-links">
        <li><a href="../index.html" class="back-link">← Back to portfolio</a></li>
        <li><a href="az104.html">AZ-104 guide</a></li>
        <li><a href="#guide-overview">Overview</a></li>
        <li><a href="#path-git">1. Git</a></li>
        <li><a href="#path-ci">2. CI</a></li>
        <li><a href="#path-release">3. Release</a></li>
        <li><a href="#path-securecd">4. Secure CD</a></li>
        <li><a href="#path-iac">5. IaC</a></li>
        <li><a href="#path-deps">6. Deps</a></li>
        <li><a href="#path-feedback">7. Feedback</a></li>
        <li><a href="#path-sec">8. Security</a></li>
        <li><a href="fr/az400-all.html">Version française</a></li>
      </ul>
      <div class="nav-right">
        <button type="button" class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode" title="Toggle dark/light mode">☀</button>
      </div>
    </div>
  </header>
'''

NAV_FR = '''  <header class="top-nav" id="topNav">
    <a href="az400-all.html" class="site-title">Guide AZ-400</a>
    <button type="button" class="menu-toggle" id="menuToggle" aria-label="Ouvrir le menu">☰</button>
    <div class="nav-wrap">
      <ul class="nav-links">
        <li><a href="../../index.html" class="back-link">← Retour au portfolio</a></li>
        <li><a href="../az104.html">Guide AZ-104 (EN)</a></li>
        <li><a href="az104.html">Guide AZ-104 (FR)</a></li>
        <li><a href="#guide-overview">Vue d’ensemble</a></li>
        <li><a href="#path-git">1. Git</a></li>
        <li><a href="#path-ci">2. CI</a></li>
        <li><a href="#path-release">3. Mise en prod.</a></li>
        <li><a href="#path-securecd">4. Déploiement sécurisé</a></li>
        <li><a href="#path-iac">5. IaC</a></li>
        <li><a href="#path-deps">6. Dépendances</a></li>
        <li><a href="#path-feedback">7. Commentaires</a></li>
        <li><a href="#path-sec">8. Sécurité</a></li>
        <li><a href="../az400-all.html">AZ-400 (EN)</a></li>
      </ul>
      <div class="nav-right">
        <button type="button" class="theme-toggle" id="themeToggle" aria-label="Basculer le mode sombre" title="Basculer clair / sombre">☀</button>
      </div>
    </div>
  </header>
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--locale", choices=("en", "fr"), default="en")
    args = ap.parse_args()
    locale = args.locale

    if locale == "fr":
        from az400_learn_snippets_fr import LEARN as learn_d
        from az400_learn_unit_excerpts_fr import UNIT_EXCERPTS as unit_d

        paths_extra = PATHS_EXTRA_FR
        nav = NAV_FR
        out_path = os.path.join(DIR, "fr", "az400-all.html")
        fold_fold = '          <button type="button" id="foldAll" aria-label="Tout replier">Tout replier</button>\n'
        fold_unfold = '          <button type="button" id="unfoldAll" aria-label="Tout déplier">Tout déplier</button>\n'
    else:
        from az400_learn_snippets import LEARN as learn_d
        from az400_learn_unit_excerpts import UNIT_EXCERPTS as unit_d

        paths_extra = PATHS_EXTRA
        nav = NAV
        out_path = os.path.join(DIR, "az400-all.html")
        fold_fold = '          <button type="button" id="foldAll" aria-label="Collapse all sections">Fold all</button>\n'
        fold_unfold = '          <button type="button" id="unfoldAll" aria-label="Expand all sections">Unfold all</button>\n'

    parts = [
        read_head(locale).rstrip() + "\n<body>\n",
        nav,
        '  <div class="layout">\n    <div class="main-wrap">\n      <main>\n',
        '        <div class="fold-unfold">\n',
        fold_fold,
        fold_unfold,
        "        </div>\n",
        guide_overview(locale, paths_extra),
        extract_git_main(locale),
    ]
    for p in paths_extra:
        parts.append(path_section(p, locale=locale, learn=learn_d, unit_excerpts=unit_d))
    parts.append("      </main>\n    </div>\n  </div>\n\n")
    parts.append(read_script(locale))
    out = "".join(parts)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)
    print("Wrote", out_path, "chars", len(out))


if __name__ == "__main__":
    main()
