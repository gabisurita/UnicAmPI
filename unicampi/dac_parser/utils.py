from __future__ import unicode_literals, division

import datetime


def get_current_semester():
    today = datetime.date.today()
    semester = today.month // 6 + 1
    return today.year, semester


class ContentFinder(object):
    def __init__(self, data, separator='\n'):
        self.data = data
        self.splited = [s.strip() for s in data.split(separator) if s.strip()]

    def find_by_content(self, pattern, offset=0, count=None,
                        end_pattern=None):
        for piece, i in zip(self.splited, range(len(self.splited))):
            if pattern in piece:
                start_idx = i
                break

        if count:
            return self.splited[start_idx + offset:start_idx + count]

        elif end_pattern:
            for piece, i in zip(self.splited[start_idx:],
                                range(start_idx, len(self.splited))):
                if end_pattern in piece:
                    end_idx = i
                    break

            return self.splited[start_idx + offset:end_idx]

        else:
            return self.splited[start_idx + offset]
