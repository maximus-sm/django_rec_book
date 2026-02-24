import json

from celery import shared_task, group, chain

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError

from movies.services import FileProcessor


# @shared_task
# def process_file(filename: str, file_type: str) -> int:
#     processor = FileProcessor()
#     return processor.process(filename, file_type)


@shared_task
def process_file(file_name: str, file_type: str) -> int:
    """Orchestrates the splitting and parallel processing of file chunks."""
    if not default_storage.exists(file_name):
        raise ValidationError("File does not exist in storage.")
    # Chain split_file_task with the processing of chunks
    workflow = chain(
        split_file_task.s(file_name, file_type),  # Splits the file
        process_chunks.s(file_type),  # Processes all chunks
    )
    result = workflow.apply_async()
    return result


@shared_task
def split_file_task(file_name: str, file_type: str) -> list[str]:
    if file_type == "text/csv":
        result = split_csv_file(file_name)
    elif file_type == "application/json":
        result = split_json_file(file_name)
    else:
        raise ValidationError("Invalid file type")
    return result


def split_csv_file(file_path: str, chunk_size_mb: int = 30) -> list[str]:
    chunk_paths = []
    part = 1
    current_chunk_size = 0
    chunk_lines = []
    row_names = ""
    # Note that "rb" , which returns file in byte format.
    # The data should be saved in bytes not in str.
    # When the server(Minio) recieves the file it checks 
    # the Content-Length header value of the request.It 
    # must be the amount of bytes of the data(file).
    # But when you save ContentFile with str data, 
    # somewhere in the code when len gets evalueted for the request, it just
    # returns amount of chars in the str not the actual bytes of the chars.
    with default_storage.open(file_path, "rb") as file:
        for line in file:
            if not row_names:
                row_names = line
            line_size = len(line)
            if current_chunk_size + line_size > chunk_size_mb * 1024 * 1024:
                chunk_file_name = f"{file_path}_part_{part}.csv"
                new_file = ContentFile(b"".join(chunk_lines))
                default_storage.save(chunk_file_name, new_file)
                chunk_paths.append(chunk_file_name)
                chunk_lines = [row_names, line]
                current_chunk_size = line_size
            else:
                chunk_lines.append(line)
                current_chunk_size += line_size
        if len(chunk_lines) > 0:  # Save the last chunk if there is any
            chunk_file_name = f"{file_path}_part_{part}.csv"
            new_file = ContentFile(b"".join(chunk_lines))
            default_storage.save(chunk_file_name, new_file)
            chunk_paths.append(chunk_file_name)
        return chunk_paths


def split_json_file(file_path: str, chunk_size_mb: int = 30) -> list[str]:
    chunk_paths = []
    part = 1
    current_chunk_size = 0
    chunk_objects = []
    with default_storage.open(file_path, "r") as file:
        objects = json.load(file)
        for obj in objects:
            obj_str = json.dumps(obj)
            obj_size = len(obj_str.encode("utf-8"))
            if current_chunk_size + obj_size > chunk_size_mb * 1024 * 1024:
                chunk_file_name = f"{file_path}_part_{part}.json"
                default_storage.save(
                    chunk_file_name, ContentFile(json.dumps(chunk_objects).encode())
                )
                chunk_paths.append(chunk_file_name)
                chunk_objects = [obj]
                current_chunk_size = obj_size
                part += 1
            else:
                chunk_objects.append(obj)
                current_chunk_size += obj_size
        if chunk_objects:  # Save the last chunk if there is any
            chunk_file_name = f"{file_path}_part_{part}.json"
            default_storage.save(
                chunk_file_name, ContentFile(json.dumps(chunk_objects).encode())
            )
            chunk_paths.append(chunk_file_name)
    return chunk_paths


@shared_task
def process_chunks(chunk_paths: list, file_type: str) -> int:
    """Task to handle processing of each chunk. This is called after the file has been split."""
    # Create a group of tasks to process each chunk
    task_group = group(
        process_chunk.s(chunk_path, file_type) for chunk_path in chunk_paths
    )
    return (
        task_group.apply_async()
    )  # Apply group asynchronously and return the AsyncResult of the group


@shared_task
def process_chunk(chunk_path: str, file_type: str) -> int:
    """Processes a single file chunk."""
    processor = FileProcessor()
    return processor.process(chunk_path, file_type)
    with default_storage.open(chunk_path, "r") as file:
        if file_type == "text/csv":
            result = parse_csv(file)
        elif file_type == "application/json":
            result = parse_json(file)
        else:
            raise ValidationError("Invalid file type")
    return result
