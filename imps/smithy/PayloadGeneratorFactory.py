import importlib

from imps.confy.JSONConfigManager import JSONConfigManager
from imps.smithy.Elements import Elements


class PayloadGeneratorFactory(object):
    """ This class acts like a factory for the actual PayloadGenerators.

        By running generate() the configured PayloadGenerator-Instance will be imported, instantiated and executed.
    """
    _impName = ''
    _config = {}
    _impConfig = {}

    _instances = {}

    def __init__(self, configuration):
        self._config = configuration
        self._impName = self._config["smithy"]["generator"]

    def getImpString(self, name):
        self._impConfig = self._config[name]

        return "imps.smithy.{0}".format(name)

    def _getGenerator(self, name):
        """
            This method instantiates the generator instance on the first call.

            Later calls will return the requested instance.

            :param name: Name of the generator module.
            :return:  `PayloadGenerator`
        """
        if not name in self._instances.keys():
            module = importlib.import_module(self.getImpString(name) + ".PayloadGenerator")
            generator = module.PayloadGenerator()
            generator.applyConfig(self._impConfig)

            elements = Elements(self._config["smithy"]["elements"]["usages"])
            elements.setDefaultLifes((JSONConfigManager(self._config["smithy"]["elements"]["lifes"])).getConfig())

            generator.setElements(elements)
            self._instances[name] = generator

        return self._instances[name]

    def adjustElements(self, elements):
        self._getGenerator(self._impName).adjustElements(elements)

    def getSimpy(self):
        return self._getGenerator("simpy")

    def generate(self):
        return self._getGenerator(self._impName).generate()
