import subprocess


def execute_code(code: str) -> dict:
    '''Выполняет код переданный в строке и возвращаем stdout и stderr'''
    executor = subprocess.run(
        ['python', '-c', code],
        capture_output=True,
        text=True
    )
    return {'stdout': executor.stdout, 'stderr': executor.stderr}

