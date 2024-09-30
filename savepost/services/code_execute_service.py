import subprocess

def execute_code(code: str) -> dict:
    '''Выполняет код переданный в строке и возвращаем stdout и stderr'''
        # удаляем лишние переносы строк
    code = code.strip()
    code_without_unnecessary_line_breaks = ''
    for line in code.split('\n'): 
        code_without_unnecessary_line_breaks += line.strip('\n') + '\n' 

    # выполняем код
    executor = subprocess.run(
        ['python', '-c', code_without_unnecessary_line_breaks],
        capture_output=True,
        text=True
    )
    return {'stdout': executor.stdout, 'stderr': executor.stderr}

