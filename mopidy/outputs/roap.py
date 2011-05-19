from mopidy import settings
from mopidy.outputs import BaseOutput

class ROAPOutput(BaseOutput):
    def describe_bin(self):
        if settings.ROAP_OUTPUT_OVERRIDE:
            return settings.ROAP_OUTPUT_OVERRIDE
        return 'apexsink name=roap'

    def modify_bin(self, output):
        if settings.ROAP_OUTPUT_OVERRIDE:
            return

        self.set_properties(output.get_by_name('roap'), {
            u'host': settings.ROAP_OUTPUT_SERVER,
            u'port': settings.ROAP_OUTPUT_PORT
        })
