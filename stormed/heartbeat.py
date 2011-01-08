import time

from stormed.frame import status

class HeartbeatMonitor(object):

    def __init__(self, connection):
        self.conn = connection
        self.timeout = connection.heartbeat * 2
        self.when = None

    def start(self):
        self._schedule()

    def _schedule(self):
        when = time.time() + self.timeout
        self.conn.io_loop.add_timeout(when, self._check)
        self.when = when

    def _check(self):
        if self.conn.status != status.CLOSED:
            last_received = self.conn.last_received_frame
            if not last_received or (self.when - last_received) > self.timeout:
                self.conn.close_stream()
                if self.conn.on_disconnect:
                    self.conn.on_disconnect()
            else:
                self._schedule()
