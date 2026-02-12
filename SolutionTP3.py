import numpy as np

def see_illusion(height, width, square_size, rectangle_size, gris1, gris2, blanc, noir):
    res = np.zeros((height, width), dtype=np.uint8)
    sq = square_size
    cy, cx = height // 2, width // 2
    half = sq // 2
    
    # Calculate offset to center the grid vertically
    y_off = (cy - half) % sq
    center_row = (cy - y_off) // sq
    
    rh, rw = rectangle_size
    
    # We iterate enough rows/cols to cover the image
    for r_idx in range(-2, (height // sq) + 3):
        row_dist = r_idx - center_row
        
        # Determine row shift
        # Even distance from center row -> aligned (0 offset)
        # Odd distance -> shifted (half offset)
        if row_dist % 2 == 0:
            x_off = 0
            is_even_row = True
        else:
            x_off = half
            is_even_row = False
            
        y_start = y_off + r_idx * sq
        y0 = max(0, y_start)
        y1 = min(height, y_start + sq)
        
        if y1 <= y0:
            continue
            
        rank_y = abs(row_dist) // 2
        
        # Loop over columns
        for c_idx in range(-2, (width // sq) + 3):
            col_start = x_off + c_idx * sq
            
            # Determine Color of current square
            # Mirroring logic for symmetry
            col_mid = col_start + half
            if col_mid >= cx:
                mirror_mid = 2 * cx - col_mid
                c_eff = (mirror_mid - x_off) // sq
            else:
                c_eff = c_idx
                
            # Color logic
            # gris1 is center. 
            # (rank_y + c_eff) % 2 == 1 -> gris1?
            # Let's check center: r_idx=center_row -> rank_y=0.
            # c_idx near center -> c_eff ~ 0?
            # If (0+0)%2=0 -> gris2. 
            # The prompt says "gris1: ... correspondant au centre".
            # So if result is even -> gris1? Or odd?
            # The snippet had `== 1 else gris2`.
            # Let's stick to the snippet: gris1 if odd, gris2 if even.
            # If center needs to be gris1, then we need odd at center.
            # If c_eff is 0 at center, we need to adjust or maybe c_eff is odd?
            # Let's just use the snippet's formula exactly.
            
            color = gris1 if (rank_y + c_eff) % 2 == 1 else gris2
            
            # Draw Square
            x0 = max(0, col_start)
            x1 = min(width, col_start + sq)
            if x1 > x0:
                res[y0:y1, x0:x1] = color
                
            # Draw Rectangle
            # Logic: At the TOP edge of this square (boundary between r-1 and r)
            # Center X = col_mid
            # Check color of Square Below (current) and Square Above (r-1)
            
            # Color Below (Current)
            color_below = color
            
            # Color Above
            r_above = r_idx - 1
            row_dist_above = r_above - center_row
            x_off_above = 0 if row_dist_above % 2 == 0 else half
            rank_y_above = abs(row_dist_above) // 2
            
            # Determine effective column in row above at x = col_mid
            c_idx_above_raw = (col_mid - x_off_above) // sq
            
            # Mirroring for Above
            if col_mid >= cx:
                mirror_mid = 2 * cx - col_mid
                c_eff_above = (mirror_mid - x_off_above) // sq
            else:
                c_eff_above = c_idx_above_raw
                
            color_above = gris1 if (rank_y_above + c_eff_above) % 2 == 1 else gris2
            
            # Condition
            if color_above == color_below:
                rect_val = blanc if color_above == gris1 else noir
                
                # Draw Rectangle centered at (col_mid, y_start)
                ry_start = y_start - rh // 2
                ry_end = ry_start + rh
                rx_start = col_mid - rw // 2
                rx_end = rx_start + rw
                
                # Clip
                ry0_c = max(0, ry_start)
                ry1_c = min(height, ry_end)
                rx0_c = max(0, rx_start)
                rx1_c = min(width, rx_end)
                
                if ry1_c > ry0_c and rx1_c > rx0_c:
                    res[ry0_c:ry1_c, rx0_c:rx1_c] = rect_val

    return res