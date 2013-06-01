---
layout: default
title: MintPack
next: /tests
prev: /mintsystem
prev_title: MintSystem
up: /
up_title: Introduction
next_title: Test Suite
---

MintPack is a portable collection of data structures and modules.

To use MintPack in your project, add the top-level `include/` folder to your include paths, and compile and link with a lib build from the source in the `src/mintpack/` folder. There's a `CMakeLists.txt` located there, so you can use CMake to generate this lib for you. See the [test suite](../tests) for some examples of how it's used.

At this point, it's recommended that you just browse the [source](https://github.com/mintomic/mintomic/tree/master/src/mintpack), [header files](https://github.com/mintomic/mintomic/tree/master/include/mintpack) and [test cases](https://github.com/mintomic/mintomic/tree/master/tests) to get more information on how to use these data structures and modules.

## Lightweight Logger

    #include <mintpack/lwlogger.h>

A lightweight logging system, identical to the one described in [this blog post](http://preshing.com/20120522/lightweight-in-memory-logging), but made portable using Mintomic.

## Pseudorandom Number Generator

    #include <mintpack/random.h>

Implements `Random`, a self-seeding pseudorandom number generator with excellent pseudorandom distribution. It passes all 144 tests in [TestU01](http://www.iro.umontreal.ca/~simardr/testu01/tu01.html)'s Crush suite. Unlike `rand`, it returns values that are uniformly distributed in the complete range of 32-bit integers. Unlike many pseudorandom number generators, you don't have to seed it, yet two instances of `Random` are extremely unlikely to generate the same sequence. It uses [MintSystem](/mintsystem) services to help accomplish this.

`Random::generate` generates a pseudorandom `uint32_t`, while `Random::generateUnique` is guaranteed to return a [unique value](http://preshing.com/20121224/how-to-generate-a-sequence-of-unique-random-integers) for up to 4,294,967,296 calls, at which point it loops. Not thread-safe.

## Thread Synchronizer

    #include <mintpack/threadsynchronizer.h>
	
Spawns two or more threads using the same entry point function, and as much as possible, tries to kick them off simultaneously, ideally on different CPU cores.

## CPU Time Waster

    #include <mintpack/timewaster.h>

Performs tiny, random amounts of busy work on the CPU. Suitable for the experiment described in [this blog post](http://preshing.com/20121019/this-is-why-they-call-it-a-weakly-ordered-cpu).
