import unidecode
from nltk.corpus import stopwords
import re

from create_file_from_template import create_insert_file, create_table_file, create_model_file, create_insert_column_structure_file

sw = stopwords.words('portuguese')

def create_camel_case(text, low_first_letter = True):
  text = unidecode.unidecode(text)
  text = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", text)
  text = text.replace("()", "")
  text = text.replace("-", " ")
  text = ''.join([k.capitalize() for k in text.split(" ") if k not in sw])

  if low_first_letter:
    camelCase = text[0].lower() + text[1:]
  else:
    camelCase = text[0].upper() + text[1:]
  return camelCase

def get_model_name(line):
  result = line.replace("NOME DA TABELA:", "")
  model_name = result.strip()
  model_name = create_camel_case(model_name, False)
  model_name = 'Data' + model_name
  return model_name

def get_normalized_string(line, replace = ""):
  result = line.replace(replace, "")
  result = result.strip()
  result = re.sub(' +', ' ', result)
  return result

def camel_case_to_snake_case(text):
  return re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()

def create_table_structure_insertion(name, model_name, example_filename, table_frequency, document_type):
  class_name = model_name + 'InTableStructures'
  filename = camel_case_to_snake_case(class_name)
  table_name_snake = camel_case_to_snake_case(model_name)

  insert_fields = '''
            'name' => '%s',
            'table_name' => '%s',
            'file_example' => '%s',
            'frequency' => '%s',
            'document_type' => '%s',
  ''' % (name, table_name_snake, example_filename, table_frequency, document_type)

  mapper = {}
  mapper['[CLASSNAME]'] = class_name
  mapper['[ENTITY]'] = 'TableStructure'
  mapper['[INSERT_FIELDS]'] = insert_fields

  create_insert_file(filename, mapper)

def create_new_entity_table(model_name, columns):
  table_name = camel_case_to_snake_case(model_name)

  insert_column_structure_class_name = model_name + 'InTableStructuresColumns'
  insert_column_structure_filename = camel_case_to_snake_case(insert_column_structure_class_name)

  fields = ''
  model_fields = ''
  insert_column_structure_insert_creates = ''
  for item in columns:
    fields += "            $table->string('%s');\n" % (item[1])
    model_fields += "        '%s',\n" % (item[1])
    insert_column_structure_insert_creates += '''
        TableStructureColumn::create([
          'table_structure_id' => $tableStructure->id,
          'name' => '%s',
          'description' => '%s',
          'order' => %d,
        ]);
    ''' % (item[1], item[2], int(item[0]))

  mapper = {}
  mapper['[TABLE_NAME_CAMEL]'] = model_name
  mapper['[TABLE_NAME_SNAKE]'] = table_name
  mapper['[FIELDS]'] = fields

  model_mapper = {}
  model_mapper['[MODEL_NAME]'] = model_name
  model_mapper['[FIELDS]'] = model_fields

  insert_column_structure_mapper = {}
  insert_column_structure_mapper['[CLASSNAME]'] = insert_column_structure_class_name
  insert_column_structure_mapper['[TABLE_NAME]'] = table_name
  insert_column_structure_mapper['[ENTITY]'] = 'TableStructureColumn'
  insert_column_structure_mapper['[CREATES]'] = insert_column_structure_insert_creates

  create_table_file(table_name, mapper)
  create_model_file(model_name, model_mapper)
  create_insert_column_structure_file(insert_column_structure_filename, insert_column_structure_mapper)

with open("input.txt") as input_file:
  input_file_lines = input_file.readlines()

  name = ""
  model_name = ""
  example_filename = ""
  table_frequency = ""
  document_type = ""

  last_line_was_number = False
  columns = []

  for line in input_file_lines:
    if ("NOME DA TABELA" in line):
      name = get_normalized_string(line, "NOME DA TABELA:")
      model_name = get_model_name(line)
      columns = []
    if ("NOME DO ARQUIVO" in line):
      example_filename = get_normalized_string(line, "NOME DO ARQUIVO:")
    if ("FREQUÊNCIA DE ENVIO" in line):
      table_frequency = get_normalized_string(line, "FREQUÊNCIA DE ENVIO:")
    if ("TIPO DE DOCUMENTO" in line):
      document_type = get_normalized_string(line, "TIPO DE DOCUMENTO:")
      create_table_structure_insertion(name, model_name, example_filename, table_frequency, document_type)

    if line[0].isdigit():
      normalized_line = get_normalized_string(line)
      description = get_normalized_string(normalized_line.split(".")[1])

      camelCaseLine = create_camel_case(normalized_line)
      camelCaseLineSplit = camelCaseLine.split(".")
      lineNumber = camelCaseLineSplit[0]
      variableName = camel_case_to_snake_case(camelCaseLineSplit[1])
      columns.append((lineNumber, variableName, description))
      last_line_was_number = True

    if last_line_was_number and not line[0].isdigit():
      create_new_entity_table(model_name, columns)

    if not line[0].isdigit():
      last_line_was_number = False
