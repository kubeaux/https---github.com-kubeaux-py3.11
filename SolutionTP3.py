import numpy as np

def see_illusion(height, width, square_size, rectangle_size, gris1, gris2, blanc, noir):
    res = np.zeros((height, width), dtype=np.uint8)
    sq = square_size
    half = sq // 2
    cx = width // 2
    cy = height // 2
    rh, rw = rectangle_size

    y_off = (cy - half) % sq
    center_r = (cy - y_off) // sq

    band_info = []
    for r in range(-2, (height // sq) + 4):
        y_start = y_off + r * sq
        y0 = max(0, y_start)
        y1 = min(height, y_start + sq)
        if y1 <= y0:
            continue

        d = abs(r - center_r)
        x_off = 0 if d % 2 == 0 else half

        has_mirror = ((cx - x_off) % sq == 0)
        mirror_c = (cx - x_off) // sq if has_mirror else -1

        g1_odd = (d // 2) % 2 == 0

        for c in range(-2, (width // sq) + 3):
            col_start = x_off + c * sq
            x0_c = max(0, col_start)
            x1_c = min(width, col_start + sq)
            if x1_c <= x0_c:
                continue

            c_eff = c
            if has_mirror and c >= mirror_c:
                c_eff = 2 * mirror_c - 1 - c

            if g1_odd:
                color = gris1 if c_eff % 2 == 1 else gris2
            else:
                color = gris1 if c_eff % 2 == 0 else gris2

            res[y0:y1, x0_c:x1_c] = color

        band_info.append((y_start, x_off, has_mirror, mirror_c, g1_odd))

    for i in range(1, len(band_info)):
        y_a, x_off_a, mirror_a, mc_a, par_a = band_info[i - 1]
        y_b, x_off_b, mirror_b, mc_b, par_b = band_info[i]
        boundary_y = y_b

        edges = set()
        for c in range(-2, (width // sq) + 3):
            edges.add(x_off_a + c * sq)
            edges.add(x_off_b + c * sq)
        edges = sorted(edges)

        for idx in range(len(edges) - 1):
            seg_start = edges[idx]
            seg_end = edges[idx + 1]
            if seg_end - seg_start != half:
                continue
            mid_x = (seg_start + seg_end) // 2
            if mid_x < -rw or mid_x >= width + rw:
                continue

            skip = False
            if mirror_a and mc_a >= 0:
                mirror_edge = x_off_a + mc_a * sq
                if seg_start == mirror_edge - half or seg_start == mirror_edge:
                    skip = True
            if mirror_b and mc_b >= 0:
                mirror_edge = x_off_b + mc_b * sq
                if seg_start == mirror_edge - half or seg_start == mirror_edge:
                    skip = True
            if skip:
                continue

            def band_color(mid_x, x_off, has_m, mc, par):
                c = (mid_x - x_off) // sq
                ce = c
                if has_m and c >= mc:
                    ce = 2 * mc - 1 - c
                if par:
                    return gris1 if ce % 2 == 1 else gris2
                else:
                    return gris1 if ce % 2 == 0 else gris2

            col_above = band_color(mid_x, x_off_a, mirror_a, mc_a, par_a)
            col_below = band_color(mid_x, x_off_b, mirror_b, mc_b, par_b)

            if col_above == col_below:
                rect_color = blanc if col_above == gris1 else noir
                ry0 = max(0, boundary_y - rh // 2)
                ry1 = min(height, boundary_y - rh // 2 + rh)
                rx0 = max(0, mid_x - rw // 2)
                rx1 = min(width, mid_x - rw // 2 + rw)
                if ry1 > ry0 and rx1 > rx0:
                    res[ry0:ry1, rx0:rx1] = rect_color

    return res