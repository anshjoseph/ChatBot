import os

def test_key():
    key = os.getenv("OPENAI_KEY")
    assert key != None
    assert len(key) == 51