import sys

class Passport:
    def __init__(self):
        self.fields = {}

    def add(self, line):
        kvs = line.split(' ')
        for kv in kvs:
            ls = kv.split(':')
            assert len(ls) == 2
            k = ls[0]
            v = ls[1]
            assert k not in self.fields
            self.fields[k] = v


    def validate_p1(self):
        return 'byr' in self.fields and \
            'iyr' in self.fields and \
            'eyr' in self.fields and \
            'hgt' in self.fields and \
            'hcl' in self.fields and \
            'ecl' in self.fields and \
            'pid' in self.fields


    def validate_p2(self):
        try:
            def check():
                byr_str = self.fields['byr']
                yield (len(byr_str) == 4, 'birth year wrong length')
                byr = int(byr_str)
                yield (byr >= 1920, 'birth year too early')
                yield (byr <= 2002, 'birth year too late')

                iyr_str = self.fields['iyr']
                yield (len(iyr_str) == 4, 'issue year wrong length')
                iyr = int(iyr_str)
                yield (iyr >= 2010, 'issue year too early')
                yield (iyr <= 2020, 'issue year too late')

                eyr_str = self.fields['eyr']
                yield (len(eyr_str) == 4, 'expire year wrong length')
                eyr = int(eyr_str)
                yield (eyr >= 2020, 'expire year too early')
                yield (eyr <= 2030, 'expire year too late')

                hgt_str = self.fields['hgt']
                units = hgt_str[-2:]
                yield (units == 'cm' or units == 'in', 'invalid height units')
                if units == 'cm':
                    value = int(hgt_str[0:-2])
                    yield (value >= 150 and value <= 193, 'unrealistic height (cm)')
                elif units == 'in':
                    value = int(hgt_str[0:-2])
                    yield (value >= 59 and value <= 76, 'unrealistic height (in)')

                hcl_str = self.fields['hcl']
                yield (hcl_str[0] == '#', 'hair color no start with #')
                yield (len(hcl_str) == 7, 'hair color wrong length')
                for char in hcl_str[1:]:
                    yield (char in 'abcdefghijklmnopqrstuvwxyz0123456789', f'invalid hair color {hcl_str}')

                ecl_str = self.fields['ecl']
                yield (ecl_str in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'], 'invalid eye color')

                pid_str = self.fields['pid']
                yield (len(pid_str) == 9, 'wrong passport ID length')
                for char in pid_str:
                    yield (char in '0123456789', 'invalid pid chars')

            for valid, reason in check():
                if not valid:
                    return False
            return True

        except KeyError as e:
            return False


def stripped_lines(filename):
    with open(filename) as f:
        for line in f.readlines():
            yield line.strip()


def parse(args):
    passports = []
    pp = Passport()
    for line in stripped_lines(args[1]):
        if line == '':
            passports.append(pp)
            pp = Passport()
        else:
            pp.add(line)
    passports.append(pp)

    return passports


def validate_p1(passports):
    return sum([pp.validate_p1() for pp in passports])


def validate_p2(passports):
    return sum([pp.validate_p2() for pp in passports])


def main(args):
    passports = parse(args)
    p1_ans = validate_p1(passports)
    print(f'part one: {p1_ans}')
    p2_ans = validate_p2(passports)
    print(f'part two: {p2_ans}')


if __name__ == '__main__':
    main(sys.argv)