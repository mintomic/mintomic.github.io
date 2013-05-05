---
layout: default
title: Memory Fences
next: /mintthreads
prev: /lock-free/atomics
prev_title: Atomic Operations
up: /lock-free
up_title: Lock-Free API
next_title: MintThreads
---

The only way to enforce memory ordering in Mintomic is by issuing an explicit fence instruction. Unlike the C/C++11 atomic library standards, there is no Mintomic primitive which simultaneously manipulates shared memory while issuing a memory barrier, like C++11's `std::atomic<int>::fetch_add` does for example. This actually works out quite well, because on the CPU architectures supported by Mintomic, a fence is always implemented using a separate machine instruction or compiler directive anyway.

To use Mintomic memory fences in your project, simply add the top-level `include/` folder to your include path and include `<mintomic/mintomic.h>`.

Thread fences can be used to establish *happens-before* relationships between threads, in the same sense defined by the C++11 standard. Signal fences only establish *happens-before* relationships between a thread and a signal handler running in the same thread.  

## Signal Fences

Signal fences in Mintomic fill the same purpose as the `std::atomic_signal_fence` function in C++11. They only guarantee memory ordering between threads which run on the same core, or between interrupts and signal handlers which run in the same thread. As such, they are not generally as useful for lock-free programming as thread fences. There are four variants of signal fences, each corresponding to a different C++11 ordering constraint:

{% highlight cpp %}
mint_signal_fence_consume();
mint_signal_fence_acquire();
mint_signal_fence_release();
mint_signal_fence_seq_cst();
{% endhighlight %}

`mint_signal_fence_consume` is always implemented as a no-op, and mainly exists to communicate the intent to acquire data through the `->` operator to other programmers. The other three variants are implemented as compiler barriers, in order to prevent any [memory ordering at compile time](http://preshing.com/20120625/memory-ordering-at-compile-time) that would break the ordering guarantee.

## Thread Fences

Thread fences are more useful. These fill the same purpose as the `std::atomic_thread_fence` function in C++11. They're basically required when you need to enforce correct memory ordering between multiple threads on a multicore device. There are four variants of thread fences, each corresponding to a C++11 ordering constraint:

{% highlight cpp %}
mint_thread_fence_consume();
mint_thread_fence_acquire();
mint_thread_fence_release();
mint_thread_fence_seq_cst();
{% endhighlight %}

On all currently supported platforms, `mint_thread_fence_consume` is implemented as a no-op. (If the DEC Alpha was supported, it would actually generate a CPU fence instruction.) It exists mainly to communicate to other programmers that you are relying on the data dependency barrier implied by the `->` operator.

`mint_thread_fence_acquire` and `mint_thread_fence_release` allow you to place [acquire and release semantics](http://preshing.com/20120913/acquire-and-release-semantics) on neighboring memory operations. On x86/64, a [strongly-ordered CPU](http://preshing.com/20120930/weak-vs-strong-memory-models), these are simply implemented as compiler barriers. On PowerPC, they generate the `lwsync` instruction, and on ARMv7, they generate `dmb`.

`mint_thread_fence_seq_cst` acts as both an acquire fence a release fence, and there is a single, global order of all `mint_thread_fence_seq_cst` operations executed across the system. It eliminates the kind of memory reordering demonstrated in [Memory Reordering Caught in the Act](http://preshing.com/20120515/memory-reordering-caught-in-the-act). On x86/64, it generates a `lock`ed instruction. On PowerPC, it generates `sync`, and on ARMv7, it generates `dmb`.
