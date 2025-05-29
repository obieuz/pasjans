import threading
import time


class Timer:
    def __init__(self):
        self._seconds = 0
        self.running = True

    def start_timer(self):
        def update_time():
            while self.running:
                time.sleep(1)
                self._seconds += 1

        timer_thread = threading.Thread(target=update_time, daemon=True)
        timer_thread.start()

    def stop_timer(self):
        self.running = False

    def reset_timer(self):
        self._seconds = 0

    def get_time(self):
        return self._seconds
