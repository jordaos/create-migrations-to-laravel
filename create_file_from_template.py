from datetime import datetime
import time

file_count = 0

def create_insert_file(filename, mapper):
  # time.sleep(1)
  global file_count
  now = datetime.now()

  now_str = now.strftime("%Y_%m_%d_%H%M")
  now_str = now_str + str(file_count).zfill(2)
  file_count += 1

  with open("templates/insert.php") as f:
    lines = f.readlines()

    output_filename = 'database/' + now_str + '_insert_' + filename + '.php'

    with open(output_filename, "w") as f1:
      for line in lines:
        line_result = line

        for key, value in mapper.items():
          line_result = line_result.replace(key, value)

        f1.write(line_result)

def create_table_file(table_name, mapper):
  # time.sleep(1)
  global file_count
  now = datetime.now()

  now_str = now.strftime("%Y_%m_%d_%H%M")
  now_str = now_str + str(file_count).zfill(2)
  file_count += 1

  with open("templates/create_table.php") as f:
    lines = f.readlines()

    output_filename = 'database/' + now_str + '_create_' + table_name + '_table.php'

    with open(output_filename, "w") as f1:
      for line in lines:
        line_result = line

        for key, value in mapper.items():
          line_result = line_result.replace(key, value)

        f1.write(line_result)

def create_model_file(model_name, mapper):
  with open("templates/model.php") as f:
    lines = f.readlines()

    output_filename = 'Models/' + model_name + '.php'

    with open(output_filename, "w") as f1:
      for line in lines:
        line_result = line

        for key, value in mapper.items():
          line_result = line_result.replace(key, value)

        f1.write(line_result)

def create_insert_column_structure_file(filename, mapper):
  # time.sleep(1)
  global file_count
  now = datetime.now()

  now_str = now.strftime("%Y_%m_%d_%H%M")
  now_str = now_str + str(file_count).zfill(2)
  file_count += 1

  with open("templates/insert_column_structure.php") as f:
    lines = f.readlines()

    output_filename = 'database/' + now_str + '_insert_' + filename + '.php'

    with open(output_filename, "w") as f1:
      for line in lines:
        line_result = line

        for key, value in mapper.items():
          line_result = line_result.replace(key, value)

        f1.write(line_result)