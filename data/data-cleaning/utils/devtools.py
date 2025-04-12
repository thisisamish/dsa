import importlib
import sys
from IPython.core.magic import register_line_magic

@register_line_magic
def reloadmypkg(line):
    """
    Jupyter line magic to reload a package and all its submodules.
    Usage:
        %reloadmypkg mypackage
    """
    package_name = line.strip()
    if not package_name:
        print("Usage: %reloadmypkg mypackage")
        return

    try:
        pkg = sys.modules.get(package_name)
        if not pkg:
            pkg = importlib.import_module(package_name)

        importlib.reload(pkg)

        for name in list(sys.modules):
            if name.startswith(package_name + "."):
                importlib.reload(sys.modules[name])

        print(f"✅ Reloaded package '{package_name}' and its submodules.")
    except Exception as e:
        print(f"❌ Error reloading package '{package_name}': {e}")
