- La section Maze Generation dit que le package vient « de 42 school ». Le sujet parle d'un package assigné par un plique comment ton code s'adapte à son interface.


16. Docstrings manquantes (III.1, PEP257). 43 classes ou fonctions publiques n'en ont pas, par exemple toutes les ost, read_json et push_json. Pour les lister : ruff check src --select D101,D102,D103.


22. Petits bugs de logique
    - level.py:294-295 : code mort.
    - src/engine/level.py:58 : le test is None est inutile.

23. try/except ImportError autour de la bibliothèque standard (json, argparse…). C'est du bruit, et ça cache de vraies erreurs d'import.

