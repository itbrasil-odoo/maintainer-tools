# License AGPLv3 (https://www.gnu.org/licenses/agpl-3.0-standalone.html)
# Copyright (c) 2019 Eficent Business and IT Consulting Services S.L.
#        (http://www.eficent.com)

import os
import subprocess
import sys

import pytest

from tools.itbr_gen_addon_icon import ICON_TYPE, ICONS_DIR, ORG_ICONS_DIR


def _gen_icon(tmp_path, *extra_args):
    addon_dir = tmp_path / "addon"
    addon_dir.mkdir()
    with (addon_dir / "__manifest__.py").open("w") as f:
        f.write("{'name': 'addon'}")
    cmd = [
        sys.executable,
        "-m",
        "tools.itbr_gen_addon_icon",
        "--addon-dir",
        str(addon_dir),
        *extra_args,
    ]
    subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    return os.path.join(addon_dir._str, ICONS_DIR, "icon.%s" % ICON_TYPE)


def _bundled_icon(org):
    with open(os.path.join(ORG_ICONS_DIR, org, "icon.%s" % ICON_TYPE), "rb") as f:
        return f.read()


def test_gen_addon_icon(tmp_path):
    icon = _gen_icon(tmp_path)
    assert os.path.exists(icon)
    with open(icon, "rb") as f:
        assert f.read() == _bundled_icon("default")


@pytest.mark.parametrize(
    "org_name, expected_org",
    [("Dedicata", "dedicata"), ("itbrasil-odoo", "default"), ("OCA", "default")],
)
def test_gen_addon_icon_org_name(tmp_path, org_name, expected_org):
    icon = _gen_icon(tmp_path, "--org-name", org_name)
    with open(icon, "rb") as f:
        assert f.read() == _bundled_icon(expected_org)
    assert _bundled_icon("dedicata") != _bundled_icon("default")
