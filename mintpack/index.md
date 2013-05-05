---
layout: default
title: MintPack
next: /tests
prev: /mintthreads
prev_title: MintThreads
up: /
up_title: Introduction
next_title: Test Suite
---

MintPack is a portable collection of data structures and modules.

To use MintPack in your project, add the top-level `include/` folder to your include paths, and compile and link with a lib build from the source in the `src/mintpack/` folder. There's a `CMakeLists.txt` located there, so you can use CMake to generate this lib for you. See the [test suite](../tests) for some examples of how it's used.

At this point, it's recommended that you just browse the source, header files and test cases to get more information on how to use these data structures and modules.

## Lightweight Logger

    #include <mintpack/lwlogger.h>

A lightweight logging system, identical to the one described in [this blog post](http://preshing.com/20120522/lightweight-in-memory-logging), but made portable using Mintomic.

## Pseudorandom Number Generator

    #include <mintpack/random.h>

Implements the Mersenne Twister, a versatile pseudorandom number generator, returning integers with excellent pseudorandom distribution.

## Thread Synchronizer

    #include <mintpack/threadsynchronizer.h>
	
Spawns two or more threads using the same entry point function, and as much as possible, tries to kick them off simultaneously, ideally on different CPU cores.

## CPU Time Waster

    #include <mintpack/timewaster.h>

Performs tiny, random amounts of busy work on the CPU. Suitable for the experiment described in [this blog post](http://preshing.com/20121019/this-is-why-they-call-it-a-weakly-ordered-cpu).
