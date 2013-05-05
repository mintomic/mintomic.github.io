---
layout: default
title: Introduction
next: /lock-free
next_title: Lock-Free API
---

Mintomic (short for "minimal atomic") is an API for low-level [lock-free programming](http://preshing.com/20120612/an-introduction-to-lock-free-programming) in C and C++.

## Design Goals

1. Efficient machine code generation.
1. Straightforward implementation.
1. Compatibility with older compilers. C11 and C++11 not required.

For more information, see the blog post [Introducing Mintomic](http://preshing.com/).

## Supported Platforms

Mintomic currently supports x86, x64, PowerPC, ARMv6 and ARMv7 and has been tested on Windows, MacOS, iOS, Linux and Xbox 360.

[CMake](http://www.cmake.org/) is required to build & run the test suite.

## Package Contents

Mintomic consists of the following submodules:

#### [Lock-Free API](lock-free)

Provides portable memory fences such as `mint_thread_fence_acquire`, atomic read-modify-write operations such as `mint_fetch_add_32_relaxed`, plus various helper functions, macros and types. Implemented in pure C, mainly as a set of header files.

#### [MintThreads](mintthreads)

Offers a portable way to create and manipulate threads, semaphore and timers across all supported platforms. Implemented as a pure C library.

#### [MintPack](mintpack)

A collection of data structures and modules built on top of Mintomic and MintThreads. Written as a platform-independent library in C++.

#### [Test Suite](tests)

A suite of unit tests in platform-independent C++ to validate the implemention of Mintomic primitives.

## License

Mintomic is distributed under the [Modified BSD License](http://directory.fsf.org/wiki/License:BSD_3Clause). See the `LICENSE` file.
