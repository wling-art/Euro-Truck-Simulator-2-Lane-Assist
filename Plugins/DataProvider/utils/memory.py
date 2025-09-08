import psutil


def read_memory_usage() -> float:
    """
    Reads the current memory usage of the process in megabytes.

    Returns:
        float: Memory usage in MB.
    """
    process = psutil.Process()
    memory_info = process.memory_info()
    return memory_info.rss / (1024 * 1024)  # Convert bytes to MB
