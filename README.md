# r-place-among-us

![r/place Among Us image](/Figure_1.png)

This is a Python script that counts the number of Among Us crewmates in r/place then generates a marked copy. I last counted 2097!

It takes the png scraped from r/place, reduces it into an array of indexes to a palette of colors, then runs some matching on those indexes using a set of stencils. I based the stencils on what I saw in r/place. Granted, this doesn't cover any random variation from the stencils, so my count of 2097 was rough.