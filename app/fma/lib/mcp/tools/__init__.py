import pkgutil
import importlib
from pathlib import Path
from . import prompts

# Dieser Block findet automatisch alle .py Files in diesem Ordner
# und importiert sie, was die Decorators triggert.
path = Path(__file__).parent
for loader, module_name, is_pkg in pkgutil.iter_modules([str(path)]):
    # Importiert das Modul relativ zum aktuellen Package
    importlib.import_module(f".{module_name}", package=__package__)