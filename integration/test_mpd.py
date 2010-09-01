import socket
import select

from glob import glob
from os import remove
from os.path import dirname, join
from subprocess import Popen
from tempfile import mkstemp
from time import sleep

TARGET_PORT = 6601

integration_folder = dirname(__file__)
replay_folder = join(integration_folder, 'replays')
mpd_folder = join(integration_folder, 'mpd')

mpd_process = None
config_name = None

def setup():
    global mpd_process
    global config_name

    base_config = open(join(mpd_folder, 'mpd.conf')).read()
    base_config = base_config.replace('$path', integration_folder)

    config_name = mkstemp()[1]
    config = open(config_name, 'w')
    config.write(base_config)
    config.flush()

    mpd_process = Popen(['mpd', '--no-create-db', '--no-daemon',
        '--stdout', '--verbose', config_name])

    sleep(1)

def teardown():
    if mpd_process:
        mpd_process.terminate()
        sleep(1)
    if config_name:
        remove(config_name)

def test_replates():
    for replay in glob(join(replay_folder, '*')):
        yield check_replay, replay

def check_replay(replay):
    connection = get_connection()

    for send, recv in parse_data(replay):
        assert_response(connection, send, recv)

def get_connection():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect(('', TARGET_PORT))
    return connection

def parse_data(path):
    previous, send, expected = '', '', ''

    for current in open(path).readlines():
        if is_recv(previous) and is_send(current):
            yield (send, expected)
            send, expected = '', ''

        if is_send(current):
            send += current[2:]
        elif is_recv(current):
            expected += current[2:]

        previous = current

    yield (send, expected)

def is_send(line):
    return line.startswith('> ')

def is_recv(line):
    return line.startswith('< ')

def assert_response(sock, send, expect):
    if send:
        sock.send(send)
    actual = ''
    while select.select([sock], [], [], 0.1)[0]:
        actual += sock.recv(8192)
    assert expect == actual, '%s != %s' % (repr(expect), repr(actual))
