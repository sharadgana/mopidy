from mopidy.frontends.mpd.protocol import handle_pattern
from mopidy.frontends.mpd.exceptions import MpdNotImplemented

@handle_pattern(r'^disableoutput "(?P<outputid>\d+)"$')
def disableoutput(frontend, outputid):
    """
    *musicpd.org, audio output section:*

        ``disableoutput``

        Turns an output off.
    """
    raise MpdNotImplemented # TODO

@handle_pattern(r'^enableoutput "(?P<outputid>\d+)"$')
def enableoutput(frontend, outputid):
    """
    *musicpd.org, audio output section:*

        ``enableoutput``

        Turns an output on.
    """
    raise MpdNotImplemented # TODO

@handle_pattern(r'^outputs$')
def outputs(frontend):
    """
    *musicpd.org, audio output section:*

        ``outputs``

        Shows information about all outputs.
    """
    outputs = []
    for output in frontend.gstreamer.list_outputs().get():
        outputs.extend([
            ('outputid', output.index),
            ('outputname', output.name),
            ('outputenabled', int(output.enabled)),
        ])
    return outputs
