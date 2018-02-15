"""
Tests tringgerman decorators, event registration, etc
"""
import uuid

from zped import ZPED
zped = ZPED()


class TriggerClass:
    """
    class holds all the triggermen
    """
    @zped.triggerman()
    def basic_triggerman():
        '''auto-named, auto-registered'''
        pass

    @zped.triggerman("custom-pre-exec", "custom-post-exec")
    def named_triggerman():
        '''registered with custom event names'''
        pass

    @zped.triggerman(pre_exec=False)
    def no_pre_exec_triggerman():
        '''has no pre-execution event'''
        pass

    @zped.triggerman(post_exec=False)
    def no_post_exec_triggerman():
        '''has no post-execution event'''
        pass

    @zped.triggerman()
    def echoing_triggerman(_input):
        '''returns unmodified _input'''
        return _input


def test_basic_triggerman():
    """
    triggerman() should result in pre and post execuation event registration
    """

    assert "TriggerClass.basic_triggerman.pre-exec" in zped.__events__
    assert "TriggerClass.basic_triggerman.post-exec" in zped.__events__


def test_named_triggerman():
    """
    triggerman() should use supplied custom names for pre and post execution
    event registration
    """
    assert "custom-pre-exec" in zped.__events__
    assert "custom-post-exec" in zped.__events__


def test_no_pre_exec_triggerman():
    """
    triggerman() should not register pre-execution events when told not to
    """

    assert "TriggerClass.no_pre_exec_triggerman.pre-exec" not in zped.__events__
    assert "TriggerClass.no_pre_exec_triggerman.post-exec" in zped.__events__


def test_no_post_exec_triggerman():
    """
    triggerman() should not register post-execution events when told not to
    """
    assert "TriggerClass.no_post_exec_triggerman.pre-exec" in zped.__events__
    assert "TriggerClass.no_post_exec_triggerman.post-exec" not in zped.__events__


def test_echoing_triggerman():
    """
    executing a triggerman()\'d function should follow expected function logic
    """

    expected = uuid.uuid4()
    assert TriggerClass.echoing_triggerman(expected) == expected

def test_decorated_function_names():
    """
    decorated functions should have the same name as undecorated function
    """
    assert TriggerClass.basic_triggerman.__name__ is "basic_triggerman"
