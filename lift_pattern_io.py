
def read_lift_pattern(filename):
    shafts_lifted = []
    with open(filename,'r') as inputFile:

        lines = inputFile.readlines()
        for line in lines:
            try:
                shafts_lifted_now = map(int, line.strip().split())
                if shafts_lifted_now:
                    shafts_lifted.append(sorted(shafts_lifted_now))
            except ValueError:
                print('Ignoring line: ' + line)
    return shafts_lifted
