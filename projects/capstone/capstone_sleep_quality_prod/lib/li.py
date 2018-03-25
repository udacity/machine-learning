"""
Module which contain processes regarding list.
"""

def remove(target_list,values_to_remove):
    """
    It removes specified values from the list.

    :param list target_list: A list which has some values to remove.
    :param list values_to_remove: Values to remove from the list.
    :return: list target_list: Returns the list whose specified values removed.
    """
    for value in values_to_remove:
        target_list.remove(value)
    return target_list