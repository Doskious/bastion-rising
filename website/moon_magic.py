from website.krynndatetime import date as kdate, timedelta as ktimedelta


INITIAL_DATE = kdate(351, 9, 13)


def hyphen_range(s):
    """ yield each integer from a complex range string like "1-9,12, 15-20,23"

    >>> list(hyphen_range('1-9,12, 15-20,23'))
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 15, 16, 17, 18, 19, 20, 23]

    >>> list(hyphen_range('1-9,12, 15-20,2-3-4'))
    Traceback (most recent call last):
        ...
    ValueError: format error in 2-3-4
    """
    for x in s.split(','):
        elem = x.split('-')
        if len(elem) == 1:  # a number
            yield int(elem[0])
        elif len(elem) == 2:  # a range inclusive
            start, end = map(int, elem)
            for i in xrange(start, end + 1):
                yield i
        else:  # more than one hyphen
            raise ValueError('format error in %s' % x)


def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]


class Moon(object):
    def __init__(self, name, pd, ip):
        super(Moon, self).__init__()
        self.name = name
        self.period = pd
        self.initial_position = ip
        phase_days = list(hyphen_range('0-{}'.format(self.period - 1)))
        for index, day_val in enumerate(phase_days):
            phase_days[index] = ((day_val + self.period) - (self.period / 8)) % self.period
        self.phase_sections = chunks(phase_days, self.period / 4)
        self.phase_bounds = ['Low Sanction', 'Waxing', 'High Sanction', 'Waning']
    def phase(self, date):
        daydiff = (date - INITIAL_DATE).days
        position = (self.initial_position + daydiff) % self.period
        for index, phase_days in enumerate(self.phase_sections):
            if position in phase_days:
                return self.phase_bounds[index]


Solinari = Moon('Solinari', 36, 28)
Lunitari = Moon('Lunitari', 28, 15)
Nuitari = Moon('Nuitari', 8, 6)
MOONS = [Solinari, Lunitari, Nuitari]


class Order(object):
    def __init__(self, name, moon_id):
        super(Order, self).__init__()
        self.name = name
        self.moon = MOONS[moon_id]
    def moon_magic(self, date):
        bonus = 0
        in_needed = ""
        phases = {}
        for index, moon in enumerate(MOONS):
            phases[moon.name] = moon.phase(date)
        my_moon_phase = phases[self.moon.name]
        if 'High' in my_moon_phase:
            bonus += 1
            in_needed = "in "
        elif 'Low' in my_moon_phase:
            bonus -= 1
            in_needed = "in "
        for moon_name in phases:
            if moon_name != self.moon.name and phases[moon_name] == my_moon_phase:
                bonus += 1
        return "{} ({} is {}{})".format(bonus, self.moon.name, in_needed, my_moon_phase)


White = Order('White Robes', 0)
Red = Order('Red Robes', 1)
Black = Order('Black Robes', 2)
ORDERS = [White, Red, Black]


def Moon_Magic(date):
    if type(date) is tuple:
        date = kdate(*date)
    elif type(date) is int:
        date = INITIAL_DATE + ktimedelta(days=date-1)
    elif not type(date) is kdate:
        raise ValueError("Invalid date format.")
    retstr = "Moon Magic for {}:\n\n".format(date.isoformat())
    for order in ORDERS:
        moonstr = "Bonus to Caster Level and Save DCs for {}: {}".format(order.name, order.moon_magic(date))
        retstr += moonstr
        retstr += "\n"
        print(moonstr)
    return retstr

