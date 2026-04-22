import asyncio
import argparse
import logging
from pathlib import Path
import shutil
from concurrent.futures import ThreadPoolExecutor

# logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("file_sorter.log"),
        logging.StreamHandler()
    ]
)

# Thread pool (for blocking I/O)
executor = ThreadPoolExecutor(max_workers=10)


async def copy_file(file_path: Path, output_folder: Path):
    try:
        ext = file_path.suffix.lower().replace('.', '') or "no_extension"
        target_dir = output_folder / ext

        target_dir.mkdir(parents=True, exist_ok=True)

        target_file = target_dir / file_path.name

        await asyncio.get_running_loop().run_in_executor(
            executor, shutil.copy2, file_path, target_file
        )

        logging.info(f"Copied: {file_path} -> {target_file}")

    except Exception as e:
        logging.error(f"Error copying {file_path}: {e}")

async def read_folder(source_folder: Path, output_folder: Path):
    tasks = []

    try:
        for item in source_folder.iterdir():
            if item.is_dir():
                tasks.append(read_folder(item, output_folder))
            else:
                tasks.append(copy_file(item, output_folder))

        await asyncio.gather(*tasks)

    except Exception as e:
        logging.error(f"Error reading folder {source_folder}: {e}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Async file sorter by extension"
    )
    parser.add_argument(
        "source",
        type=str,
        help="Source folder path"
    )
    parser.add_argument(
        "output",
        type=str,
        help="Output folder path"
    )
    return parser.parse_args()


async def main():
    args = parse_args()

    source = Path(args.source)
    output = Path(args.output)

    if not source.exists() or not source.is_dir():
        logging.error("Source folder does not exist or is not a directory")
        return

    output.mkdir(parents=True, exist_ok=True)

    await read_folder(source, output)


if __name__ == "__main__":
    asyncio.run(main())