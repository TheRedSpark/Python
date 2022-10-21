import pytest

def rem_if_gt_3(lst : list, numb : int):
    """ given a list and a number, remove that
        number from the list if it is greater than 3
        do nothing if the numb is <= 3. raise an error
        if numb is not in the list """
    if numb not in lst:
        raise ValueError('numb must be in list')
    if numb > 3:
        lst.remove(numb)

def test_rem():
    """ tests the rem_if_gt_3 function """
    test_list = [0, 4, 5, 3]
    rem_if_gt_3(test_list, 4)

    assert test_list == [0, 5, 3]
    assert rem_if_gt_3(test_list, 0) == None

    # testing errors:
    with pytest.raises(ValueError):
        rem_if_gt_3(test_list, 6)

    with pytest.raises(ValueError):
        rem_if_gt_3(test_list, 2)