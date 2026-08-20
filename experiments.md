# Experiment Log

## Project Question

Can property transaction prices be explained/predicted using
location, property type, tenure, new-build status and time?

## Project motivation

I'm hoping to improve my skills in random forests, regression
and just practice generally while working on a real project.

## Initial Hypotheses

### H1 — Location matters
Properties closer to major urban centres should have higher prices.
While this is basically a given, I'm also planning to graph
it's effect per city.

### H2 — Property type matters
Detached properties should sell for more than flats, on average.

### H3 — New builds differ
New-build properties may have systematically different prices.

## Experiment 1 — Data Reduction

### Thought process

The raw dataset contains detailed address information which is unlikely
to be useful for the research question.

I decided that:
- exact street names are unnecessary
- secondary address text is unnecessary
- month/day are unnecessary