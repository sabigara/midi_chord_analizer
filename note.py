class Note:
    def __init__(self, number, start, end):
        self.number = int(number)
        self.start = int(start)
        self.end = int(end)
        self.symbol = self.num_to_symbol()

    def __str__(self):
        return f'{self.symbol}({self.number})  {self.start} - {self.end}'

    def get_duplication_rate(self, measure_start, measure_end):
        if self.start <= measure_start and self.end >= measure_end:
            return 1

        if self.start <= measure_start and self.end >= measure_start and self.end <= measure_end:
            return (self.end - measure_start) / (measure_end - measure_start)

        if self.start >= measure_start and self.start <= measure_end and self.end >= measure_end:
            return (measure_end - self.start) / (measure_end - measure_start)

        if self.start >= measure_start and self.start <= measure_end \
        and self.end >= measure_start and self.end <= measure_end:
            return (self.end - self.start) / (measure_end - measure_start)

    def num_to_symbol(self):
        if self.number in range(0, 150, 12):
            return "C"
        if self.number in range(1, 150, 12):
            return "C#"
        if self.number in range(2, 150, 12):
            return "D"
        if self.number in range(3, 150, 12):
            return "D#"
        if self.number in range(4, 150, 12):
            return "E"
        if self.number in range(5, 150, 12):
            return "F"
        if self.number in range(6, 150, 12):
            return "F#"
        if self.number in range(7, 150, 12):
            return "G"
        if self.number in range(8, 150, 12):
            return "G#"
        if self.number in range(9, 150, 12):
            return "A"
        if self.number in range(10, 150, 12):
            return "A#"
        if self.number in range(11, 150, 12):
            return "B"


class Chord:
    def __init__(self, *args):
        self.notes = args