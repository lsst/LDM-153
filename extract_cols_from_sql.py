#!/usr/bin/env python

#
# This implements a very mediocre parsing of the baselineSchema.sql file, in
# order to extact a list of columns in each table.
#
# This is used to compare the schema defined in the cat package SQL files with
# the schema recorded in the LDM-153 LaTeX.
#

import re

if __name__ == '__main__':
    f = open("baselineSchema_8088853.sql")
    f_out = open("baselineSchema_columns.txt", "w")
    current_table = ""
    inside_parens = False
    for raw_line in f:
        line = raw_line.strip()

        if line.startswith('--'):
            continue

        if line.startswith("INSERT") or line.startswith("ALTER") \
           or line.startswith("PRIMARY") or line.startswith("INDEX") \
           or line.startswith("CONSTRAINT") or line.startswith("FOREIGN") \
           or line.startswith("REFERENCES") \
           or line.startswith("UNIQUE"):
            continue

        if "(" in line and not ")" in line:
            inside_parens = True
            continue

        if ")" in line and not "(" in line:
            inside_parens = False
            continue


        res = re.match("CREATE TABLE (\w+)", line)
        if res:
            current_table = res[1]
            continue

        if inside_parens:
            print("{:s},{:s}".format(current_table.strip(),  line.split(" ")[0]))

