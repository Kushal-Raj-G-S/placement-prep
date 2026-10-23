# -*- coding: utf-8 -*-
"""
LINKS for the pattern library.

Two things live here:

  PLATFORM[pattern_id]  one topic hub per platform, so every pattern can be practised on
                        HackerEarth / HackerRank / GeeksforGeeks / CodeChef / InterviewBit as
                        well as LeetCode.  "cf" is a Codeforces TAG rather than a url --
                        verify_links.py pulls the most-solved real problems with that tag
                        straight from the Codeforces API.

  EXTRA[variant_id]     per-variant problems that are NOT on LeetCode.

Nothing here is trusted: run  python verify_links.py  and every url is fetched. Anything that
does not answer 200 is reported and dropped from the build instead of shipping as a dead link.
LeetCode links are not written by hand at all -- the "LC <id>" tags in pattern_library.py are
resolved against LeetCode's own problem index, which also corrects the titles.
"""

PLATFORM = {
 "two-pointers": {
   "cf": "two pointers",
   "he": "https://www.hackerearth.com/practice/data-structures/arrays/1-d/practice-problems/",
   "hr": "https://www.hackerrank.com/interview/interview-preparation-kit/arrays/",
   "gfg": "https://www.geeksforgeeks.org/two-pointers-technique/",
   "cc": "https://www.codechef.com/practice/arrays",
   "ib": "https://www.interviewbit.com/courses/programming/two-pointers/",
 },
 "sliding-window": {
   "cf": "two pointers",
   "he": "https://www.hackerearth.com/practice/data-structures/arrays/1-d/practice-problems/",
   "hr": "https://www.hackerrank.com/interview/interview-preparation-kit/arrays/",
   "gfg": "https://www.geeksforgeeks.org/window-sliding-technique/",
   "cc": "https://www.codechef.com/practice/arrays",
   "ib": "https://www.interviewbit.com/courses/programming/arrays/",
 },
 "prefix-sum": {
   "cf": "dp",
   "he": "https://www.hackerearth.com/practice/data-structures/arrays/1-d/practice-problems/",
   "hr": "https://www.hackerrank.com/interview/interview-preparation-kit/arrays/",
   "gfg": "https://www.geeksforgeeks.org/prefix-sum-array-implementation-applications-competitive-programming/",
   "cc": "https://www.codechef.com/practice/arrays",
   "ib": "https://www.interviewbit.com/courses/programming/arrays/",
 },
 "binary-search": {
   "cf": "binary search",
   "he": "https://www.hackerearth.com/practice/algorithms/searching/binary-search/practice-problems/",
   "hr": "https://www.hackerrank.com/interview/interview-preparation-kit/search/",
   "gfg": "https://www.geeksforgeeks.org/binary-search/",
   "cc": "https://www.codechef.com/practice/binary-search",
   "ib": "https://www.interviewbit.com/courses/programming/binary-search/",
 },
 "hashing": {
   "cf": "hashing",
   "he": "https://www.hackerearth.com/practice/data-structures/hash-tables/basics-of-hash-tables/practice-problems/",
   "hr": "https://www.hackerrank.com/interview/interview-preparation-kit/dictionaries-hashmaps/",
   "gfg": "https://www.geeksforgeeks.org/hashing-data-structure/",
   "cc": "https://www.codechef.com/practice/strings",
   "ib": "https://www.interviewbit.com/courses/programming/hashing/",
 },
 "monotonic-stack": {
   "cf": "data structures",
   "he": "https://www.hackerearth.com/practice/data-structures/stacks/basics-of-stacks/practice-problems/",
   "hr": "https://www.hackerrank.com/interview/interview-preparation-kit/stacks-queues/",
   "gfg": "https://www.geeksforgeeks.org/next-greater-element/",
   "cc": "https://www.codechef.com/practice/stacks-and-queues",
   "ib": "https://www.interviewbit.com/courses/programming/stacks-and-queues/",
 },
 "heap": {
   "cf": "data structures",
   "he": "https://www.hackerearth.com/practice/data-structures/trees/heapspriority-queues/practice-problems/",
   "hr": "https://www.hackerrank.com/domains/data-structures",
   "gfg": "https://www.geeksforgeeks.org/heap-data-structure/",
   "cc": "https://www.codechef.com/practice/heaps",
   "ib": "https://www.interviewbit.com/courses/programming/heaps-and-maps/",
 },
 "intervals": {
   "cf": "sortings",
   "he": "https://www.hackerearth.com/practice/algorithms/sorting/merge-sort/practice-problems/",
   "hr": "https://www.hackerrank.com/interview/interview-preparation-kit/sorting/",
   "gfg": "https://www.geeksforgeeks.org/merging-intervals/",
   "cc": "https://www.codechef.com/practice/sorting",
   "ib": "https://www.interviewbit.com/courses/programming/greedy-algorithm/",
 },
 "bits": {
   "cf": "bitmasks",
   "he": "https://www.hackerearth.com/practice/basic-programming/bit-manipulation/basics-of-bit-manipulation/practice-problems/",
   "hr": "https://www.hackerrank.com/interview/interview-preparation-kit/miscellaneous/",
   "gfg": "https://www.geeksforgeeks.org/bits-manipulation-important-tactics/",
   "cc": "https://www.codechef.com/practice/bit-manipulation",
   "ib": "https://www.interviewbit.com/courses/programming/bit-manipulation/",
 },
}

EXTRA = {
 "tp-ends": [
   {"n": "Sherlock and Anagrams", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/sherlock-and-anagrams/problem"},
   {"n": "Pairs", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/pairs/problem"},
   {"n": "Two pointers technique", "p": "GfG", "u": "https://www.geeksforgeeks.org/two-pointers-technique/"},
 ],
 "tp-write": [
   {"n": "Move all zeroes to end of array", "p": "GfG", "u": "https://www.geeksforgeeks.org/move-zeroes-end-array/"},
   {"n": "Remove duplicates from a sorted array", "p": "GfG", "u": "https://www.geeksforgeeks.org/remove-duplicates-sorted-array/"},
 ],
 "tp-merge": [
   {"n": "Merge two sorted arrays", "p": "GfG", "u": "https://www.geeksforgeeks.org/merge-two-sorted-arrays/"},
   {"n": "Find the Median", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/find-the-median/problem"},
 ],
 "tp-partition": [
   {"n": "Sort an array of 0s, 1s and 2s", "p": "GfG", "u": "https://www.geeksforgeeks.org/sort-an-array-of-0s-1s-and-2s/"},
   {"n": "Quicksort In-Place", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/quicksort3/problem"},
 ],
 "sw-fixed": [
   {"n": "Window sliding technique", "p": "GfG", "u": "https://www.geeksforgeeks.org/window-sliding-technique/"},
   {"n": "Maximum of all subarrays of size k", "p": "GfG", "u": "https://www.geeksforgeeks.org/sliding-window-maximum-maximum-of-all-subarrays-of-size-k/"},
 ],
 "sw-longest": [
   {"n": "Longest substring with k unique characters", "p": "GfG", "u": "https://www.geeksforgeeks.org/find-the-longest-substring-with-k-unique-characters-in-a-given-string/"},
   {"n": "Longest subarray with sum divisible by k", "p": "GfG", "u": "https://www.geeksforgeeks.org/longest-subarray-sum-divisible-k/"},
 ],
 "sw-shortest": [
   {"n": "Smallest window containing all characters of another string", "p": "GfG", "u": "https://www.geeksforgeeks.org/find-the-smallest-window-in-a-string-containing-all-characters-of-another-string/"},
   {"n": "Smallest subarray with sum greater than a given value", "p": "GfG", "u": "https://www.geeksforgeeks.org/minimum-length-subarray-sum-greater-given-value/"},
 ],
 "sw-exact": [
   {"n": "Count of subarrays having exactly K distinct elements", "p": "GfG", "u": "https://www.geeksforgeeks.org/count-of-subarrays-having-exactly-k-distinct-elements/"},
 ],
 "sw-deque": [
   {"n": "Sliding window maximum with a deque", "p": "GfG", "u": "https://www.geeksforgeeks.org/sliding-window-maximum-maximum-of-all-subarrays-of-size-k/"},
   {"n": "Deque-STL", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/deque-stl/problem"},
 ],
 "ps-range": [
   {"n": "Prefix sum array", "p": "GfG", "u": "https://www.geeksforgeeks.org/prefix-sum-array-implementation-applications-competitive-programming/"},
   {"n": "Equilibrium index of an array", "p": "GfG", "u": "https://www.geeksforgeeks.org/equilibrium-index-of-an-array/"},
 ],
 "ps-count": [
   {"n": "Subarray with given sum", "p": "GfG", "u": "https://www.geeksforgeeks.org/find-subarray-with-given-sum/"},
   {"n": "Count subarrays with sum divisible by k", "p": "GfG", "u": "https://www.geeksforgeeks.org/count-sub-arrays-sum-divisible-k/"},
 ],
 "ps-longest": [
   {"n": "Largest subarray with equal number of 0s and 1s", "p": "GfG", "u": "https://www.geeksforgeeks.org/largest-subarray-with-equal-number-of-0s-and-1s/"},
   {"n": "Longest subarray with sum k", "p": "GfG", "u": "https://www.geeksforgeeks.org/longest-sub-array-sum-k/"},
 ],
 "ps-2d": [
   {"n": "Submatrix sum queries", "p": "GfG", "u": "https://www.geeksforgeeks.org/submatrix-sum-queries/"},
 ],
 "ps-diff": [
   {"n": "Difference array, range update in O(1)", "p": "GfG", "u": "https://www.geeksforgeeks.org/difference-array-range-update-query-o1/"},
   {"n": "Array Manipulation", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/crush/problem"},
 ],
 "ps-suffix": [
   {"n": "A product array puzzle", "p": "GfG", "u": "https://www.geeksforgeeks.org/a-product-array-puzzle/"},
   {"n": "Trapping rain water", "p": "GfG", "u": "https://www.geeksforgeeks.org/trapping-rain-water/"},
 ],
 "bs-exact": [
   {"n": "Binary search", "p": "GfG", "u": "https://www.geeksforgeeks.org/binary-search/"},
   {"n": "Ice Cream Parlor", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/icecream-parlor/problem"},
 ],
 "bs-bound": [
   {"n": "Floor in a sorted array", "p": "GfG", "u": "https://www.geeksforgeeks.org/floor-in-a-sorted-array/"},
   {"n": "Count occurrences in a sorted array", "p": "GfG", "u": "https://www.geeksforgeeks.org/count-number-of-occurrences-or-frequency-in-a-sorted-array/"},
 ],
 "bs-answer": [
   {"n": "Allocate minimum number of pages", "p": "GfG", "u": "https://www.geeksforgeeks.org/allocate-minimum-number-pages/"},
   {"n": "Place k elements so the minimum distance is maximised", "p": "GfG", "u": "https://www.geeksforgeeks.org/place-k-elements-such-that-minimum-distance-is-maximized/"},
   {"n": "Binary search tutorial", "p": "HackerEarth", "u": "https://www.hackerearth.com/practice/algorithms/searching/binary-search/tutorial/"},
 ],
 "bs-rotated": [
   {"n": "Search in a sorted and rotated array", "p": "GfG", "u": "https://www.geeksforgeeks.org/search-an-element-in-a-sorted-and-pivoted-array/"},
   {"n": "Find a peak element", "p": "GfG", "u": "https://www.geeksforgeeks.org/find-a-peak-in-a-given-array/"},
 ],
 "bs-partition": [
   {"n": "Median of two sorted arrays of different sizes", "p": "GfG", "u": "https://www.geeksforgeeks.org/median-of-two-sorted-arrays-of-different-sizes/"},
 ],
 "hs-seen": [
   {"n": "Two Strings", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/two-strings/problem"},
   {"n": "Longest consecutive subsequence", "p": "GfG", "u": "https://www.geeksforgeeks.org/longest-consecutive-subsequence/"},
 ],
 "hs-freq": [
   {"n": "Sherlock and Anagrams", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/sherlock-and-anagrams/problem"},
   {"n": "Counting frequencies of array elements", "p": "GfG", "u": "https://www.geeksforgeeks.org/counting-frequencies-of-array-elements/"},
   {"n": "Find k numbers with most occurrences", "p": "GfG", "u": "https://www.geeksforgeeks.org/find-k-numbers-occurrences-given-array/"},
 ],
 "hs-index": [
   {"n": "Count Triplets", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/count-triplets-1/problem"},
   {"n": "Check if a pair with a given sum exists", "p": "GfG", "u": "https://www.geeksforgeeks.org/check-if-pair-with-given-sum-exists-in-array/"},
 ],
 "hs-group": [
   {"n": "Print all anagrams together", "p": "GfG", "u": "https://www.geeksforgeeks.org/given-a-sequence-of-words-print-all-anagrams-together/"},
 ],
 "hs-cyclic": [
   {"n": "Find the missing number", "p": "GfG", "u": "https://www.geeksforgeeks.org/find-the-missing-number/"},
   {"n": "Smallest positive missing number", "p": "GfG", "u": "https://www.geeksforgeeks.org/find-the-smallest-positive-number-missing-from-an-unsorted-array/"},
 ],
 "ms-next": [
   {"n": "Next greater element", "p": "GfG", "u": "https://www.geeksforgeeks.org/next-greater-element/"},
   {"n": "The stock span problem", "p": "GfG", "u": "https://www.geeksforgeeks.org/the-stock-span-problem/"},
 ],
 "ms-hist": [
   {"n": "Largest rectangle under a histogram", "p": "GfG", "u": "https://www.geeksforgeeks.org/largest-rectangle-under-histogram/"},
   {"n": "Largest Rectangle", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/largest-rectangle/problem"},
 ],
 "ms-match": [
   {"n": "Balanced Brackets", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/balanced-brackets/problem"},
   {"n": "Check for balanced parentheses", "p": "GfG", "u": "https://www.geeksforgeeks.org/check-for-balanced-parentheses-in-an-expression/"},
   {"n": "Maximum Element", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/maximum-element/problem"},
 ],
 "ms-greedy": [
   {"n": "Build the lowest number by removing n digits", "p": "GfG", "u": "https://www.geeksforgeeks.org/build-lowest-number-by-removing-n-digits-from-a-given-number/"},
 ],
 "hp-topk": [
   {"n": "Jesse and Cookies", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/jesse-and-cookies/problem"},
   {"n": "K largest or smallest elements in an array", "p": "GfG", "u": "https://www.geeksforgeeks.org/k-largestor-smallest-elements-in-an-array/"},
   {"n": "QHEAP1", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/qheap1/problem"},
 ],
 "hp-merge": [
   {"n": "Merge k sorted arrays", "p": "GfG", "u": "https://www.geeksforgeeks.org/merge-k-sorted-arrays/"},
 ],
 "hp-two": [
   {"n": "Find the Running Median", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/find-the-running-median/problem"},
   {"n": "Median in a stream of integers", "p": "GfG", "u": "https://www.geeksforgeeks.org/median-of-stream-of-integers-running-integers/"},
 ],
 "hp-greedy": [
   {"n": "Minimum platforms required for a railway station", "p": "GfG", "u": "https://www.geeksforgeeks.org/minimum-number-platforms-required-railwaybus-station/"},
   {"n": "Connect n ropes with minimum cost", "p": "GfG", "u": "https://www.geeksforgeeks.org/connect-n-ropes-minimum-cost/"},
 ],
 "iv-merge": [
   {"n": "Merging intervals", "p": "GfG", "u": "https://www.geeksforgeeks.org/merging-intervals/"},
 ],
 "iv-insert": [
   {"n": "Insert into a sorted, non-overlapping interval array", "p": "GfG", "u": "https://www.geeksforgeeks.org/insert-in-sorted-and-non-overlapping-interval-array/"},
 ],
 "iv-greedy": [
   {"n": "Activity selection problem", "p": "GfG", "u": "https://www.geeksforgeeks.org/activity-selection-problem-greedy-algo-1/"},
   {"n": "Greedy Florist", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/greedy-florist/problem"},
 ],
 "iv-sweep": [
   {"n": "Minimum platforms required for a railway station", "p": "GfG", "u": "https://www.geeksforgeeks.org/minimum-number-platforms-required-railwaybus-station/"},
 ],
 "iv-sortkey": [
   {"n": "Arrange numbers to form the biggest number", "p": "GfG", "u": "https://www.geeksforgeeks.org/given-an-array-of-numbers-arrange-the-numbers-to-form-the-biggest-number/"},
   {"n": "Mark and Toys", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/mark-and-toys/problem"},
 ],
 "bt-xor": [
   {"n": "Find the number occurring an odd number of times", "p": "GfG", "u": "https://www.geeksforgeeks.org/find-the-number-occurring-odd-number-of-times/"},
   {"n": "Lonely Integer", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/lonely-integer/problem"},
   {"n": "Maximum subarray XOR", "p": "GfG", "u": "https://www.geeksforgeeks.org/find-the-maximum-subarray-xor-in-a-given-array/"},
   {"n": "Bitwise hacks for competitive programming", "p": "GfG", "u": "https://www.geeksforgeeks.org/bitwise-hacks-for-competitive-programming/"},
 ],
 "bt-subsets": [
   {"n": "Power set", "p": "GfG", "u": "https://www.geeksforgeeks.org/power-set/"},
   {"n": "Subset sum problem", "p": "GfG", "u": "https://www.geeksforgeeks.org/subset-sum-problem-dp-25/"},
 ],
 "bt-dp": [
   {"n": "Travelling salesman problem", "p": "GfG", "u": "https://www.geeksforgeeks.org/travelling-salesman-problem-set-1/"},
   {"n": "Bitmasking and dynamic programming", "p": "GfG", "u": "https://www.geeksforgeeks.org/bitmasking-and-dynamic-programming-set-1-count-ways-to-assign-unique-cap-to-every-person/"},
 ],
 "bt-tricks": [
   {"n": "Bit manipulation, important tactics", "p": "GfG", "u": "https://www.geeksforgeeks.org/bits-manipulation-important-tactics/"},
   {"n": "Count set bits in an integer", "p": "GfG", "u": "https://www.geeksforgeeks.org/count-set-bits-in-an-integer/"},
   {"n": "Flipping bits", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/flipping-bits/problem"},
 ],
}

# ---- batch 3: linked lists, trees, graphs, DP, search & greedy -----------------
PLATFORM.update({
 "linked-list": {
   "cf": "implementation",
   "he": "https://www.hackerearth.com/practice/data-structures/linked-list/singly-linked-list/practice-problems/",
   "hr": "https://www.hackerrank.com/interview/interview-preparation-kit/linked-lists/",
   "gfg": "https://www.geeksforgeeks.org/data-structures/linked-list/",
   "cc": "https://www.codechef.com/practice/linked-lists",
   "ib": "https://www.interviewbit.com/courses/programming/linked-lists/",
 },
 "tree-dfs": {
   "cf": "dfs and similar",
   "he": "https://www.hackerearth.com/practice/data-structures/trees/binary-search-tree/practice-problems/",
   "hr": "https://www.hackerrank.com/interview/interview-preparation-kit/trees/",
   "gfg": "https://www.geeksforgeeks.org/binary-tree-data-structure/",
   "ib": "https://www.interviewbit.com/courses/programming/trees/",
 },
 "tree-bfs": {
   "cf": "trees",
   "he": "https://www.hackerearth.com/practice/algorithms/graphs/breadth-first-search/practice-problems/",
   "hr": "https://www.hackerrank.com/interview/interview-preparation-kit/trees/",
   "gfg": "https://www.geeksforgeeks.org/level-order-tree-traversal/",
   "ib": "https://www.interviewbit.com/courses/programming/trees/",
 },
 "trie": {
   "cf": "strings",
   "he": "https://www.hackerearth.com/practice/data-structures/advanced-data-structures/trie-keyword-tree/practice-problems/",
   "hr": "https://www.hackerrank.com/domains/data-structures",
   "gfg": "https://www.geeksforgeeks.org/trie-insert-and-search/",
   "cc": "https://www.codechef.com/practice/strings",
   "ib": "https://www.interviewbit.com/courses/programming/trees/",
 },
 "grid": {
   "cf": "dfs and similar",
   "he": "https://www.hackerearth.com/practice/algorithms/graphs/depth-first-search/practice-problems/",
   "hr": "https://www.hackerrank.com/interview/interview-preparation-kit/graphs/",
   "gfg": "https://www.geeksforgeeks.org/find-number-of-islands/",
   "cc": "https://www.codechef.com/practice/graph",
   "ib": "https://www.interviewbit.com/courses/programming/graph-data-structure-algorithms/",
 },
 "toposort": {
   "cf": "graphs",
   "he": "https://www.hackerearth.com/practice/algorithms/graphs/topological-sort/practice-problems/",
   "hr": "https://www.hackerrank.com/interview/interview-preparation-kit/graphs/",
   "gfg": "https://www.geeksforgeeks.org/topological-sorting/",
   "cc": "https://www.codechef.com/practice/graph",
   "ib": "https://www.interviewbit.com/courses/programming/graph-data-structure-algorithms/",
 },
 "shortest-path": {
   "cf": "shortest paths",
   "he": "https://www.hackerearth.com/practice/algorithms/graphs/shortest-path-algorithms/practice-problems/",
   "hr": "https://www.hackerrank.com/interview/interview-preparation-kit/graphs/",
   "gfg": "https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/",
   "cc": "https://www.codechef.com/practice/graph",
   "ib": "https://www.interviewbit.com/courses/programming/graph-data-structure-algorithms/",
 },
 "dsu": {
   "cf": "dsu",
   "he": "https://www.hackerearth.com/practice/data-structures/disjoint-data-strutures/basics-of-disjoint-data-structures/practice-problems/",
   "hr": "https://www.hackerrank.com/interview/interview-preparation-kit/graphs/",
   "gfg": "https://www.geeksforgeeks.org/introduction-to-disjoint-set-data-structure-or-union-find-algorithm/",
   "cc": "https://www.codechef.com/practice/graph",
   "ib": "https://www.interviewbit.com/courses/programming/graph-data-structure-algorithms/",
 },
 "dp-1d": {
   "cf": "dp",
   "he": "https://www.hackerearth.com/practice/algorithms/dynamic-programming/introduction-to-dynamic-programming-1/practice-problems/",
   "hr": "https://www.hackerrank.com/interview/interview-preparation-kit/dynamic-programming/",
   "gfg": "https://www.geeksforgeeks.org/dynamic-programming/",
   "cc": "https://www.codechef.com/practice/dynamic-programming",
   "ib": "https://www.interviewbit.com/courses/programming/dynamic-programming/",
 },
 "dp-2d": {
   "cf": "dp",
   "he": "https://www.hackerearth.com/practice/algorithms/dynamic-programming/2-dimensional/practice-problems/",
   "hr": "https://www.hackerrank.com/interview/interview-preparation-kit/dynamic-programming/",
   "gfg": "https://www.geeksforgeeks.org/longest-common-subsequence-dp-4/",
   "cc": "https://www.codechef.com/practice/dynamic-programming",
   "ib": "https://www.interviewbit.com/courses/programming/dynamic-programming/",
 },
 "backtracking": {
   "cf": "brute force",
   "he": "https://www.hackerearth.com/practice/basic-programming/recursion/recursion-and-backtracking/practice-problems/",
   "hr": "https://www.hackerrank.com/interview/interview-preparation-kit/recursion-backtracking/",
   "gfg": "https://www.geeksforgeeks.org/backtracking-algorithms/",
   "ib": "https://www.interviewbit.com/courses/programming/backtracking/",
 },
 "greedy": {
   "cf": "greedy",
   "he": "https://www.hackerearth.com/practice/algorithms/greedy/basics-of-greedy-algorithms/practice-problems/",
   "hr": "https://www.hackerrank.com/interview/interview-preparation-kit/greedy-algorithms/",
   "gfg": "https://www.geeksforgeeks.org/greedy-algorithms/",
   "cc": "https://www.codechef.com/practice/greedy-algorithms",
   "ib": "https://www.interviewbit.com/courses/programming/greedy-algorithm/",
 },
})

EXTRA.update({
 "ll-fastslow": [
   {"n": "Detect a loop in a linked list", "p": "GfG", "u": "https://www.geeksforgeeks.org/detect-loop-in-a-linked-list/"},
   {"n": "Cycle Detection", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/detect-whether-a-linked-list-contains-a-cycle/problem"},
 ],
 "ll-reverse": [
   {"n": "Reverse a linked list", "p": "GfG", "u": "https://www.geeksforgeeks.org/reverse-a-linked-list/"},
   {"n": "Reverse a Linked List", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/reverse-a-linked-list/problem"},
 ],
 "ll-dummy": [
   {"n": "Remove duplicates from a sorted linked list", "p": "GfG", "u": "https://www.geeksforgeeks.org/remove-duplicates-from-a-sorted-linked-list/"},
   {"n": "Delete a Node", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/delete-a-node-from-a-linked-list/problem"},
 ],
 "ll-merge": [
   {"n": "Merge two sorted linked lists", "p": "GfG", "u": "https://www.geeksforgeeks.org/merge-two-sorted-linked-lists/"},
   {"n": "Merge two sorted linked lists", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/merge-two-sorted-linked-lists/problem"},
 ],
 "td-up": [
   {"n": "Height of a binary tree", "p": "GfG", "u": "https://www.geeksforgeeks.org/write-a-c-program-to-find-the-maximum-depth-or-height-of-a-tree/"},
   {"n": "Diameter of a binary tree", "p": "GfG", "u": "https://www.geeksforgeeks.org/diameter-of-a-binary-tree/"},
   {"n": "Height of a Binary Tree", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/tree-height-of-a-binary-tree/problem"},
 ],
 "td-down": [
   {"n": "Root to leaf paths", "p": "GfG", "u": "https://www.geeksforgeeks.org/given-a-binary-tree-print-all-root-to-leaf-paths/"},
   {"n": "Root to leaf path sum", "p": "GfG", "u": "https://www.geeksforgeeks.org/root-to-leaf-path-sum-equal-to-a-given-number/"},
 ],
 "td-bst": [
   {"n": "Check if a binary tree is a BST", "p": "GfG", "u": "https://www.geeksforgeeks.org/a-program-to-check-if-a-binary-tree-is-bst-or-not/"},
   {"n": "Binary Search Tree: Insertion", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/binary-search-tree-insertion/problem"},
 ],
 "td-lca": [
   {"n": "Lowest common ancestor in a binary tree", "p": "GfG", "u": "https://www.geeksforgeeks.org/lowest-common-ancestor-binary-tree-set-1/"},
   {"n": "BST: Lowest Common Ancestor", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/binary-search-tree-lowest-common-ancestor/problem"},
 ],
 "tb-levels": [
   {"n": "Level order traversal", "p": "GfG", "u": "https://www.geeksforgeeks.org/level-order-tree-traversal/"},
   {"n": "Tree: Level Order Traversal", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/tree-level-order-traversal/problem"},
   {"n": "Print left view of a binary tree", "p": "GfG", "u": "https://www.geeksforgeeks.org/print-left-view-binary-tree/"},
 ],
 "tr-basic": [
   {"n": "Trie insert and search", "p": "GfG", "u": "https://www.geeksforgeeks.org/trie-insert-and-search/"},
   {"n": "Contacts", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/contacts/problem"},
 ],
 "tr-search": [
   {"n": "Word break problem, trie solution", "p": "GfG", "u": "https://www.geeksforgeeks.org/word-break-problem-trie-solution/"},
   {"n": "No Prefix Set", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/no-prefix-set/problem"},
 ],
})

EXTRA.update({
 "gr-flood": [
   {"n": "Find the number of islands", "p": "GfG", "u": "https://www.geeksforgeeks.org/find-number-of-islands/"},
   {"n": "Flood fill algorithm", "p": "GfG", "u": "https://www.geeksforgeeks.org/flood-fill-algorithm-implement-fill-paint/"},
   {"n": "Connected Cells in a Grid", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/connected-cell-in-a-grid/problem"},
 ],
 "gr-bfs": [
   {"n": "Shortest path in a binary maze", "p": "GfG", "u": "https://www.geeksforgeeks.org/shortest-path-in-a-binary-maze/"},
   {"n": "BFS: Shortest Reach in a Graph", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/bfsshortreach/problem"},
   {"n": "Breadth first search tutorial", "p": "HackerEarth", "u": "https://www.hackerearth.com/practice/algorithms/graphs/breadth-first-search/tutorial/"},
 ],
 "gr-multi": [
   {"n": "Minimum time to rot all oranges", "p": "GfG", "u": "https://www.geeksforgeeks.org/minimum-time-required-so-that-all-oranges-become-rotten/"},
   {"n": "Distance of the nearest cell having 1", "p": "GfG", "u": "https://www.geeksforgeeks.org/distance-nearest-cell-1-binary-matrix/"},
 ],
 "to-kahn": [
   {"n": "Topological sorting", "p": "GfG", "u": "https://www.geeksforgeeks.org/topological-sorting/"},
   {"n": "Kahn's algorithm, indegree based", "p": "GfG", "u": "https://www.geeksforgeeks.org/topological-sorting-indegree-based-solution/"},
   {"n": "Topological sort tutorial", "p": "HackerEarth", "u": "https://www.hackerearth.com/practice/algorithms/graphs/topological-sort/tutorial/"},
 ],
 "to-dfs": [
   {"n": "Detect a cycle in a directed graph", "p": "GfG", "u": "https://www.geeksforgeeks.org/detect-cycle-in-a-graph/"},
 ],
 "sp-dijkstra": [
   {"n": "Dijkstra's shortest path algorithm", "p": "GfG", "u": "https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/"},
   {"n": "Dijkstra: Shortest Reach 2", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/dijkstrashortreach/problem"},
   {"n": "Shortest path algorithms tutorial", "p": "HackerEarth", "u": "https://www.hackerearth.com/practice/algorithms/graphs/shortest-path-algorithms/tutorial/"},
 ],
 "sp-bellman": [
   {"n": "Bellman-Ford algorithm", "p": "GfG", "u": "https://www.geeksforgeeks.org/bellman-ford-algorithm-dp-23/"},
 ],
 "sp-floyd": [
   {"n": "Floyd-Warshall algorithm", "p": "GfG", "u": "https://www.geeksforgeeks.org/floyd-warshall-algorithm-dp-16/"},
   {"n": "Floyd : City of Blinding Lights", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/floyd-city-of-blinding-lights/problem"},
 ],
 "dsu-connect": [
   {"n": "Disjoint set union (union-find)", "p": "GfG", "u": "https://www.geeksforgeeks.org/introduction-to-disjoint-set-data-structure-or-union-find-algorithm/"},
   {"n": "Components in a graph", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/components-in-graph/problem"},
 ],
 "dsu-cycle": [
   {"n": "Union-find and cycle detection", "p": "GfG", "u": "https://www.geeksforgeeks.org/union-find/"},
 ],
 "dsu-kruskal": [
   {"n": "Kruskal's minimum spanning tree algorithm", "p": "GfG", "u": "https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/"},
   {"n": "Kruskal (MST): Really Special Subtree", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/kruskalmstrsub/problem"},
 ],
})

EXTRA.update({
 "dp-linear": [
   {"n": "Count ways to reach the n-th stair", "p": "GfG", "u": "https://www.geeksforgeeks.org/count-ways-reach-nth-stair/"},
   {"n": "Maximum sum with no two adjacent", "p": "GfG", "u": "https://www.geeksforgeeks.org/find-maximum-possible-stolen-value-houses/"},
   {"n": "Dynamic programming tutorial", "p": "HackerEarth", "u": "https://www.hackerearth.com/practice/algorithms/dynamic-programming/introduction-to-dynamic-programming-1/tutorial/"},
 ],
 "dp-kadane": [
   {"n": "Largest sum contiguous subarray (Kadane)", "p": "GfG", "u": "https://www.geeksforgeeks.org/largest-sum-contiguous-subarray/"},
   {"n": "The Maximum Subarray", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/maxsubarray/problem"},
 ],
 "dp-coin": [
   {"n": "Minimum number of coins that make a change", "p": "GfG", "u": "https://www.geeksforgeeks.org/find-minimum-number-of-coins-that-make-a-change/"},
   {"n": "Coin change, count the ways", "p": "GfG", "u": "https://www.geeksforgeeks.org/coin-change-dp-7/"},
   {"n": "The Coin Change Problem", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/coin-change/problem"},
 ],
 "dp-lis": [
   {"n": "Longest increasing subsequence", "p": "GfG", "u": "https://www.geeksforgeeks.org/longest-increasing-subsequence-dp-3/"},
   {"n": "LIS in O(n log n)", "p": "GfG", "u": "https://www.geeksforgeeks.org/longest-monotonically-increasing-subsequence-size-n-log-n/"},
 ],
 "dp-grid": [
   {"n": "Count all possible paths in a matrix", "p": "GfG", "u": "https://www.geeksforgeeks.org/count-possible-paths-top-left-bottom-right-nxm-matrix/"},
   {"n": "Minimum cost path in a matrix", "p": "GfG", "u": "https://www.geeksforgeeks.org/min-cost-path-dp-6/"},
 ],
 "dp-twostring": [
   {"n": "Longest common subsequence", "p": "GfG", "u": "https://www.geeksforgeeks.org/longest-common-subsequence-dp-4/"},
   {"n": "Edit distance", "p": "GfG", "u": "https://www.geeksforgeeks.org/edit-distance-dp-5/"},
   {"n": "Common Child", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/common-child/problem"},
 ],
 "dp-knapsack": [
   {"n": "0-1 knapsack problem", "p": "GfG", "u": "https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/"},
   {"n": "Partition problem, equal sum subsets", "p": "GfG", "u": "https://www.geeksforgeeks.org/partition-problem-dp-18/"},
 ],
 "dp-interval": [
   {"n": "Matrix chain multiplication", "p": "GfG", "u": "https://www.geeksforgeeks.org/matrix-chain-multiplication-dp-8/"},
   {"n": "Palindrome partitioning, minimum cuts", "p": "GfG", "u": "https://www.geeksforgeeks.org/palindrome-partitioning-dp-17/"},
 ],
 "bk-subsets": [
   {"n": "Power set", "p": "GfG", "u": "https://www.geeksforgeeks.org/power-set/"},
   {"n": "Combinational sum", "p": "GfG", "u": "https://www.geeksforgeeks.org/combinational-sum/"},
   {"n": "Recursion and backtracking tutorial", "p": "HackerEarth", "u": "https://www.hackerearth.com/practice/basic-programming/recursion/recursion-and-backtracking/tutorial/"},
 ],
 "bk-perms": [
   {"n": "Print all permutations of a string", "p": "GfG", "u": "https://www.geeksforgeeks.org/write-a-c-program-to-print-all-permutations-of-a-given-string/"},
 ],
 "bk-board": [
   {"n": "N-Queen problem", "p": "GfG", "u": "https://www.geeksforgeeks.org/n-queen-problem-backtracking-3/"},
   {"n": "Sudoku solver using backtracking", "p": "GfG", "u": "https://www.geeksforgeeks.org/sudoku-backtracking-7/"},
   {"n": "Rat in a maze", "p": "GfG", "u": "https://www.geeksforgeeks.org/rat-in-a-maze-backtracking-2/"},
 ],
 "gr-reach": [
   {"n": "Minimum number of jumps to reach the end", "p": "GfG", "u": "https://www.geeksforgeeks.org/minimum-number-of-jumps-to-reach-end-of-a-given-array/"},
   {"n": "Find a tour that visits all petrol pumps", "p": "GfG", "u": "https://www.geeksforgeeks.org/find-a-tour-that-visits-all-stations/"},
 ],
 "gr-pair": [
   {"n": "Greedy algorithms tutorial", "p": "HackerEarth", "u": "https://www.hackerearth.com/practice/algorithms/greedy/basics-of-greedy-algorithms/tutorial/"},
   {"n": "Minimum product subset of an array", "p": "GfG", "u": "https://www.geeksforgeeks.org/minimum-product-subset-array/"},
 ],
 "gr-local": [
   {"n": "Activity selection problem", "p": "GfG", "u": "https://www.geeksforgeeks.org/activity-selection-problem-greedy-algo-1/"},
   {"n": "Job sequencing problem", "p": "GfG", "u": "https://www.geeksforgeeks.org/job-sequencing-problem/"},
   {"n": "Greedy Florist", "p": "HackerRank", "u": "https://www.hackerrank.com/challenges/greedy-florist/problem"},
 ],
})
