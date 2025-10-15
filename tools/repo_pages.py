# -*- coding: utf-8 -*-
# License AGPLv3 (https://www.gnu.org/licenses/agpl-3.0-standalone.html)
"""
itbr-repo-pages

Generate RST files for repositories and teams based on YAML configuration files.

"""

from __future__ import print_function

import os
import yaml
import click
from collections import defaultdict


def load_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


@click.command()
@click.option("--org", required=True, help="GitHub organization")
@click.option("--conf-dir", required=True, help="Configuration directory")
@click.option("--path", required=True, help="Output path for RST files")
def main(org, conf_dir, path):
    # Load global config
    global_config = load_yaml(os.path.join(conf_dir, "global.yml"))
    title = global_config.get("title", "Repository Structure")

    # Load PSC configs (teams)
    psc_dir = os.path.join(conf_dir, "psc")
    teams = {}
    for psc_file in os.listdir(psc_dir):
        if psc_file.endswith(".yml"):
            psc_config = load_yaml(os.path.join(psc_dir, psc_file))
            teams.update(psc_config)

    # Load repo configs
    repo_dir = os.path.join(conf_dir, "repo")
    repos = {}
    categories = defaultdict(list)
    for repo_file in os.listdir(repo_dir):
        if repo_file.endswith(".yml"):
            repo_config = load_yaml(os.path.join(repo_dir, repo_file))
            for repo_name, repo_data in repo_config.items():
                repos[repo_name] = repo_data
                category = repo_data.get("category", "Other")
                categories[category].append((repo_name, repo_data))

    # Generate teams.rst
    teams_rst = f"{title} - Teams\n{'=' * (len(title) + 7)}\n\n"
    for team_name, team_data in sorted(teams.items()):
        teams_rst += f"{team_data['name']}\n{'-' * len(team_data['name'])}\n\n"
        if team_data.get("members"):
            teams_rst += "Members:\n\n"
            for member in team_data["members"]:
                teams_rst += f"* @{member}\n"
            teams_rst += "\n"
        if team_data.get("representatives"):
            teams_rst += "Representatives:\n\n"
            for rep in team_data["representatives"]:
                teams_rst += f"* @{rep}\n"
            teams_rst += "\n"
        teams_rst += "\n"

    with open(os.path.join(path, "teams.rst"), "w") as f:
        f.write(teams_rst)

    # Generate repos.rst
    repos_rst = f"{title} - Repositories\n{'=' * (len(title) + 15)}\n\n"
    for category in sorted(categories.keys()):
        repos_rst += f"{category}\n{'-' * len(category)}\n\n"
        for repo_name, repo_data in sorted(categories[category]):
            repos_rst += f"{repo_data['name']}\n{'~' * len(repo_data['name'])}\n\n"
            repos_rst += (
                f"* Repository: `{repo_name} <https://github.com/{org}/{repo_name}>`_\n"
            )
            repos_rst += f"* PSC: {repo_data.get('psc', 'N/A')}\n"
            if repo_data.get("default_branch"):
                repos_rst += f"* Default branch: {repo_data['default_branch']}\n"
            if repo_data.get("branches"):
                repos_rst += f"* Branches: {', '.join(repo_data['branches'])}\n"
            repos_rst += "\n"

    with open(os.path.join(path, "repos.rst"), "w") as f:
        f.write(repos_rst)

    print("RST files generated.")


if __name__ == "__main__":
    main()
