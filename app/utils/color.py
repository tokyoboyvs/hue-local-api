def hex_to_rgb(hex_color: str):
    hex_color = hex_color.lstrip('#')

    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255

    return r, g, b


def apply_gamma(value: float):
    if value > 0.04045:
        return ((value + 0.055) / 1.055) ** 2.4
    
    return value / 12.92


def hex_to_xy(hex_color: str):
    r, g, b = hex_to_rgb(hex_color)

    r = apply_gamma(r)
    g = apply_gamma(g)
    b = apply_gamma(b)

    x = r * 0.664511 + g * 0.154324 + b * 0.162028
    y = r * 0.283881 + g * 0.668433 + b * 0.047685
    z = r * 0.000088 + g * 0.072310 + b * 0.986039

    total = x + y + z

    if total == 0:
        return 0.0, 0.0

    return x / total, y / total
