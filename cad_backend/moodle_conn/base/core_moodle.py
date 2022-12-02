

class MoodleCore:

    def __init__(self, moodle):
        self._moodle = moodle

    @property
    def moodle(self):
        return self._moodle

    # @abc.abstractclassmethod
    # def __call__(self, *args, **kwds):
    #     return super().__call__(*args, **kwds)
