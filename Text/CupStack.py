# -*- coding: utf-8 -*-
# @Author: cb

## My first python program

count = 1
print("So you're building a 2D pyramid of cups")
target = input("Enter total number of cups:")


def sum_range(n):
    return sum(range(0, n))


if target == 0:
    print("How can you build with no cups??")
else:
    while sum_range(count) < target:
        print(sum_range(count))
        count += 1
    remaining = target - sum_range(count - 1)
    print(
        "Use a base with %s cups. You will have %s left over." % (count - 2, remaining)
    )
