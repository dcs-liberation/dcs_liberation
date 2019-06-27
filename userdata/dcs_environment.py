"""
This utility classes provides methods to check players installed DCS environment.

TODO : add method 'is_using_open_beta', 'is_using_stable'
TODO : [NICE to have] add method to check list of installed DCS modules (could be done either through window registry, or through filesystem analysis)
TODO : add method 'get DCS install path'
TODO : add method 'get DCS save path'

"""

import winreg


def is_using_dcs_steam_edition():
    """
    Check if DCS World : Steam Edition version is installed on this computer
    :return True if DCS Steam edition is installed,
            -1 if DCS Steam Edition is registered in Steam apps but not installed,
            False if never installed in Steam
    """
    try:
        # Note : Steam App ID for DCS World is 223750
        dcs_path_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Valve\\Steam\\Apps\\223750")
        installed = winreg.QueryValueEx(dcs_path_key, "Installed")
        winreg.CloseKey(dcs_path_key)
        if installed[0] == 1:
            return True
        else:
            return False
    except FileNotFoundError as fnfe:
        return False


def is_using_dcs_standalone_edition():
    """
    Check if DCS World standalone edition is installed on this computer
    :return True if Standalone is installed, False if it is not
    """
    try:
        dcs_path_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Eagle Dynamics\\DCS World")
        winreg.CloseKey(dcs_path_key)
        return True
    except FileNotFoundError as fnfe:
        return False


if __name__ == "__main__":
    print("Using STEAM Edition : " + str(is_using_dcs_steam_edition()))
    print("Using Standalone Edition : " + str(is_using_dcs_standalone_edition()))