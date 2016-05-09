
def read_lift_pattern(filename=None, text=None):
    assert not (filename is None and text is None)
    if text:
        lines = text
    else:
        with open(filename,'r') as inputFile:
            lines = inputFile.readlines()

    shafts_lifted = []
    for line in lines:
        try:
            shafts_lifted_now = map(int, line.strip().split())
            if shafts_lifted_now:
                shafts_lifted.append(sorted(shafts_lifted_now))
        except ValueError:
            print('Ignoring line: ' + line)
    return shafts_lifted
