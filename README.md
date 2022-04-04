# r-place-among-us

![r/place Among Us image](/Figure_1.png)

This is a Python script that counts the number of Among Us crewmates in r/place then generates a marked copy. I counted 2097 on 4/3/2022, and I counted only 1013 just before r/place ended on 4/4/2022.

It takes the png scraped from r/place, reduces it into an array of indexes to a palette of colors, then runs some matching on those indexes using a set of stencils. I based the stencils on what I saw in r/place. Granted, this doesn't cover any random variation from the stencils, so my counts were rough.