class ground_forces_procurement_raito:

    # initial cost ratio based on a force of 10 M1A2, 6 Bradly, 2 MLRPS, 2 Avenger and 4 TOW which seemed feasible. Can be adjusted to resemble forces with different doctrines or wars
    # Could later be changed to resemble a task force
    tank_ratio: int = 6
    atgm_ratio: int = 1
    apc_ratio: int = 3
    ifv_ratio: int = 4
    artillery_ratio: int = 2
    shorad_ratio: int = 1
    combined_ratio: int = tank_ratio + atgm_ratio + apc_ratio + ifv_ratio + artillery_ratio + shorad_ratio