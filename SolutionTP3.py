import numpy as np

def see_illusion(height, width, square_size, rectangle_size, gris1, gris2, blanc, noir):
    res = np.zeros((height, width), dtype=np.uint8)
    sq = square_size
    cy, cx = height // 2, width // 2
    half = sq // 2
    y_off = (cy - half) % sq
    center_row = (cy - y_off) // sq
    rh, rw = rectangle_size

    for r_idx in range(-2, (height // sq) + 3):
        row_dist = r_idx - center_row
        x_off = 0 if row_dist % 2 == 0 else half
        is_even = (row_dist % 2 == 0)

        y_start = y_off + r_idx * sq
        y0 = max(0, y_start)
        y1 = min(height, y_start + sq)
        if y1 <= y0:
            continue

        rank_y = abs(row_dist) // 2

        for c_idx in range(-2, (width // sq) + 3):
            col_start = x_off + c_idx * sq

            if is_even:
                col_mid = col_start + half
                if col_mid >= cx:
                    mirror_mid = 2 * cx - col_mid
                    c_eff = (mirror_mid - x_off) // sq
                else:
                    c_eff = c_idx
            else:
                c_eff = c_idx

            if (rank_y + c_eff) % 2 == 1:
                color = gris1
            else:
                color = gris2

            x0 = max(0, col_start)
            x1 = min(width, col_start + sq)
            if x1 > x0:
                res[y0:y1, x0:x1] = color

    # --- DRAW RECTANGLES ---
    for r_idx in range(-2, (height // sq) + 4):
        frontier_y = y_off + r_idx * sq

        if frontier_y < -rh or frontier_y > height + rh:
            continue

        rd_above = (r_idx - 1) - center_row
        x_off_above = 0 if rd_above % 2 == 0 else half
        is_even_above = (rd_above % 2 == 0)
        rank_y_above = abs(rd_above) // 2

        rd_below = r_idx - center_row
        x_off_below = 0 if rd_below % 2 == 0 else half
        is_even_below = (rd_below % 2 == 0)
        rank_y_below = abs(rd_below) // 2

        edges = set()
        for c in range(-2, (width // sq) + 3):
            edges.add(x_off_above + c * sq)
            edges.add(x_off_below + c * sq)
        edges = sorted(edges)

        for idx in range(len(edges) - 1):
            seg_start = edges[idx]
            seg_end = edges[idx + 1]

            if seg_end - seg_start != half:
                continue

            mid_x = (seg_start + seg_end) // 2

            if mid_x < -rw or mid_x > width + rw:
                continue

            c_above = (mid_x - x_off_above) // sq
            if is_even_above:
                col_mid_a = x_off_above + c_above * sq + half
                if col_mid_a >= cx:
                    c_eff_above = (2 * cx - col_mid_a - x_off_above) // sq
                else:
                    c_eff_above = c_above
            else:
                c_eff_above = c_above

            color_above = gris1 if (rank_y_above + c_eff_above) % 2 == 1 else gris2

            c_below = (mid_x - x_off_below) // sq
            if is_even_below:
                col_mid_b = x_off_below + c_below * sq + half
                if col_mid_b >= cx:
                    c_eff_below = (2 * cx - col_mid_b - x_off_below) // sq
                else:
                    c_eff_below = c_below
            else:
                c_eff_below = c_below

            color_below = gris1 if (rank_y_below + c_eff_below) % 2 == 1 else gris2

            if color_above == color_below:
                rect_color = blanc if color_above == gris1 else noir

                ry0 = max(0, frontier_y - rh // 2)
                ry1 = min(height, frontier_y - rh // 2 + rh)
                rx0 = max(0, mid_x - rw // 2)
                rx1 = min(width, mid_x - rw // 2 + rw)

                if ry1 > ry0 and rx1 > rx0:
                    res[ry0:ry1, rx0:rx1] = rect_color

    return res