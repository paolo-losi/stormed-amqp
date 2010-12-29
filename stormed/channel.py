from stormed.util import Enum
from stormed.method.channel import Open, status
from stormed.method import exchange

class Channel(object):

    def __init__(self, channel_id, conn):
        self.channel_id = channel_id
        self.conn = conn
        self.status = status.CLOSED
        self._task_queue = []
        #TODO as a property
        self.on_tasks_completed = None

    def open(self):
        self._add_task(Open(out_of_band=''))

    def exchange_declare(self, name, type="direct", durable=False):
        self._add_task(exchange.Declare(ticket      = 0,
                                        exchange    = name,
                                        type        = type,
                                        passive     = False,
                                        durable     = durable,
                                        auto_delete = False,
                                        internal    = False,
                                        nowait      = False,
                                        arguments   = dict()))

    #TODO do we need FrameHandler class?
    def handle_frame(self, frame):
        method = frame.payload
        if hasattr(method, 'handle'):
            method.handle(self)
            #FIXME verify if the answer is the one we're expecting
            self._task_queue.pop(0)
            self._run_tasks()
        else:
            #TODO better error reporting/handling
            print "ERROR: %r not handled" % method._name

    def _add_task(self, task):
        pending = len(self._task_queue)
        self._task_queue.append(task)
        if not pending:
            self._run_tasks()

    def _run_tasks(self):
        if self._task_queue:
            task = self._task_queue[0]
            self.conn.write_method(task, channel=self.channel_id)
        else:
            if self.on_tasks_completed is not None:
                self.on_tasks_completed()
                self.on_tasks_completed = None
