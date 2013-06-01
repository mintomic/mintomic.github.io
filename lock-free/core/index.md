---
layout: default
title: Core Definitions
next: /lock-free/atomics
prev: /lock-free/memory-model
prev_title: The Memory Model
up: /lock-free
up_title: Lock-Free API
next_title: Atomic Operations
---

Mintomic has its own internal set of core definitions, including portable integer types, compiler attributes and convenience functions. You can include it directly via `<mintomic/core.h>`.

In most cases, though, you'll probably want to include `<mintomic/mintomic.h>` instead, which includes the core definitions for you.

## Integer Types

All of the following fixed-size integer types are defined:

    int8_t      uint8_t
    int16_t     uint16_t
    int32_t     uint32_t
    int64_t     uint64_t

On platforms where `stdint.h` is available, it defines them by including that. On other platforms, such as Visual Studio 2008, it defines them on its own.

## Macros

##### MINT_DECL_ALIGNED

Declare memory alignment of a variable or structure. May not work [on local variables](http://gcc.gnu.org/bugzilla/show_bug.cgi?id=24691) in GCC.

    MINT_DECL_ALIGNED(int value, 16);

	typedef MINT_DECL_ALIGNED(struct, 16) Point { float x, y, z, w; };

##### MINT_C_INLINE

Declares *only* pure C functions (non-C++ class members) inline.

##### MINT_NO_INLINE

Disables automatic inlining on functions whose definitions are visible from the caller's scope.

##### MINT_THREAD_LOCAL

To declare thread-local variables.
