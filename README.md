# BU HUB greedy algorithm
An algorithm to help knock out your non-major graduation requirements

> "In the Hub, students can pursue their interests by taking courses across BU’s 10 undergraduate schools and colleges as they fulfill their general education requirements. How students experience learning in the Hub is up to them–the program is designed to integrate with a student’s major studies while encouraging exploration. Students can select from a wide range of courses that carry Hub units, both in and outside of their major."
-https://www.bu.edu/hub/hub-courses/

```shell
├── README.md
├── catalog
│   ├── catalog.json
│   ├── catalog_sorted.json
│   ├── set.json
│   └── set_everything.json
├── sample\ outputs
│   └── subset-whowe-courses
├── search.js
└── set_cover.py
```

### The Problem

BU students know how annoying the HUB is, and how confusing it is to ensure they aren't forgetting any requirements, as even one overlooked unit necessitates a whole extra 4 credit class.

One way to formulate the BU HUB course selection problem is as a graph problem.  Given a graph G={U,V,E}, let U be the available courses, V be the set of required HUB units, and E connect courses to the units they fullfil.  A solution is any subset of U that collectively neighbors all of V.

### A Solution

Unfortunately this description is of an NP-complete problem, as it is mutually reducable to ordinary set coverage.  And even though we may be able to narrow down BUs thousands of courses to a couple hundred, it's still intractible to solve exhaustively—or guarantee the most optimal solution.

Thankfully however, we don't necessarily need to guarantee *most* optimal course-selection, just a good enough one for a recommendation, and there's a nice little greedy algorithm for finding sets that are pretty close if not indeed correct on occasion.

The reduction to make use of this algorithm is simply rewriting the courses as sets of the HUB units they provide and remembering to look up the indexes of the chosen classes at the end.

### Commentary

Often, there is more than one most optimal solution, and we can run the algorithm again over a differently ordering of the catalog to see the others.  Alternatively if the algorithm fails to find a good-enough sloution on the sorted list, where easiest classes would get considered first, we can rerun it nondeterministically on randomly shuffled inputs until it either halts with a great schedule, or our patience runs out.  It can take as many as 400+ tries sometimes on the default set with strict requirements, so don't always expect a loop.