from .base_plugin import BasePlugin
from .veaf_plugin import VeafPlugin
from .jtacautolase_plugin import JtacAutolasePlugin
from .liberation_plugin import LiberationPlugin

INSTALLED_PLUGINS={
    "VeafPlugin": VeafPlugin(),
    "JtacAutolasePlugin": JtacAutolasePlugin(),
    "LiberationPlugin": LiberationPlugin(),
}
