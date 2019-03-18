
import yaml
import io


def escape_tex(string):
    """
    Escape or replace strings that LaTeX will misinterpret.
    """
    replacements = {"#": "\#",
                    "^2": "$^2$",
                    "^4": "$^4$",
                    "_": "\_",
                    "<": "$<$",
                    "%": "\%",
                    "&": "\&"}
    output = string
    for k, v in replacements.items():
        output = output.replace(k, v)
    return output


def split_ucd(string):
    """
    Add spacing and line break hints to UCD fields.

    This enables line breaks between UCDs, and if necessary, inside of a UCD
    at a period. The latter is not very desirable but was the only way to
    make certain long UCDs fit in the column.
    """
    # .replace(".", ".\\linebreak[0]")
    return string.replace(";", "; ")


def make_table_tex(table, column_list_output=None):
    """
    Generate LaTeX output from an input table in YAML format. Returns a
    StringIO object.
    """

    output = io.StringIO()
    table_name = escape_tex(table['name'])

    print("\\subsection{{{:s}}}\n".format(table_name), file=output)
    print(escape_tex(table.get("description", "")), file=output)
    print("", file=output)

    print("\\begin{{schema}}{{{:s} Table}}{{{:s} Table}}{{}}".format(table_name, table_name),
          file=output)
    for column in table['columns']:
        # For columns with long names, we split the row into two separate rows,
        # with the column name on the top row and the rest of the record on the
        # second row. The skipcoloring command ensure that both rows receive
        # the same background color.
        if len(column["name"]) > 18:
            format_string = "\multicolumn{{3}}{{l}}{{{:s}}} & \skipcoloring \\\\ \n"
            format_string += " & {:s} & {:s} & {:s} \\\\"
        else:
            format_string = "{:s} & {:s} & {:s} & {:s}\\\\"

        if("ivoa:ucd" in column):
            ucd_string = " [{:s}]".format(split_ucd(column["ivoa:ucd"]))
        else:
            ucd_string = ""
        print(format_string.format(escape_tex(column["name"]),
                                   column["datatype"],
                                   escape_tex(column.get("fits:tunit", "")),
                                   escape_tex(column.get("description", "") + ucd_string)),
              file=output)
        if column_list_output is not None:
            print("{:s},{:s}".format(table['name'], column['name']), file=column_list_output)
    print("\\end{schema}\n\n", file=output)
    return output


if __name__ == "__main__":

    output_filename = "core_tables.tex"
    yaml_filename = "cat/yml/baselineSchema.yaml"

    with open(yaml_filename) as f:
        yaml_contents = yaml.load(f)

    output_file = open(output_filename, "w")

    # The column list output is optional and can be disabled
    # once the Yaml schema file is deemed authoritative.
    column_list_file = open("yaml_column_list.txt", "w")
    for table in yaml_contents['tables']:
        tex_output = make_table_tex(table, column_list_output=column_list_file)
        output_file.write(tex_output.getvalue())

    column_list_file.close()
    output_file.close()
