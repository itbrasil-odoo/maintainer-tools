# -*- coding: utf-8 -*-
# License AGPLv3 (https://www.gnu.org/licenses/agpl-3.0-standalone.html)
"""
itbr-repo-manage

Manage repositories and teams based on YAML configuration files.

"""

from __future__ import print_function

import os
import yaml
import click

try:
    from .itbr_github_login import login
except ImportError:
    from itbr_github_login import login


def load_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


@click.command()
@click.option("--org", required=True, help="GitHub organization")
@click.option("--token", help="GitHub token")
@click.option("--conf-dir", required=True, help="Configuration directory")
def main(org, token, conf_dir):
    # Load global config
    global_config = load_yaml(os.path.join(conf_dir, "global.yml"))
    org = global_config.get("org", org)

    # Login to GitHub
    login()

    # Load PSC configs
    psc_dir = os.path.join(conf_dir, "psc")
    for psc_file in os.listdir(psc_dir):
        if psc_file.endswith(".yml"):
            psc_config = load_yaml(os.path.join(psc_dir, psc_file))
            for team_name, team_data in psc_config.items():
                print(f"Processing team: {team_name}")
                # TODO: Create or update team

    # Load repo configs
    repo_dir = os.path.join(conf_dir, "repo")
    for repo_file in os.listdir(repo_dir):
        if repo_file.endswith(".yml"):
            repo_config = load_yaml(os.path.join(repo_dir, repo_file))
            for repo_name, repo_data in repo_config.items():
                print(f"Processing repo: {repo_name}")
                # TODO: Create or update repo

    print("Repo manage completed.")


if __name__ == "__main__":
    main()
