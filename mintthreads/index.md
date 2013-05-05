---
layout: default
title: MintThreads
next: /mintpack
prev: /lock-free/memory-fences
prev_title: Memory Fences
up: /
up_title: Introduction
next_title: MintPack
---

MintThreads offers a minimal, portable way to create and manipulate threads, semaphores and timers across all supported platforms. If your project requires a more complete set of PThreads functionality, and you still want Windows compatibility, you might be interested in the [PThreads-Win32](http://sourceware.org/pthreads-win32/) project.

To use MintThreads in your project, add the top-level `include/` folder to your include path, then include the appropriate headers such as `<mintthreads/thread.h>`. To use MintThreads on UNIX-like platforms, including Linux, MacOS or iOS, you must also compile and link using the `-pthread` option.

On all platforms, you must also compile and link with a lib built from the appropriate source in the `src/mintthreads/` folder. There's a `CMakeLists.txt` located there, so you can use CMake to generate this lib for you. See the [tests](/tests) for some examples of how it's used.

## Thread Creation

You can use the following functions to create threads and wait for threads to complete. These are roughly inspired by POSIX thread creation functions, [`pthread_create`](http://www.kernel.org/doc/man-pages/online/pages/man3/pthread_create.3.html) and [`pthread_join`](http://www.kernel.org/doc/man-pages/online/pages/man3/pthread_join.3.html).

`mint_thread_t` is an opaque pointer type which represents a handle to the thread. The first argument to `mint_thread_create` is actually a pointer to a pointer which receives the new handle.

{% highlight cpp %}
#include <mintthreads/thread.h>

int mint_thread_create(mint_thread_t *thread, void *(*start_routine) (void *), void *arg);
int mint_thread_join(mint_thread_t thread, void **retval);
{% endhighlight %}

## Semaphores

You can use the following functions to create, manipulate and destroy semaphores. These are different from POSIX semaphores, though they share a similar API.

{% highlight cpp %}
#include <mintthreads/semaphore.h>

mint_sem_t *mint_sem_create();
int mint_sem_destroy(mint_sem_t *sem);
int mint_sem_post(mint_sem_t *sem);
int mint_sem_wait(mint_sem_t *sem);
{% endhighlight %}

These functions provide unnamed semaphores even on Apple operating systems, which [do not natively support them](http://www.cocos2d-x.org/boards/6/topics/10583). Since the semaphores are unnamed, they cannot be shared between different processes.

Unlike a POSIX semaphore, `mint_sem_wait` is guaranteed never to return early with an `EINTR` error due to a signal interrupt. It is presumed that nobody using Mintomic semaphores will care about signal interrupts. On several platforms, including some configurations of Xcode and iOS, [every debug event causes a signal interrupt](http://stackoverflow.com/questions/2013181/gdb-causes-sem-wait-to-fail-with-eintr-error), which would otherwise break the logic of the application being debugged. Mintomic semaphores protect you from this particular surprise.

## Timers

Mintomic provides portable functions for low-overhead, high-resolution timers suitable for timing sections of code in the 0.5 microsecond range and up.

{% highlight cpp %}
#include <mintthreads/timer.h>

extern double mint_timer_secondsToTicks;
extern double mint_timer_ticksToSeconds;

void mint_timer_initialize();
mint_timer_tick mint_timer_get();
{% endhighlight %}

At program startup, you must call `mint_timer_initialize`.

After that, you can safely call `mint_timer_get`, which returns `mint_timer_tick` values. You can subtract these values to obtain timing deltas, then convert them to and from seconds by using the conversion ratios `mint_timer_ticksToSeconds` and `mint_timer_secondsToTicks`.
