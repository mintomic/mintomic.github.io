---
layout: default
title: The Memory Model
next: /lock-free/core
prev: /lock-free
prev_title: Lock-Free API
up: /lock-free
up_title: Lock-Free API
next_title: Core Definitions
---

When you program using Mintomic, you must target a memory model that's identical to C/C++11's memory model using only low-level ordering constraints. In rough terms:

* Memory operations are weakly ordered.
* Memory barriers can be used to introduce *happens-before* relationship between operations on different threads.
* No load/store operation on shared memory may be considered atomic unless it uses one of the atomic data types.
* The compiler must not introduce data races which were not present in the original source code listing.

Unfortunately, some older compilers do not always comply with the last guarantee when certain optimization settings are enabled. Mintomic is therefore not 100% compatible with such compilers. Still, it is often possible to create a fully working application anyway. See the [Out-Of-Thin-Air Stores](#outofthinair_stores) section below.

Possibly helpful background reading:

* [Weak vs. Strong Memory Models](http://preshing.com/20120930/weak-vs-strong-memory-models)
* [Memory Barriers Are Like Source Control Operations](http://preshing.com/20120710/memory-barriers-are-like-source-control-operations)

## Weak Ordering

Mintomic is based on a weak software memory model. At runtime, the effects of load and store operations are permitted to occur in a different order than in the original source code listing, as long as those reorderings are guaranteed not to alter single-threaded program behavior. As a result, memory reordering is undetectable to a single-threaded application, but must be taken into account in lock-free programming.

The only way to limit such memory reordering is by performing an operation that acts as a memory barrier, thus establishing a *happens-before* relationship between operations on different threads. In C/C++11 atomics, there are many operations which act as memory barriers, but in Mintomic, the only way to obtain a memory barrier is by issuing an explicit [fence instruction](/lock-free/memory-fences).

In theory, to write correct lock-free code, one should imagine a machine which takes every possible liberty with memory reordering. The C/C++11 standards call this the "abstract machine". For full portability and correctness, the lock-free programmer is responsible for employing memory barriers as necessary to guarantee correct behavior even on this hypothetical abstract machine. In practice, a given real-world machine may not perform every type of memory reordering permitted by the software memory model, so it's very easy for some lock-free programming errors to slip by undetected.

## Out-Of-Thin-Air Stores

As mentioned above, it is possible for some older, non-C/C++11 compilers to introduce data races in cases where the original source code listing has none. Specifically, this can happen when the compiler introduces stores to shared memory in cases where the original source code listing performs no such store. Such undesired stores are sometimes referred to as [out-of-thin-air stores](http://preshing.com/20120625/memory-ordering-at-compile-time#out-of-thin-air).

An excellent example of a problematic out-of-thin-air store using GCC 4.3 is given in [this mailing list entry](http://gcc.gnu.org/ml/gcc/2007-10/msg00275.html).

Mintomic tries to minimize the risk of out-of-thin-air stores by detecting when the compiler is not compliant with the C/C++11 memory model and internally declaring its atomic data types `volatile`. This guarantees that there will be no out-of-thin-air stores on shared atomic variables such as `mint_atomic32_t` and `mint_atomic64_t`, which is the most important thing. However, it would still be possible to encounter the example from the mailing list, as no Mintomic data types were involved in that case.

This creates a dilemma for Mintomic (or any multithreaded code, for that matter), which aims for compatibility with older compilers, but cannot guarantee, in general, that data-race-free programs will remain data-race-free on such compilers.

If your compiler is prone to out-of-thin-air stores, you can:

* Ignore the risk of new data races (which is slim) and continue developing multithreaded applications anyway. This is what programmers have always historically done using GCC;
* Check the assembly listing for correctness wherever non-atomic shared variables are manipulated, especially if surrounded by conditional expressions or loops;
* Find workarounds if and when bad code generation is detected; or
* Plan for a compiler upgrade, ideally one supporting the C/C++11 memory model.

Compilers based on LLVM 3.0 and higher [guarantee not to make](http://llvm.org/docs/LangRef.html#memory-model-for-concurrent-operations) out-of-thin-air stores. Also, there don't appear to be any documented cases of out-of-thin-air stores using Microsoft Visual Studio 2005 or later.

(Note: Mintomic could probably be more formal about its memory model by specifically identifying which compilers and settings are known to inject data races, with test cases to verify known issues.)

## No Sequentially Consistent Data Types

C11, C++11 and Java 5 all provide ways for the programmer to treat shared variables as sequentially consistent data types. This means that at runtime, all operations acting across all such variables are guaranteed happen in a single, global order which is consistent between all threads.

Mintomic does not offer sequentially consistent data types.
