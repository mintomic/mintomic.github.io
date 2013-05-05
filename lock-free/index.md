---
layout: default
title: Lock-Free API
next: /lock-free/memory-model
prev: /
prev_title: Introduction
up: /
up_title: Introduction
next_title: The Memory Model
---

Mintomic's lock-free API is a single set of functions for lock-free programming which works on a variety of platforms. It's implemented in pure C, mainly as a set of header files.

To use the lock-free API in your project, simply add the top-level `include/` folder to your include path, and include `<mintomic/mintomic.h>`. More information can be found in the following subsections:

#### [The Memory Model](memory-model)

Mintomic relies on the compiler to make certain guarantees about the underlying memory model.

#### [Core Definitions](core)

Mintomic has its own internal set of core definitions, including portable integer types, compiler attributes and convenience functions. You can include it directly via `<mintomic/core.h>`.

#### [Atomic Operations](atomics)

Mintomic provides atomic data types such as `mint_atomic32_t`, and portable 32- and 64-bit variants of common atomic operations such as `mint_load_32_relaxed`, `mint_store_32_relaxed` and `mint_compare_exchange_32_relaxed`. In Mintomic, all atomic operations use relaxed memory ordering constraints.

#### [Memory Fences](memory-fences)

The only way to enforce memory ordering in Mintomic is by issuing an explicit fence instruction. Different instructions apply different ordering constraints, such as `mint_thread_fence_acquire`, `mint_thread_fence_release` and `mint_thread_fence_seq_cst`.
