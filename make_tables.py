
import yaml
import io


def escape_tex(string):
    replacements = {"#": "\#",
                    "^2": "$^2$",
                    "_": "\_",
                    "<": "$<$",
                    "%": "\%",
                    "&": "\&"}
    output = string
    for k, v in replacements.items():
        output = output.replace(k, v)
    return output


def split_ucd(string):
    # This enables line breaks between UCDs, and if necessary, inside of a
    # UCD at a period. The latter is not very desirable but was the only way
    # to make certain long UCDs fit in the column.
    return string.replace(";", "; ").replace(".", ".\\linebreak[0]")


def make_table_tex(table):

    output = io.StringIO()

    print("\\subsection{{{:s}}}".format(escape_tex(table['name'])), file=output)
    print("", file=output)
    print(escape_tex(table.get("description", "")), file=output)
    print("", file=output)

    print("\\begin{longtable}{p{1.3in}lp{1in}p{3.3in}}", file=output)
    print("\\hline\\hline", file=output)
    print("\\rowcolor{white}", file=output)
    print("Column Name & Data type & UCD & Description \\\\", file=output)
    print("\\hline\\hline\\endhead", file=output)
    print("\\hline\\hline\\endfoot", file=output)
    for column in table['columns']:
        if len(column["name"]) > 18:
            format_string = "\multicolumn{{3}}{{l}}{{{:s}}} & \skipcoloring \\\\ \n"
            format_string += " & {:s} & {:s} & {:s} \\\\"
        else:
            format_string = "{:s} & {:s} & {:s} & {:s}\\\\"
        print(format_string.format(escape_tex(column["name"]),
                                   column["datatype"],
                                   split_ucd(column.get("ivoa:ucd", "")),
                                   escape_tex(column.get("description", ""))),
              file=output)
    print("\\end{longtable}", file=output)
    print("", file=output)
    print("", file=output)
    return output


if __name__ == "__main__":

    output_filename = "core_tables.tex"

    yaml_filename = "cat/yml/baselineSchema.yaml"
    with open(yaml_filename) as f:
        yaml_contents = yaml.load(f)

    output_file = open(output_filename, "w")
    for table in yaml_contents['tables']:
        tex_output = make_table_tex(table)
        output_file.write(tex_output.getvalue())

    output_file.close()
