"""
This utility classes provides methods to check players installed DCS environment.

TODO : add method 'is_using_open_beta', 'is_using_stable'
TODO : [NICE to have] add method to check list of installed DCS modules (could be done either through window registry, or through filesystem analysis)
TODO : add method 'get DCS save path'

"""

import winreg
import os


def is_using_dcs_steam_edition():
    """
    Check if DCS World : Steam Edition version is installed on this computer
    :return True if DCS Steam edition is installed,
            -1 if DCS Steam Edition is registered in Steam apps but not installed,
            False if never installed in Steam
    """
    try:
        # Note : Steam App ID for DCS World is 223750
        dcs_steam_app_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Valve\\Steam\\Apps\\223750")
        installed = winreg.QueryValueEx(dcs_steam_app_key, "Installed")
        winreg.CloseKey(dcs_steam_app_key)
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


def _find_steam_directory():
    """
    Get the Steam install directory for this computer from registry
    :return Steam installation path
    """
    try:
        steam_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Valve\\Steam")
        path = winreg.QueryValueEx(steam_key, "SteamPath")[0]
        winreg.CloseKey(steam_key)
        return path
    except FileNotFoundError as fnfe:
        print(fnfe)
        return ""


def _get_steam_library_folders():
    """
    Get the installation directory for Steam games
    :return List of Steam library folders where games can be installed
    """
    try:
        steam_dir = _find_steam_directory()
        """        
        For reference here is what the vdf file is supposed to look like : 
        
        "LibraryFolders"
        {
            "TimeNextStatsReport"        "1561832478"
            "ContentStatsID"        "-158337411110787451"
            "1"        "D:\\Games\\Steam"
            "2"        "E:\\Steam"
        }
        """
        vdf_file_location = steam_dir + os.path.sep + "steamapps" + os.path.sep + "libraryfolders.vdf"
        with open(vdf_file_location) as adf_file:
            paths = [l.split("\"")[3] for l in adf_file.readlines()[1:] if ':\\\\' in l]
            return paths
    except Exception as e:
        print(e)
        return []


def _find_steam_dcs_directory():
    """
    Find the DCS install directory for DCS World Steam Edition
    :return: Install directory as string, empty string if not found
    """
    for library_folder in _get_steam_library_folders():
        folder = library_folder + os.path.sep + "steamapps" + os.path.sep + "common" + os.path.sep + "DCSWorld"
        if os.path.isdir(folder):
            return folder + os.path.sep
    return ""


def get_dcs_install_directory():
    """
    Get the Steam install directory for this computer
    :return Steam installation path
    """
    if is_using_dcs_standalone_edition():
        try:
            dcs_path_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Eagle Dynamics\\DCS World")
            path = winreg.QueryValueEx(dcs_path_key, "Path")
            dcs_dir = path[0] + os.path.sep
            winreg.CloseKey(dcs_path_key)
            return dcs_dir
        except Exception as e:
            print("Couldn't detect DCS World installation folder")
            return ""
    elif is_using_dcs_steam_edition():
        return _find_steam_dcs_directory()
    else:
        print("Couldn't detect any installed DCS World version")


if __name__ == "__main__":
    print("Using STEAM Edition : " + str(is_using_dcs_steam_edition()))
    print("Using Standalone Edition : " + str(is_using_dcs_standalone_edition()))
    print("DCS Installation directory : " + get_dcs_install_directory())