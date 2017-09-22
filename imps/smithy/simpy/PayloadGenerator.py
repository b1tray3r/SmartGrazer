from imps.smithy.simpy.RandomStringGenerator import RandomStringGenerator


class PayloadGenerator(object):
    config = None

    def applyConfig(self, configuration):
        self.config = configuration

    def generate(self):
        payloads = []

        if self.config["checks"]['keywords']:
            payloads.append(self._getKeyWords())

        if self.config["checks"]['max_get_length']:
            payloads.append(self._getLongRandomString())

        if self.config["checks"]['specialchars']:
            payloads.append(self._getSpecialCharsString())

        if self.config["checks"]['jsfuck']:
            payloads.append(self._getJSFUCKCharsString())

        if self.config["checks"]['chars']:
            payloads.append(self._getRandomString(RandomStringGenerator.MIXEDCASE))

        return payloads

    def _getRandomString(self, type):
        stringconf = self.config['stringgenerator']['length']
        rs = RandomStringGenerator(stringconf['min'], stringconf['max'])
        return rs.get(type).encode()

    def _getLongRandomString(self, type=RandomStringGenerator.MIXEDCASE):
        rs = RandomStringGenerator(1000, 16000)
        return rs.get(type).encode()

    def _getSpecialCharsString(self):
        chars = ''
        for digit in self.config['stringgenerator']['specialchars']:
            chars = chars + chr(digit)

        return chars

    def _getJSFUCKCharsString(self):
        return b'()[]!+'

    def _getKeyWords(self):
        return "<img /> <IMG /> src SRC javascript alert xss script SCRIPT <a onerror </body> <iframe <input style= onload="