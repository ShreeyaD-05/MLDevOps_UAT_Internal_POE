from hello import greet


def test_greet_default():
    assert greet() == "Hello, MLOps! UAT environment is working."