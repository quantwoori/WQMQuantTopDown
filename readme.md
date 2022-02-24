# Quant Top Down with Eigen Portfolio

## Overview
<p>
To figure out the most varying stocks on a daily basis. 
Differ by universe.
</p>

<p>
Output should be

```
output = {
    "date": [some date],
    "freq": [some frequency],
    'infotyp': 'reference',
    "data": {
        "sort_by": "size",
        "eigen": {
            "big": [
                (some stock, some weight),
                (some stock, some weight),
                (some stock, some weight),
                ...
                ],
            "middle": [
                ...
                ],
            "small": [
                ...
                ],
            },
        }
    }   
```

</p>

## Pipeline
<p>

1. Get small sector universe from the database
2. For each sector S
   1. Perform a Eigen Decomposition and gain vectors that best explains the dataset
   2. Sort out the result as mentioned in the output format (some stock, some weight)
3. return the output in json format(for future use). 

</p>