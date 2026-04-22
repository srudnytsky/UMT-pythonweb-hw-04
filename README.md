# UMT-pythonweb-hw-04

# Async File Sorter

## Overview

This project implements an asynchronous Python script that reads all files from a specified source directory and distributes them into subdirectories in a target (output) directory based on file extensions.

The solution is designed to efficiently handle large numbers of files using asynchronous execution combined with thread-based parallelism for file operations.

## Features

- Recursive traversal of all subdirectories in the source folder
- Sorting files into subfolders based on extension
- Asynchronous processing using `asyncio`
- Parallel file operations via `ThreadPoolExecutor`
- Command-line interface using `argparse`
- Logging of operations and errors
- Graceful handling of missing extensions and runtime errors

## Requirements

- Python 3.8 or higher

No external dependencies are required.

## Usage

Run the script from the command line:

`python app.py <source_folder> <output_folder>`

Example:

`python app.py ./data ./sorted`

## How It Works

1. The script parses command-line arguments to obtain source and output directories.
2. It recursively scans the source directory.
3. Each file is processed asynchronously:
   - Its extension is extracted.
   - A corresponding subdirectory is created in the output folder.
   - The file is copied into that subdirectory.
4. Blocking file operations are executed in a thread pool to avoid blocking the event loop.
5. All actions and errors are logged.

## Logging

Logs are written to:

`file_sorter.log`

Log levels:
- INFO: successful file operations
- ERROR: exceptions and failures

## Notes

- Files without extensions are placed into a folder named `no_extension`.
- Existing files with the same name in the destination directory may be overwritten.
- The script focuses on copying files, not moving them.