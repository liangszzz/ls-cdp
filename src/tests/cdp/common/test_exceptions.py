from src.main.cdp.common.exceptions import exception_decorator, BizException, ParamNotFoundException, \
    FileNotFoundException, S3FileNotExistException, DateFormatException, NotImplementedException


@exception_decorator
def throw_exceptions(index):
    if index == 0:
        raise BizException("xxx", Exception("xxx"))
    elif index == 1:
        raise ParamNotFoundException("xxx", Exception("xxx"))
    elif index == 2:
        raise FileNotFoundException("xxx", Exception("xxx"))
    elif index == 3:
        raise S3FileNotExistException("xxx", Exception("xxx"))
    elif index == 4:
        raise DateFormatException("xxx", "xxx2", Exception("xxx"))
    elif index == 5:
        raise NotImplementedException(Exception("xxx"))
    else:
        print("success")


def test_exception():
    try:
        throw_exceptions(-1)
    except Exception as e:
        assert e is not None

    try:
        throw_exceptions(0)
    except Exception as e:
        assert e is not None

    try:
        throw_exceptions(1)
    except Exception as e:
        assert e is not None

    try:
        throw_exceptions(2)
    except Exception as e:
        assert e is not None

    try:
        throw_exceptions(3)
    except Exception as e:
        assert e is not None

    try:
        throw_exceptions(4)
    except Exception as e:
        assert e is not None

    try:
        throw_exceptions(5)
    except Exception as e:
        assert e is not None
