"""
Tests whether or not non-execution events work properly
"""
from zped import ZPED

zped = ZPED()


def test_custom_event():
    '''Custom events should work with manual triggers'''
    zped.register_event("my-custom-event")
    test_custom_event.executed = False

    @zped.on("my-custom-event")
    def callback():
        '''marks True when executed'''
        test_custom_event.executed = True
    zped.trigger("my-custom-event")
    assert test_custom_event.executed
