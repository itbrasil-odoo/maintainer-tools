# License AGPLv3 (https://www.gnu.org/licenses/agpl-3.0-standalone.html)
# Copyright (c) 2019 Eficent Business and IT Consulting Services S.L.
#        (http://www.eficent.com)

import os
import subprocess
import sys

from tools.itbr_gen_addon_icon import ICON_TYPE, ICONS_DIR


def test_gen_addon_icon(tmp_path):
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
    ]
    subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    assert os.path.exists(
        os.path.join(addon_dir._str, ICONS_DIR, "icon.%s" % ICON_TYPE)
    )
