import pytest
import tempfile
import json
import os
import math

# from movies.tasks import split_file_task
from movies.tasks import split_json_file
from movies.tasks import split_csv_file
from movies.tasks import process_file

# def test_create_file(name: str = "", extension: str = ""):

#     # with open("test.json","x+t") as f:
#     #     f.write("[")
#     #     abc = {"name": "name"}
#     #     for _ in range(0, 65535):
#     #         f.write(json.dumps(abc) + ",\n")
#     #     f.write(json.dumps(abc) + "]\n")
#     #     print(os.path.getsize(f.name))
#     res = split_file_task("all_movies_data.json", file_type="application/json")
#     # res = split_file_task("all_movies_data.csv", file_type="text/csv")
#     print(len(res))
#     # file = tempfile.NamedTemporaryFile(mode="w+t", encoding="utf-8")


# def test_json_splitting():
#     split_size_mb = 1
#     bytes_in_mb = 1024 * 1024
#     split_amount = math.ceil(os.path.getsize("all_movies_data.json") / bytes_in_mb)
#     res = split_csv_file("all_movies_data.json",split_size_mb)

# def test_csv_splitting():
#     split_size_mb = 1
#     bytes_in_mb = 1024 * 1024
#     split_amount = math.ceil(os.path.getsize("all_movies_data.csv") / bytes_in_mb)
#     res = split_csv_file("all_movies_data.csv", split_size_mb)
#     assert split_amount == len(res)


def test_proccess_file():
    split_size_mb = 1
    bytes_in_mb = 1024 * 1024
    split_amount = math.ceil(os.path.getsize("all_movies_data.csv") / bytes_in_mb)
    # print(os.getcwd())
    res = process_file("all_movies_data.csv", "text/csv").get(timeout=10)
    # print(res)
    assert split_amount == len(res[1])


# def test_split_file_json
# file.write("[")
# for _ in range(0, 65535):
#     file.write(json.dumps(abc) + ",\n")
# file.write(json.dumps(abc) + "]\n")
# # file.write("]")
# # file.name = file.name + ".json"
# # print(file.name)
# file.seek(0)
# res = split_file_task(file.name,file_type="application/json")
# print(len(res))
# print(file.read())
# print(len(json.dumps(abc).encode()))
# print(os.path.getsize(file.name))
# with open(file.name, "r") as f:
#     kapa = json.load(f)
#     # print(kapa)
#     # # print(f)
#     # for row in kapa:
#     #     obj = json.dumps(row)
#     #     print(obj)
#     #     print(row)


# create_file()
