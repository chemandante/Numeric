### Numeric

Repository contains some funny math scripts.

At first commit it contains only one script - `sum_squares`. This script prints all representations of the particular natural number
as a sum of two, three or four squares. For exapmle:
```
python3 sum_squares -4 55
```
prints all representation of `55` as a sum of four (or less) squares:
```
Total 3 decompositions found:
7²+2²+1²+1²
6²+3²+3²+1²
5²+5²+2²+1²
```

```
python3 sum_squares -3 54
```
prints all representation of `54` as a sum of three (or less) squares:
```
Total 3 decompositions found:
7²+2²+1²
6²+3²+3²
5²+5²+2²
```

```
python3 sum_squares -2 54
```
prints all representation of `54` as a sum of two (or less) squares:
```
54 can not be expressed as sum of two squares due to sum of two squares theorem.
```
