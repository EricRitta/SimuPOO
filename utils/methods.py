
def BezierInAcc(t: float) -> float:
    if t <= 0:
        return 0
    if t >= 1:
        return 1

    # peguei essa curva da ia fi, fico legal até
    return 1 - (1 - t)**2 * (2.7 * (1 - t) - 1.7)
