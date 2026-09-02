# Concurrent File Downloader Simulator

# This one is more advanced.

# Concepts covered:

# * Functions
# * Exception handling
# * *args
# * **kwargs
# * threading
# * concurrent.futures
# * Context managers
# * Timing
# * List/dictionary processing

# Challenge

# Create a program that simulates downloading multiple files.

# The system should:

# * Download multiple files.
# * Track successful/failed downloads.
# * Run downloads concurrently.
# * Measure total execution time.
# * Generate a summary.
# * Retry failed downloads.

import time
import random
from concurrent.futures import ThreadPoolExecutor


def download_file(filename, size, retry_count=2):
    attempt = 0

    while attempt <= retry_count:
        attempt += 1

        print(
            f"Downloading {filename} "
            f"(Attempt {attempt})..."
        )

        try:
            download_time = size / 10

            time.sleep(download_time)

            success = random.choice(
                [True, True, True, False]
            )

            if not success:
                raise ConnectionError(
                    "Network connection failed"
                )

            print(
                f"✓ {filename} downloaded successfully"
            )

            return {
                "filename": filename,
                "size": size,
                "status": "success",
                "attempts": attempt
            }

        except ConnectionError as error:

            print(
                f"✗ {filename} failed: {error}"
            )

            if attempt > retry_count:
                return {
                    "filename": filename,
                    "size": size,
                    "status": "failed",
                    "attempts": attempt
                }

            print(
                f"Retrying {filename}..."
            )


def download_all_files(files, max_workers=3):
    results = []

    start_time = time.time()

    with ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:

        futures = []

        for filename, size in files.items():
            future = executor.submit(
                download_file,
                filename,
                size
            )

            futures.append(future)

        for future in futures:
            try:
                result = future.result()
                results.append(result)

            except Exception as error:
                print(
                    "Unexpected error:",
                    error
                )

    end_time = time.time()

    total_time = end_time - start_time

    return results, total_time


def generate_report(results, total_time):

    successful = [
        result
        for result in results
        if result["status"] == "success"
    ]

    failed = [
        result
        for result in results
        if result["status"] == "failed"
    ]

    total_size = sum(
        result["size"]
        for result in successful
    )

    print("\n")
    print("=" * 55)
    print("DOWNLOAD REPORT")
    print("=" * 55)

    print(
        f"Total Files   : {len(results)}"
    )

    print(
        f"Successful    : {len(successful)}"
    )

    print(
        f"Failed        : {len(failed)}"
    )

    print(
        f"Downloaded    : {total_size} MB"
    )

    print(
        f"Total Time    : {total_time:.2f} seconds"
    )

    print("\nSuccessful Downloads:")

    for result in successful:
        print(
            f"✓ {result['filename']} | "
            f"{result['size']} MB | "
            f"Attempts: {result['attempts']}"
        )

    if failed:
        print("\nFailed Downloads:")

        for result in failed:
            print(
                f"✗ {result['filename']} | "
                f"Attempts: {result['attempts']}"
            )


files = {
    "python.pdf": 20,
    "machine_learning.pdf": 30,
    "data_analysis.csv": 10,
    "deep_learning.zip": 50,
    "dataset.zip": 40,
    "project.zip": 25
}


results, total_time = download_all_files(
    files,
    max_workers=3
)

generate_report(
    results,
    total_time
)