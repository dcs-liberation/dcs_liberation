from .a4ec import *
from .f104 import *
from .f22a import *
from .frenchpack import *
from .hercules import *
from .highdigitsams import *
from .jas39 import *
from .su57 import *
from .uh60l import *
from .ov10a import *


def load_mods() -> None:
    """Loads all mods.

    Note that this function doesn't *do* anything. Its purpose is to prevent editors
    from removing `import pydcs_extensions` when it is "unused", because mod imports
    have side effects (unit types are registered with pydcs).
    """
