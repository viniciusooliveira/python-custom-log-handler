import logging
import threading
import time
from datetime import datetime
from logging import LogRecord


class CustomBufferingHandler(logging.Handler):

    def __init__(self, time=10, capacity=10, max_buffer_size=100):
        """
        :param time: max time between flushes in seconds
        :param capacity: max buffer capacity before flush
        :param max_buffer_size: max buffer size before dropping logs
        """
        self._time = time
        self._capacity = capacity
        self._max_buffer_size = max_buffer_size
        self._last_sent_time = datetime.now()

        self._buffer = []
        self._buffer_lock = threading.Lock()
        self._stopping = False

        self._thread = None
        self._start()

        logging.Handler.__init__(self)

    def emit(self, record: LogRecord) -> None:
        """
        Overrides base emit, saving the LogRecord to the internal buffer.
        """
        if len(self._buffer) >= self._max_buffer_size:
            self._buffer.pop(0)
        self._buffer.append(record)

    def close(self) -> None:
        """
        Overrides base close, gracefully stopping the _monitor, without losing log records.
        """
        self._stopping = True
        self._thread.join()
        logging.Handler.close(self)

    def _start(self) -> None:
        """
        Start the monitor thread.
        """
        self._thread = threading.Thread(target=self._monitor, daemon=False)
        self._thread.start()

    def _monitor(self) -> None:
        """
        Monitor thread, verifies if it should flush and calls flush function.
        Keeps doing this while its not stopping or the buffer has logs.
        """
        while not self._stopping or len(self._buffer) > 0:
            if self._should_flush():
                self._flush()
            time.sleep(1)

    def _flush(self) -> None:
        """
        Empties the buffer and call the send function.
        If a error occurs on send, reinserts the logs into the buffer.
        """
        self._buffer_lock.acquire()
        records = self._buffer
        self._buffer = []
        self._buffer_lock.release()

        if not self._send(records):
            self._buffer_lock.acquire()
            self._buffer.extend(records)
            self._buffer_lock.release()

        self._last_sent_time = datetime.now()

    def _send(self, records) -> bool:
        """
        Sends the log records to the final destination.
        In this example just print into the console.
        """
        print([x.getMessage() for x in records])
        return True

    def _should_flush(self) -> bool:
        """
        Tells monitor if should call flush.
        """
        return (self._stopping
                or len(self._buffer) >= self._capacity
                or (datetime.now() - self._last_sent_time).seconds >= self._time)
