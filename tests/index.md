---
layout: default
title: Test Suite
prev: /mintpack
prev_title: MintPack
up: /
up_title: Introduction
---

Mintomic comes with a test suite which you can build and run yourself. The only requirement is [CMake](http://www.cmake.org/). This test suite helps ensure that Mintomic was implemented correctly on each platform, while bringing the library to life with a working set of examples. Here’s what its output looks like on an iPhone 4S:

![](testsuite_iphone4s.png)

Every test case with a `_fail` suffix on its name contains an intentional bug. These tests are allowed to fail, and in general, designed to do so. The point is to show how incorrect lock-free code may succeed on certain platforms out of luck, depending on things like <a href="http://preshing.com/20120625/memory-ordering-at-compile-time">compiler ordering</a>, machine word size and <a href="http://preshing.com/20120930/weak-vs-strong-memory-models">hardware memory model</a>.

## How to Build

First, you must generate the projects using [CMake](http://www.cmake.org/). Open a command prompt in the `tests` folder, and do the following.

    mkdir build
    cd build
    cmake .. 

`cmake` takes an optional `-G` argument to specify which project generator to use. For example, the following command will use the Visual Studio 2012 generator. A complete list of available generators can be found by running `cmake` with no arguments.

    cmake -G "Visual Studio 11" ..

To generate projects for iOS devices, use the following.

    cmake -DCMAKE_TOOLCHAIN_FILE=../../../cmake/iOS.cmake -G "Xcode" ..

To build the project, simply use the generated project files as you would normally. Optionally, you can use CMake to perform the build step, too. For example, on Windows, you can use the command:

    cmake --build . --config Release

