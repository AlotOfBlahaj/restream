from abc import ABCMeta, abstractmethod
from multiprocessing import Process


class VideoDaemon(Process, metaclass=ABCMeta):
    def __init__(self, target_id):
        super().__init__()
        self.target_id = target_id

    def run(self) -> None:
        try:
            self.check()
        except KeyboardInterrupt:
            exit(0)

    @abstractmethod
    def check(self):
        pass
