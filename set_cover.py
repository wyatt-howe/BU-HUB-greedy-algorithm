import json
import random

CATALOG_PATH = 'catalog/catalog_sorted.json'

catalog_descriptions = json.load(open(CATALOG_PATH))

#
# Retrieve a course's full description from it's number, e.g. "CAS CH 182".
#

def lookup(num: str):
    return next(filter(lambda e : e['number'] == num, catalog_descriptions))

#
# Implementation of the greedy algorithm for set covering.
#

def set_cover_greedy(U):
    courses = U  # ordered set of unit sets each representing a course

    # Preprocess for the set sizes and unit lookups.
    units = {}  # All units mapping to a list of courses that have each unit.
    sizes = {}
    for course_num, course in enumerate(courses):
        l = len(course)
        if not l in sizes:
            sizes[l] = set()
        sizes[l].add(course_num)

        for unit in course:
            if not unit in units:
                units[unit] = []
            units[unit].append(course_num)

    # Find a satisfiable set of courses in linear time.
    solution = []
    for size in reversed(sorted(sizes.keys())[1:]):
        S = sizes[size]
        while len(S):
            candidate = S.pop()
            solution.append(candidate)
            for unit in courses[candidate]:
                for course_num in units[unit]:
                    if course_num != candidate:
                        course = courses[course_num]
                        l = len(course)
                        course.remove(unit)
                        sizes[l].remove(course_num)
                        sizes[l-1].add(course_num)
                del units[unit]
    return solution

#
# Remove the full course description and order as a set of sets.
# Courses are represented as a set of their HUB units.
#
def set_problem_reduction(G):
    return [set(v['units']) for v in G]

#
# Remove any BU HUB units that were already completed.
#

def filter_units(G, units):
    return filter_units([
        {'number': e['number'], 'units': list(filter( \
            lambda s : not s == units[0] \
        , e['units']))} for e in G
    ], units[1:]) if len(units) else G

#
# Only allow classes from a list of specific schools
#

def filter_schools(G, schools):
    return list(filter(lambda e : any(map(lambda school : school in e['number'], schools)), G))



"""
vvv  Modify the code below to get a recommendation  vvv
"""

# Load the catalog and remove unneeded units.  Example: I have already completed my philosophy unit.
catalog = json.load(open(CATALOG_PATH))
catalog = filter_units(catalog, [
    # 'Critical Thinking',
    # 'Ethical Reasoning',
    "Philosophical Inquiry and Life's Meanings",
    # 'Creativity/Innovation',
    # 'Global Citizenship and Intercultural Literacy',
    # 'Aesthetic Exploration',
    # 'Social Inquiry I',
    # 'Historical Consciousness',
    # 'Teamwork/Collaboration',
    # 'Quantitative Reasoning I',
    # 'Scientific Inquiry I',
    # 'The Individual in Community',
    # 'Quantitative Reasoning II',
    # 'Scientific Inquiry II',
    # 'Research and Information Literacy',
    # 'Social Inquiry II',
    # 'Digital/Multimedia Expression',
    # 'Oral and/or Signed Communication',
    # 'First-Year Writing Seminar',
    # 'Writing-Intensive Course',
    # 'Writing, Research, and Inquiry'
])  # Ignore all of these units.
catalog = filter_schools(catalog, ['CAS', 'CFA', 'CGS', 'ENG', 'KHC'])  # Accept classes from any of these schools.

# init mutables
courses = list(range(len(catalog)))
dump = ''

# Search for courses.  Example: No more than 8 courses; I require multiple of the same unit for writing and reasearch literacy.
while len(courses) > 8 or dump.count("Writing-Intensive Course") < 2 or dump.count("Research and Information Literacy") < 2:
    random.shuffle(catalog)  # Delete this to prioritize low level courses (100s first and up)

    # Invoke the set cover oracle
    courses_set = set_problem_reduction(catalog)
    courses = set_cover_greedy(courses_set)

    print(len(courses))

    dump = json.dumps([
        catalog[e] for e in courses
    ], indent=2, sort_keys=True)

    print(len(courses), dump.count("Writing-Intensive Course"), dump.count("Research and Information Literacy"))

# Write output to console in JSON format.
dump = json.dumps([
        lookup(catalog[e]['number']) for e in courses
    ], indent=2, sort_keys=True)
print(dump)
