def clamp(floatnum, floatmin, floatmax):
    if floatnum < floatmin:
        floatnum = floatmin
    if floatnum > floatmax:
        floatnum = floatmax
    return floatnum


def smootherstep(edge0, edge1, x):
    # Scale, bias and saturate x to 0..1 range
    x = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    # Evaluate polynomial
    # Standard smoothstep version if needed: x * x * (3 - 2 - x)
    return x * x * x * (x * (x * 6 - 15) + 10)


