import uuid

from zped import ZPED
zped = ZPED()

class TriggerClass:
    @zped.triggerman()
    def basic_triggerman():
        pass

    @zped.triggerman("custom-pre-exec", "custom-post-exec")
    def named_triggerman():
        pass

    @zped.triggerman(pre_exec=False)
    def no_pre_exec_triggerman():
        pass

    @zped.triggerman(post_exec=False)
    def no_post_exec_triggerman():
        pass

    @zped.triggerman()
    def echoing_triggerman(input):
        return input

def test_basic_triggerman():
    assert "TriggerClass.basic_triggerman.pre-exec" in zped.__events__
    assert "TriggerClass.basic_triggerman.post-exec" in zped.__events__

def test_named_triggerman():
    assert "custom-pre-exec" in zped.__events__
    assert "custom-post-exec" in zped.__events__

def test_no_pre_exec_triggerman():
    assert "TriggerClass.no_pre_exec_triggerman.pre-exec" not in zped.__events__
    assert "TriggerClass.no_pre_exec_triggerman.post-exec" in zped.__events__

def test_no_post_exec_triggerman():
    assert "TriggerClass.no_post_exec_triggerman.pre-exec" in zped.__events__
    assert "TriggerClass.no_post_exec_triggerman.post-exec" not in zped.__events__

def test_echoing_triggerman():
    expected = uuid.uuid4()
    assert TriggerClass.echoing_triggerman(expected) == expected

