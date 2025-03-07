# global
from typing import Union, Optional

import paddle
import math
import ivy.functional.backends.paddle as paddle_backend

# local
import ivy
from . import backend_version
from ivy.func_wrapper import with_unsupported_dtypes, with_unsupported_device_and_dtypes


def _elementwise_helper(x1, x2):
    x1, x2 = ivy.promote_types_of_inputs(x1, x2)
    x1, x2 = paddle_backend.broadcast_arrays(x1, x2)
    return x1, x2, x1.dtype


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def add(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    alpha: Optional[Union[int, float]] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if x1.dtype in [paddle.int8, paddle.uint8, paddle.float16, paddle.bool]:
        x1, x2 = x1.astype("float32"), x2.astype("float32")
    if alpha not in (1, None):
        x2 = paddle_backend.multiply(x2, alpha)
        x1, x2 = ivy.promote_types_of_inputs(x1, x2)
    return paddle.add(x1, x2).astype(ret_dtype)


def bitwise_xor(
    x1: Union[int, bool, paddle.Tensor],
    x2: Union[int, bool, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    return paddle.bitwise_xor(x1, x2)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def expm1(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [paddle.float16, paddle.float32, paddle.float64]:
        return paddle.expm1(x)
    return paddle_backend.subtract(paddle_backend.exp(x), 1.0).astype(x.dtype)


def bitwise_invert(
    x: Union[int, bool, paddle.Tensor], /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    return paddle.bitwise_not(x)


@with_unsupported_dtypes(
    {
        "2.4.2 and below": (
            "int8",
            "int16",
            "uint8",
            "uint16",
            "bfloat16",
            "complex64",
            "complex128",
            "bool",
        )
    },
    backend_version,
)
def isfinite(
    x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    return paddle.isfinite(x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def isinf(
    x: paddle.Tensor,
    /,
    *,
    detect_positive: bool = True,
    detect_negative: bool = True,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    if detect_negative and detect_positive:
        return paddle.isinf(x)

    if detect_negative:
        return paddle_backend.equal(x, float("-inf"))

    if detect_positive:
        return paddle_backend.equal(x, float("inf"))

    return paddle.zeros(shape=x.shape, dtype=bool)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def equal(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    diff = paddle_backend.subtract(x1, x2)
    ret = paddle_backend.logical_and(
        paddle_backend.less_equal(diff, 0), paddle_backend.greater_equal(diff, 0)
    )
    # ret result is sufficient for all cases except where the value is +/-INF of NaN
    return paddle_backend.where(
        paddle_backend.isnan(diff),
        ~paddle_backend.logical_or(paddle_backend.isnan(x1), paddle_backend.isnan(x2)),
        ret,
    )


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def less_equal(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if x1.dtype in [paddle.int8, paddle.uint8, paddle.complex64, paddle.complex128]:
        if paddle.is_complex(x1):
            if paddle.is_complex(x1):
                real = paddle.less_equal(x1.real(), x2.real())
                imag = paddle.less_equal(x1.imag(), x2.imag())
                return paddle_backend.logical_and(real, imag)
        return paddle.less_equal(x1.astype("float32"), x2.astype("float32"))

    return paddle.less_equal(x1, x2)


def bitwise_and(
    x1: Union[int, bool, paddle.Tensor],
    x2: Union[int, bool, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    return paddle.bitwise_and(x1, x2)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def ceil(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.int32,
        paddle.int64,
        paddle.uint8,
        paddle.float16,
        paddle.complex64,
        paddle.complex128,
        paddle.bool,
    ]:
        if paddle.is_complex(x):
            return paddle.complex(paddle.ceil(x.real()), paddle.ceil(x.imag()))
        return paddle.ceil(x.astype("float32")).astype(x.dtype)
    return paddle.ceil(x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def floor(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.int32,
        paddle.int64,
        paddle.uint8,
        paddle.float16,
        paddle.complex64,
        paddle.complex128,
        paddle.bool,
    ]:
        if paddle.is_complex(x):
            return paddle.complex(paddle.floor(x.real()), paddle.floor(x.imag()))
        return paddle.floor(x.astype("float32")).astype(x.dtype)
    return paddle.floor(x)


@with_unsupported_device_and_dtypes(
    {
        "2.4.2 and below": {
            "cpu": ("uint16", "bfloat16", "complex64", "complex128", "bool")
        }
    },
    backend_version,
)
def asin(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.int32,
        paddle.int64,
        paddle.uint8,
        paddle.float16,
    ]:
        ret_dtype = x.dtype
        return paddle.asin(x.astype("float32")).astype(ret_dtype)
    return paddle.asin(x)


@with_unsupported_device_and_dtypes(
    {
        "2.4.2 and below": {
            "cpu": ("uint16", "bfloat16", "complex64", "complex128", "bool")
        }
    },
    backend_version,
)
def asinh(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.int32,
        paddle.int64,
        paddle.uint8,
        paddle.float16,
    ]:
        ret_dtype = x.dtype
        return paddle.asinh(x.astype("float32")).astype(ret_dtype)
    return paddle.asinh(x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def sign(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.int32,
        paddle.int64,
        paddle.uint8,
        paddle.float16,
        paddle.bool,
    ]:
        return paddle.sgn(x.astype("float32")).astype(x.dtype)
    return paddle.sgn(x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def sqrt(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.int32,
        paddle.int64,
        paddle.uint8,
        paddle.float16,
        paddle.complex64,
        paddle.complex128,
        paddle.bool,
    ]:
        if paddle.is_complex(x):
            angle = paddle.angle(x)
            result = paddle.complex(
                paddle.cos(angle / 2), paddle.sin(angle / 2)
            ) * paddle.sqrt(paddle.abs(x))
            return result
        return paddle.sqrt(x.astype("float32")).astype(x.dtype)
    return paddle.sqrt(x)


@with_unsupported_device_and_dtypes(
    {
        "2.4.2 and below": {
            "cpu": ("uint16", "bfloat16", "complex64", "complex128", "bool")
        }
    },
    backend_version,
)
def cosh(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.int32,
        paddle.int64,
        paddle.uint8,
        paddle.float16,
    ]:
        ret_dtype = x.dtype
        return paddle.cosh(x.astype("float32")).astype(ret_dtype)
    return paddle.cosh(x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def log10(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.int32,
        paddle.int64,
        paddle.uint8,
        paddle.float16,
        paddle.complex64,
        paddle.complex128,
        paddle.bool,
    ]:
        if paddle.is_complex(x):
            base = paddle.to_tensor(10.0).squeeze()
            return paddle_backend.divide(
                paddle_backend.log(x), paddle_backend.log(base)
            ).astype(x.dtype)
        return paddle.log10(x.astype("float32")).astype(x.dtype)
    return paddle.log10(x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def log2(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.int32,
        paddle.int64,
        paddle.uint8,
        paddle.float16,
        paddle.complex64,
        paddle.complex128,
        paddle.bool,
    ]:
        if paddle.is_complex(x):
            base = paddle.to_tensor(2.0).squeeze()
            return paddle_backend.divide(
                paddle_backend.log(x), paddle_backend.log(base)
            ).astype(x.dtype)
        return paddle.log2(x.astype("float32")).astype(x.dtype)
    return paddle.log2(x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def log1p(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.int32,
        paddle.int64,
        paddle.uint8,
        paddle.float16,
        paddle.complex64,
        paddle.complex128,
        paddle.bool,
    ]:
        if paddle.is_complex(x):
            return paddle.complex(paddle.log1p(paddle.abs(x)), paddle.angle(x + 1))
        return paddle.log1p(x.astype("float32")).astype(x.dtype)
    return paddle.log1p(x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def isnan(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.uint8,
        paddle.complex64,
        paddle.complex128,
        paddle.bool,
    ]:
        if paddle.is_complex(x):
            return paddle.logical_or(paddle.isnan(x.real()), paddle.isnan(x.imag()))
        return paddle.isnan(x.astype("float32"))
    return paddle.isnan(x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def less(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if x1.dtype in [paddle.int8, paddle.uint8, paddle.complex64, paddle.complex128]:
        if paddle.is_complex(x1):
            real = paddle.less_than(x1.real(), x2.real())
            imag = paddle.less_than(x1.imag(), x2.imag())
            return logical_and(real, imag)
        return paddle.less_than(x1.astype("float32"), x2.astype("float32"))

    return paddle.less_than(x1, x2)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def multiply(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if x1.dtype in [paddle.int8, paddle.int16, paddle.uint8, paddle.float16]:
        x1, x2 = x1.astype("float32"), x2.astype("float32")
    return paddle.multiply(x1, x2).astype(ret_dtype)


@with_unsupported_device_and_dtypes(
    {
        "2.4.2 and below": {
            "cpu": ("uint16", "bfloat16", "complex64", "complex128", "bool")
        }
    },
    backend_version,
)
def cos(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.int32,
        paddle.int64,
        paddle.uint8,
        paddle.float16,
    ]:
        ret_dtype = x.dtype
        return paddle.cos(x.astype("float32")).astype(ret_dtype)
    return paddle.cos(x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def logical_not(
    x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    if x.dtype in [paddle.uint8, paddle.float16, paddle.complex64, paddle.complex128]:
        if paddle.is_complex(x):
            return paddle.logical_and(
                paddle.logical_not(x.real()), paddle.logical_not(x.imag())
            )
        return paddle.logical_not(x.astype("float32"))
    return paddle.logical_not(x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def divide(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if x1.dtype in [paddle.float16]:
        x1, x2 = x1.astype("float32"), x2.astype("float32")
    if not (ivy.is_float_dtype(ret_dtype) or ivy.is_complex_dtype(ret_dtype)):
        ret_dtype = ivy.default_float_dtype(as_native=True)
    return (x1 / x2).astype(ret_dtype)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def greater(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if x1.dtype in [paddle.int8, paddle.uint8, paddle.complex64, paddle.complex128]:
        if paddle.is_complex(x1):
            if paddle.is_complex(x1):
                real = paddle.greater_than(x1.real(), x2.real())
                imag = paddle.greater_than(x1.imag(), x2.imag())
                return paddle.logical_and(real, imag)
        return paddle.greater_than(x1.astype("float32"), x2.astype("float32"))
    return paddle.greater_than(x1, x2)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def greater_equal(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if x1.dtype in [paddle.int8, paddle.uint8, paddle.complex64, paddle.complex128]:
        if paddle.is_complex(x1):
            if paddle.is_complex(x1):
                real = paddle.greater_equal(x1.real(), x2.real())
                imag = paddle.greater_equal(x1.imag(), x2.imag())
                return paddle.logical_and(real, imag)
        return paddle.greater_equal(x1.astype("float32"), x2.astype("float32"))
    return paddle.greater_equal(x1, x2)


@with_unsupported_device_and_dtypes(
    {
        "2.4.2 and below": {
            "cpu": ("uint16", "bfloat16", "complex64", "complex128", "bool")
        }
    },
    backend_version,
)
def acos(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.int32,
        paddle.int64,
        paddle.uint8,
        paddle.float16,
    ]:
        return paddle.acos(x.astype("float32")).astype(x.dtype)
    return paddle.acos(x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def logical_xor(
    x1: paddle.Tensor, x2: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if ret_dtype in [paddle.uint8, paddle.float16, paddle.complex64, paddle.complex128]:
        if paddle.is_complex(x1):
            return paddle.logical_xor(
                paddle.logical_xor(x1.real(), x2.real()),
                paddle.logical_xor(x1.imag(), x2.imag()),
            )
        return paddle.logical_xor(x1.astype("float32"), x2.astype("float32"))
    return paddle.logical_xor(x1, x2)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def logical_and(
    x1: paddle.Tensor, x2: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if ret_dtype in [paddle.uint8, paddle.float16, paddle.complex64, paddle.complex128]:
        if paddle.is_complex(x1):
            return paddle.logical_and(
                paddle.logical_and(x1.real(), x2.real()),
                paddle.logical_and(x1.imag(), x2.imag()),
            )
        return paddle.logical_and(x1.astype("float32"), x2.astype("float32"))
    return paddle.logical_and(x1, x2)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def logical_or(
    x1: paddle.Tensor, x2: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if ret_dtype in [paddle.uint8, paddle.float16, paddle.complex64, paddle.complex128]:
        if paddle.is_complex(x1):
            return paddle.logical_or(
                paddle.logical_or(x1.real(), x2.real()),
                paddle.logical_or(x1.imag(), x2.imag()),
            )
        return paddle.logical_or(x1.astype("float32"), x2.astype("float32"))
    return paddle.logical_or(x1, x2)


@with_unsupported_device_and_dtypes(
    {
        "2.4.2 and below": {
            "cpu": ("uint16", "bfloat16", "complex64", "complex128", "bool")
        }
    },
    backend_version,
)
def acosh(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.int32,
        paddle.int64,
        paddle.uint8,
        paddle.float16,
    ]:
        return paddle.acosh(x.astype("float32")).astype(x.dtype)
    return paddle.acosh(x)


@with_unsupported_device_and_dtypes(
    {
        "2.4.2 and below": {
            "cpu": ("uint16", "bfloat16", "complex64", "complex128", "bool")
        }
    },
    backend_version,
)
def sin(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.int32,
        paddle.int64,
        paddle.uint8,
        paddle.float16,
    ]:
        return paddle.sin(x.astype("float32")).astype(x.dtype)
    return paddle.sin(x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def negative(
    x: Union[float, paddle.Tensor], /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    if not isinstance(x, paddle.Tensor):
        x = paddle.to_tensor(
            x, dtype=ivy.default_dtype(item=x, as_native=True)
        ).squeeze()
    if x.dtype == paddle.bool:
        return paddle.logical_not(x)
    return paddle.neg(x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def not_equal(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    return paddle.logical_not(paddle_backend.equal(x1, x2))


@with_unsupported_device_and_dtypes(
    {
        "2.4.2 and below": {
            "cpu": ("uint16", "bfloat16", "complex64", "complex128", "bool")
        }
    },
    backend_version,
)
def tanh(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.int32,
        paddle.int64,
        paddle.uint8,
        paddle.float16,
    ]:
        return paddle.tanh(x.astype("float32")).astype(x.dtype)
    return paddle.tanh(x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}},
    backend_version,
)
def floor_divide(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if x1.dtype in [paddle.int32, paddle.int64]:
        return paddle.floor_divide(x1, x2)
    return paddle_backend.floor(paddle_backend.divide(x1, x2)).astype(ret_dtype)


def bitwise_or(
    x1: Union[int, bool, paddle.Tensor],
    x2: Union[int, bool, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    return paddle.bitwise_or(x1, x2)


@with_unsupported_device_and_dtypes(
    {
        "2.4.2 and below": {
            "cpu": ("uint16", "bfloat16", "complex64", "complex128", "bool")
        }
    },
    backend_version,
)
def sinh(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.int32,
        paddle.int64,
        paddle.uint8,
        paddle.float16,
    ]:
        ret_dtype = x.dtype
        return paddle.sinh(x.astype("float32")).astype(ret_dtype)
    return paddle.sinh(x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def positive(
    x: Union[float, paddle.Tensor], /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    if not isinstance(x, paddle.Tensor):
        x = paddle.to_tensor(
            x, dtype=ivy.default_dtype(item=x, as_native=True)
        ).squeeze()
    return x.clone()


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def square(
    x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    if x.dtype in [paddle.int32, paddle.int64, paddle.float32, paddle.float64]:
        return paddle.square(x)
    return paddle_backend.pow(x, 2).astype(x.dtype)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def pow(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if x1.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.uint8,
        paddle.float16,
        paddle.complex64,
        paddle.complex128,
        paddle.bool,
    ]:
        if paddle.is_complex(x1):
            # https://math.stackexchange.com/questions/476968/complex-power-of-a-complex-number
            r = paddle.abs(x1)
            theta = paddle.angle(x1)
            power = x2 * paddle.complex(paddle.log(r), theta)
            result = paddle.exp(power.real()) * paddle.complex(
                paddle.cos(power.imag()), paddle.sin(power.imag())
            )
            return result
        return paddle.pow(x1.astype("float32"), x2.astype("float32")).astype(ret_dtype)
    return paddle.pow(x1, x2)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def round(
    x: paddle.Tensor, /, *, decimals: int = 0, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    def _np_round(x, decimals):
        # this is a logic to mimic np.round behaviour
        # which rounds odd numbers up and even numbers down at limits like 0.5
        eps = 1e-6 * paddle.sign(x)

        # check if the integer is even or odd
        candidate_ints = paddle_backend.remainder(paddle_backend.trunc(x), 2.0).astype(
            bool
        )
        # check if the fraction is exactly half
        candidate_fractions = paddle_backend.equal(
            paddle_backend.abs(paddle_backend.subtract(x, paddle_backend.trunc(x))),
            0.5,
        )
        x = paddle_backend.where(
            paddle.logical_and(~candidate_ints, candidate_fractions),
            x - eps,
            x,
        )
        factor = paddle_backend.pow(10, decimals).astype(x.dtype)
        factor_denom = ivy.where(ivy.isinf(x), 1, factor)
        return paddle_backend.divide(
            paddle.round(paddle_backend.multiply(x, factor)), factor_denom
        )

    x, _ = ivy.promote_types_of_inputs(x, x)
    if x.dtype not in [paddle.float32, paddle.float64]:
        if paddle.is_complex(x):
            return paddle.complex(
                _np_round(x.real(), decimals), _np_round(x.imag(), decimals)
            )
        return _np_round(x.astype("float32"), decimals).astype(x.dtype)
    return _np_round(x, decimals)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def trunc(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.uint8,
        paddle.float16,
        paddle.complex64,
        paddle.complex128,
        paddle.bool,
    ]:
        if paddle.is_complex(x):
            return paddle.complex(paddle.trunc(x.real()), paddle.trunc(x.imag()))
        return paddle.trunc(x.astype("float32")).astype(x.dtype)
    return paddle.trunc(x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def abs(
    x: Union[float, paddle.Tensor],
    /,
    *,
    where: Union[bool, paddle.Tensor] = True,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.uint8,
        paddle.float16,
        paddle.bool,
    ]:
        return ivy.where(where, paddle.abs(x.astype("float32")).astype(x.dtype), x)
    return ivy.where(where, paddle.abs(x), x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def logaddexp(
    x1: paddle.Tensor, x2: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    return paddle_backend.log(
        paddle_backend.add(paddle_backend.exp(x1), paddle_backend.exp(x2))
    ).astype(ret_dtype)


@with_unsupported_device_and_dtypes(
    {
        "2.4.2 and below": {
            "cpu": ("uint16", "bfloat16", "complex64", "complex128", "bool")
        }
    },
    backend_version,
)
def tan(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.int32,
        paddle.int64,
        paddle.uint8,
        paddle.float16,
    ]:
        ret_dtype = x.dtype
        return paddle.tan(x.astype("float32")).astype(ret_dtype)
    return paddle.tan(x)


@with_unsupported_device_and_dtypes(
    {
        "2.4.2 and below": {
            "cpu": ("uint16", "bfloat16", "complex64", "complex128", "bool")
        }
    },
    backend_version,
)
def atan(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.int32,
        paddle.int64,
        paddle.uint8,
        paddle.float16,
    ]:
        ret_dtype = x.dtype
        return paddle.atan(x.astype("float32")).astype(ret_dtype)
    return paddle.atan(x)


@with_unsupported_device_and_dtypes(
    {
        "2.4.2 and below": {
            "cpu": ("uint16", "bfloat16", "complex64", "complex128", "bool")
        }
    },
    backend_version,
)
def atan2(
    x1: paddle.Tensor, x2: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if x1.dtype in [paddle.int8, paddle.int16, paddle.uint8]:
        x1, x2 = x1.astype("float32"), x2.astype("float32")
    return paddle.atan2(x1, x2).astype(ret_dtype)


def log(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.int32,
        paddle.int64,
        paddle.uint8,
        paddle.float16,
        paddle.complex64,
        paddle.complex128,
        paddle.bool,
    ]:
        if paddle.is_complex(x):
            return paddle.complex(paddle.log(paddle.abs(x)), paddle.angle(x))
        return paddle.log(x.astype("float32")).astype(x.dtype)
    return paddle.log(x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def exp(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [paddle.int32, paddle.int64, paddle.float32, paddle.float64]:
        return paddle.exp(x)
    return pow(math.e, x).astype(x.dtype)


def subtract(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    alpha: Optional[Union[int, float]] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if x1.dtype in [paddle.int8, paddle.uint8, paddle.float16, paddle.bool]:
        x1, x2 = x1.astype("float32"), x2.astype("float32")
    if alpha not in (1, None):
        x2 = paddle_backend.multiply(x2, alpha)
        x1, x2 = ivy.promote_types_of_inputs(x1, x2)
    return paddle.subtract(x1, x2).astype(ret_dtype)


@with_unsupported_device_and_dtypes(
    {
        "2.4.2 and below": {
            "cpu": ("uint16", "bfloat16", "complex64", "complex128", "bool")
        }
    },
    backend_version,
)
def remainder(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    modulus: bool = True,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if not modulus:
        res = paddle_backend.divide(x1, x2)
        res_floored = paddle_backend.where(
            paddle_backend.greater_equal(res, 0.0),
            paddle_backend.floor(res),
            paddle_backend.ceil(res),
        )
        diff = paddle_backend.subtract(res, res_floored).astype(res.dtype)
        return paddle_backend.round(paddle_backend.multiply(diff, x2)).astype(x1.dtype)

    if x1.dtype in [paddle.int8, paddle.int16, paddle.uint8, paddle.float16]:
        x1, x2 = x1.astype("float32"), x2.astype("float32")
    return paddle.remainder(x1, x2).astype(ret_dtype)


@with_unsupported_device_and_dtypes(
    {
        "2.4.2 and below": {
            "cpu": ("uint16", "bfloat16", "complex64", "complex128", "bool")
        }
    },
    backend_version,
)
def atanh(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.int32,
        paddle.int64,
        paddle.uint8,
        paddle.float16,
    ]:
        ret_dtype = x.dtype
        return paddle.atanh(x.astype("float32")).astype(ret_dtype)
    return paddle.atanh(x)


def bitwise_right_shift(
    x1: Union[int, bool, paddle.Tensor],
    x2: Union[int, bool, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    return paddle.floor(x1.astype("float64") / 2 ** x2.astype("float64")).astype(
        ret_dtype
    )


def bitwise_left_shift(
    x1: Union[int, bool, paddle.Tensor],
    x2: Union[int, bool, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    return paddle.floor(x1.astype("float64") * 2 ** x2.astype("float64")).astype(
        ret_dtype
    )


# Extra #
# ------#


@with_unsupported_device_and_dtypes(
    {
        "2.4.2 and below": {
            "cpu": ("uint16", "bfloat16", "complex64", "complex128", "bool")
        }
    },
    backend_version,
)
def erf(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    # TODO: add support for complex x, supported in scipy only atm
    if x.dtype in [paddle.int8, paddle.int16, paddle.int32, paddle.int64, paddle.uint8]:
        return paddle.erf(x.astype("float32")).astype(x.dtype)
    return paddle.erf(x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def minimum(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    use_where: bool = True,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if x1.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.uint8,
        paddle.float16,
        paddle.complex64,
        paddle.complex128,
        paddle.bool,
    ]:
        if paddle.is_complex(x1):
            use_where = True
        else:
            x1, x2 = x1.astype("float32"), x2.astype("float32")

    if use_where:
        return paddle_backend.where(paddle_backend.less_equal(x1, x2), x1, x2).astype(
            ret_dtype
        )

    return paddle.minimum(x1, x2).astype(ret_dtype)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def maximum(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    use_where: bool = True,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if x1.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.uint8,
        paddle.float16,
        paddle.complex64,
        paddle.complex128,
        paddle.bool,
    ]:
        if paddle.is_complex(x1):
            use_where = True
        else:
            x1, x2 = x1.astype("float32"), x2.astype("float32")
    if use_where:
        return paddle_backend.where(
            paddle_backend.greater_equal(x1, x2), x1, x2
        ).astype(ret_dtype)
    return paddle.maximum(x1, x2).astype(ret_dtype)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def reciprocal(
    x: Union[float, paddle.Tensor], /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    if x.dtype in [paddle.float32, paddle.float64]:
        return paddle.reciprocal(x)
    return paddle_backend.divide(1, x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def deg2rad(
    x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    if x.dtype in [paddle.int32, paddle.int64, paddle.bool]:
        return paddle.deg2rad(x.astype("float32")).astype(x.dtype)
    return paddle.deg2rad(x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def rad2deg(
    x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    if x.dtype in [paddle.int32, paddle.int64, paddle.bool]:
        return paddle.rad2deg(x.astype("float32")).astype(x.dtype)
    return paddle.rad2deg(x)


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def trunc_divide(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    return paddle_backend.trunc(paddle_backend.divide(x1, x2))


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def isreal(
    x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    if paddle.is_complex(x):
        return paddle.logical_not(x.imag().astype(bool))
    else:
        return paddle.ones_like(x, dtype="bool")


@with_unsupported_device_and_dtypes(
    {"2.4.2 and below": {"cpu": ("uint16", "bfloat16")}}, backend_version
)
def fmod(
    x1: paddle.Tensor,
    x2: paddle.Tensor,
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    res = paddle_backend.remainder(paddle_backend.abs(x1), paddle_backend.abs(x2))
    return paddle_backend.where(paddle_backend.less(x1, 0), -res, res)
