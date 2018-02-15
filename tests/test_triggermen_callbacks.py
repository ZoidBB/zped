import uuid

from zped import ZPED
zped = ZPED()


class TriggerClass:
    @zped.triggerman()
    def basic_triggerman():
        pass

    @zped.triggerman()
    def modified_input_echoing_triggerman(input):
        return input

    @zped.triggerman()
    def modified_output_echoing_triggerman(input):
        return input

    @zped.triggerman()
    def stopped_triggerman_with_post_exec():
        assert 1 / 0  # junk assertion to indicate stuff broke

    @zped.triggerman()
    def stopped_triggerman_without_post_exec():
        assert 1 / 0  # junk assertion to indicate stuff broke


class CallbackClass:
    basic_triggerman_pre_exec_called = False
    basic_triggerman_post_exec_called = False

    modified_input_echoing_triggerman_input = uuid.uuid4()

    modified_output_echoing_triggerman_output = uuid.uuid4()

    stopped_triggerman_with_post_exec_executed_post = False
    stopped_triggerman_with_post_exec_output = uuid.uuid4()

    stopped_triggerman_without_post_exec_executed_post = False
    stopped_triggerman_without_post_exec_output = uuid.uuid4()

    @zped.on("TriggerClass.basic_triggerman.pre-exec")
    def basic_triggerman_pre_exec(args, kwargs):
        CallbackClass.basic_triggerman_pre_exec_called = True

    @zped.on("TriggerClass.basic_triggerman.post-exec")
    def basic_triggerman_post_exec(args, kwargs, result):
        CallbackClass.basic_triggerman_post_exec_called = True

    @zped.on("TriggerClass.modified_input_echoing_triggerman.pre-exec")
    def modified_input_echoing_triggerman_pre_exec(args, kwargs):
        raise zped.ModifyPayload(
            [CallbackClass.modified_input_echoing_triggerman_input], kwargs)

    @zped.on("TriggerClass.modified_output_echoing_triggerman.post-exec")
    def modified_output_echoing_triggerman_post_exec(args, kwargs, result):
        raise zped.ModifyPayload(
            [
                CallbackClass.modified_output_echoing_triggerman_output],
            kwargs,
            CallbackClass.modified_output_echoing_triggerman_output)

    @zped.on("TriggerClass.stopped_triggerman_with_post_exec.pre-exec")
    def stopped_triggerman_with_post_exec_pre_exec(args, kwargs):
        raise zped.StopExecution(
            CallbackClass.stopped_triggerman_with_post_exec_output)

    @zped.on("TriggerClass.stopped_triggerman_with_post_exec.post-exec")
    def stopped_triggerman_with_post_exec_post_exec(args, kwargs, result):
        CallbackClass.stopped_triggerman_with_post_exec_executed_post = True

    @zped.on("TriggerClass.stopped_triggerman_without_post_exec.pre-exec")
    def stopped_triggerman_without_post_exec_pre_exec(args, kwargs):
        raise zped.StopExecution(
            CallbackClass.stopped_triggerman_without_post_exec_output, False)

    @zped.on("TriggerClass.stopped_triggerman_without_post_exec.post-exec")
    def stopped_triggerman_without_post_exec_post_exec(args, kwargs, result):
        CallbackClass.stopped_triggerman_without_post_exec_executed_post = True


def test_basic_triggerman():
    """
    executing triggerman()'d function should call pre and post exec listeners
    """

    assert not CallbackClass.basic_triggerman_pre_exec_called
    assert not CallbackClass.basic_triggerman_post_exec_called

    TriggerClass.basic_triggerman()

    assert CallbackClass.basic_triggerman_pre_exec_called
    assert CallbackClass.basic_triggerman_post_exec_called


def test_modified_input_echoing_triggerman():
    """
    executing a triggerman()'d function with a listener which raises
    ModifyPayload on pre-exec should have input modified
    """

    assert TriggerClass.modified_input_echoing_triggerman(
           uuid.uuid4()) == CallbackClass.modified_input_echoing_triggerman_input


def test_modified_output_echoing_triggerman():
    """
    executing a triggerman()'d function with a listener which raises
    ModifyPayload on post-exec should have output modified
    """

    assert TriggerClass.modified_output_echoing_triggerman(
           uuid.uuid4()) == CallbackClass.modified_output_echoing_triggerman_output


def test_stopped_triggerman_with_post_exec():
    """
    executinging a triggerman'd function with listener which raises
    StopExecution on pre-exec should not execute function
    """

    assert not CallbackClass.stopped_triggerman_with_post_exec_executed_post
    assert TriggerClass.stopped_triggerman_with_post_exec(
           ) == CallbackClass.stopped_triggerman_with_post_exec_output
    assert CallbackClass.stopped_triggerman_with_post_exec_executed_post


def test_stopped_triggerman_without_post_exec():
    """
    executing a triggerman'd function with listener which raises StopExecution
    with exec_post set to False should execute neither function nor post-exec
    listener stack
    """
    
    assert not CallbackClass.stopped_triggerman_without_post_exec_executed_post
    assert TriggerClass.stopped_triggerman_without_post_exec(
           ) == CallbackClass.stopped_triggerman_without_post_exec_output
    assert not CallbackClass.stopped_triggerman_without_post_exec_executed_post
