---
layout: default
title: Atomic Operations
next: /lock-free/memory-fences
prev: /lock-free/core
prev_title: Core Definitions
up: /lock-free
up_title: Lock-Free API
next_title: Memory Fences
---

Mintomic provides atomic data types such as `mint_atomic32_t`, and portable 32- and 64-bit variants of common atomic operations such as `mint_load_32_relaxed`, `mint_store_32_relaxed` and `mint_compare_exchange_32_relaxed`. In Mintomic, all atomic operations use relaxed memory ordering constraints.

You should consider every *other* method of manipulating shared memory to be non-atomic. For example, suppose you're storing a value to a shared integer `x` using a plain assignment expression such as `x = 5`. In the worst case, imagine a moment where the variable temporarily receives a random, garbage value in the process of switching from the old value to the new one -- with the possibility of another thread seeing it! (This is not such a far-fetched interpretation of reality on certain platforms when the integer is a 64-bit type.) The only guaranteed way to prevent it is to use an atomic operation.

To use these atomic operations in your project, simply add the top-level `include/` folder to your include path, and include `<mintomic/mintomic.h>`.

When targeting ARM, you must also compile and link with `src/mintomic/mintomic_gcc.c`.

## Atomic Data Types

To guarantee that a memory operation is performed atomically on all platforms, declare the variable using one of Mintomic's atomic data types:

* `mint_atomic32_t` holds a 32-bit unsigned integer.
* `mint_atomic64_t` holds a 64-bit unsigned integer.
* `mint_atomicPtr_t` holds a `void *`, which may be a 32- or 64-bit value depending on your platform.

These types are defined as simple structs with a single member, `_nonatomic`, containing the value itself. Variables defined using these types are guaranteed to be aligned to their natural size, which is required for performing atomic operations on every platform Mintomic supports, as long as you don't declare the variable on the stack. (In particular, note that 64-bit integers are not already guaranteed to be 8-byte aligned on some ARM compilers.)

You should not declare local variables using these atomic types because [some compilers do not correctly align local variables on the stack](http://gcc.gnu.org/bugzilla/show_bug.cgi?id=24691).

If the variable is a global or static class member, you can initialize it using a C-style initializer list:

    mint_atomic32_t readyFlag = { 0 };
    mint_atomic32_t MyClass::ms_flag = { 0 };

For an atomic pointer-sized integer, you can just use `mint_atomicPtr_t` and cast to and from `size_t`, `ptrdiff_t` or an equivalent pointer-sized integer type.

#### Non-Atomic Manipulation
    
In Mintomic, it is perfectly valid to manipulate the `_nonatomic` member of these atomic data types directly. Such operations are faster on some platforms, but considered non-atomic. Therefore, you should only use them in functions which only run when no other threads access the variable, such as in initialization code, shutdown code, or at a known safe point in your application's main loop. Additionally, these operations should always be delimited by a synchronizing operation, such as a memory fence, semaphore operation or creation of a thread.

    mint_atomic32_t readyFlag = { 0 };
    mint_atomic64_t sharedValue;
    
    void initialize(uint64_t initialValue)
    {
        sharedValue._nonatomic = initialValue;  // non-atomic assignment
        mint_thread_fence_release();            // synchronizing operation
        mint_store_32_relaxed(&readyFlag, 1);
    }

#### Casting Non-Atomic Variables to Atomic Types

If you have a plain integer or pointer in memory, and you can guarantee that it is already aligned to its natural size, it is valid to cast this variable to an atomic type and perform an atomic operation on it. However, if there are any non-atomic manipulations of this variable elsewhere, you must take the same precautions as you would when directly accessing the `_nonatomic` member of an atomic type.

    MINT_DECL_ALIGNED(uint64_t, 8) sharedValue;
    
    void atomicUpdate(uint64_t newValue)
    {
        mint_store_64_relaxed((mint_atomic64_t *) &sharedValue, newValue);
    }

## Loads and Stores

These functions perform either an atomic load or an atomic store on a shared variable:

    uint32_t mint_load_32_relaxed(mint_atomic32_t *object);
    void mint_store_32_relaxed(mint_atomic32_t *object, uint32_t value);
	
    uint64_t mint_load_64_relaxed(mint_atomic64_t *object);
    void mint_store_64_relaxed(mint_atomic64_t *object, uint64_t value);

    void *mint_load_ptr_relaxed(mint_atomicPtr_t *object);
    void mint_store_ptr_relaxed(mint_atomicPtr_t *object, void *desired);

## Read-Modify-Write Operations

These functions perform a read, modify and write as a single atomic operation. Each of them returns the previous value.

    uint32_t mint_compare_exchange_32_relaxed(mint_atomic32_t *object, uint32_t expected, uint32_t desired);
    uint32_t mint_fetch_add_32_relaxed(mint_atomic32_t *object, int32_t operand);
    uint32_t mint_fetch_and_32_relaxed(mint_atomic32_t *object, uint32_t operand);
    uint32_t mint_fetch_or_32_relaxed(mint_atomic32_t *object, uint32_t operand);

    uint64_t mint_compare_exchange_64_relaxed(mint_atomic64_t *object, uint64_t expected, uint64_t desired);
    uint64_t mint_fetch_add_64_relaxed(mint_atomic64_t *object, int64_t operand);
    uint64_t mint_fetch_and_64_relaxed(mint_atomic64_t *object, uint64_t operand);
    uint64_t mint_fetch_or_64_relaxed(mint_atomic64_t *object, uint64_t operand);

    void *mint_compare_exchange_ptr_relaxed(mint_atomicPtr_t *object, void *expected, void *desired);
    void *mint_fetch_add_ptr_relaxed(mint_atomicPtr_t *object, ptrdiff_t operand);
    void *mint_fetch_and_ptr_relaxed(mint_atomicPtr_t *object, size_t operand);
    void *mint_fetch_or_ptr_relaxed(mint_atomicPtr_t *object, size_t operand);
