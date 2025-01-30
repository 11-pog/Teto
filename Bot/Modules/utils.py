import zc.lockfile

class Utils:
    @staticmethod
    def is_duplicate(lock_name):
        try:
            lock = zc.lockfile.LockFile(lock_name)
            return lock
        except zc.lockfile.LockError:
            return None

