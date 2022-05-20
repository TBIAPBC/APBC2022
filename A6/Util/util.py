"""
Utility Functions
"""
import random


def player_colors(player_count) -> list:
    colors = []
    for p in range(player_count):
        hex = "#" + "".join([random.choice("ABCDEF0123456789") for _ in range(6)])
        colors.append(hex)
    return colors

