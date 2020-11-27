# BU HUB greedy algorithm
A greedy approach to the BU HUB requirements

> "The BU Hub is Boston University’s University-wide general education program that emphasizes working across disciplines to prepare for a complex and diverse world. Students can explore a variety of courses and innovative learning experiences while developing six essential capacities and fulfilling Hub requirements. Explore these six capacities, Hub learning outcomes, and how the Hub works below."
-https://www.bu.edu/hub/hub-courses/

```
├── README.md
├── catalog
│   ├── catalog.json  (full catalog scraped from the BU course catalog)
│   └── catalog_sorted.json  (all HUB courses as of fall 2020 - 100-level and up)
│
├── search.js  (catalog in JavaScript for easy map/reduce/filter-ing)
│
└── set_cover.py (the actual algorithm)
```

BU students know how annoying the HUB is, and how confusing it is to ensure they aren't forgetting any requirements, as even one overlooked unit necessitates a whole extra 4 credit class.

### The Problem

One way to formulate the BU HUB course selection problem is as a graph problem.  Given a graph G={U,V,E}, let U be the available courses, V be the set of required HUB units, and E connect courses to the units they fulfill.  A solution is any subset of U that collectively neighbors all of V.

### A Solution

Unfortunately this description is of an NP-complete problem, as it is mutually reducible to ordinary set coverage.  And even though we may be able to narrow down BUs thousands of courses to a couple hundred, it's still intractable to solve exhaustively—or guarantee the most optimal solution.

Thankfully however, we don't necessarily need to guarantee *most* optimal course-selection, just a good enough one for a recommendation, and there's a nice little greedy algorithm for finding sets that are pretty close if not indeed correct on occasion.

The reduction to make use of this algorithm is simply rewriting the courses as sets of the HUB units they provide and remembering to look up the indexes of the chosen classes at the end.

### Probabilistic Techniques

Often, there is more than one most optimal solution, and we can run the algorithm again over a differently ordering of the catalog to see the others.  Alternatively if the algorithm fails to find a good-enough solution on the sorted list, where the easiest classes would get considered first, we can rerun it nondeterministically on randomly shuffled inputs until it either halts with a great schedule, or our patience runs out.  It can take as many as 400+ tries sometimes on the default set with strict requirements, so don't always expect a loop.

### Notes about the included data set

Social Inquiry and Scientific Inquiry are not both required—only one of them.  Thankfully this is easily fixable with a quick preprocessing step, which combines the two into a "Social/Scientific Inquiry II" as a single unit.  Managing doubled requirements, however, does not have such a simple reduction, and I took the naive (but not unbearably inefficient) approach of rerunning the algorithm until it finds a selection with the desired multiplicity of HUB units (for example "Writing-Intensive Course" is needed twice).

```json
Number of courses offering each unit
------------------------------------
   5 First-Year Writing Seminar
  11 Writing, Research, and Inquiry
  65 Scientific Inquiry II
  73 Quantitative Reasoning I
  77 Scientific Inquiry I
  82 Quantitative Reasoning II
  84 Philosophical Inquiry and Life's Meanings
  97 Digital/Multimedia Expression
 110 Social Inquiry II
 132 Creativity/Innovation
 134 Social Inquiry I
 146 Ethical Reasoning
 158 Oral and/or Signed Communication
 167 Teamwork/Collaboration
 183 Writing-Intensive Course
 209 The Individual in Community
 223 Research and Information Literacy
 273 Historical Consciousness
 286 Aesthetic Exploration
 296 Global Citizenship and Intercultural Literacy
 320 Critical Thinking
```

### Usage

Run [`set_cover.py`](https://github.com/wyatt-howe/BU-HUB-greedy-algorithm/blob/master/set_cover.py#L81-L114) in your favorite python interpreter.  You will want to edit the file and fill in which HUB units are already completed.

<!-- ```sh
python set_cover.py catalog.json
``` -->
