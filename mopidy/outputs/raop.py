from mopidy import settings
from mopidy.outputs import BaseOutput

class RaopOutput(BaseOutput):
    def describe_bin(self):
        return 'apexsink name=raop'

    def modify_bin(self):
        raop = self.bin.get_by_name('raop')
        self.set_properties(raop, {
            u'host': settings.RAOP_OUTPUT_SERVER,
            u'port': settings.RAOP_OUTPUT_PORT,,
        })
