from zped import ZPED

zped = ZPED()

def test_custom_event():
    zped.register_event("my-custom-event")
    test_custom_event.executed = False
    @zped.on("my-custom-event")
    def callback():
        test_custom_event.executed = True
    zped.trigger("my-custom-event")
    assert test_custom_event.executed
