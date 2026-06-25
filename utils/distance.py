import math



# -------------------------
# BASIC DISTANCE
# -------------------------

def calculate_distance(p1, p2):


    if p1 is None or p2 is None:

        return 0



    return math.sqrt(

        (p2[0]-p1[0])**2 +

        (p2[1]-p1[1])**2

    )






# -------------------------
# NORMALIZED DISTANCE
# Useful for different screens
# -------------------------

def normalized_distance(
        p1,
        p2,
        width,
        height
):


    if width == 0 or height == 0:

        return 0



    dx = (p2[0]-p1[0]) / width

    dy = (p2[1]-p1[1]) / height



    return math.sqrt(

        dx*dx +

        dy*dy

    )







# -------------------------
# MID POINT
# -------------------------

def midpoint(p1,p2):


    return (

        int((p1[0]+p2[0])/2),

        int((p1[1]+p2[1])/2)

    )






# -------------------------
# MOVEMENT AMOUNT
# -------------------------

def movement_distance(
        old,
        new
):


    if old is None or new is None:

        return 0



    return calculate_distance(
        old,
        new
    )