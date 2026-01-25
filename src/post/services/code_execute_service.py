import aiodocker

async def execute_code(code: str) -> dict:
    '''Выполняет код переданный в строке и возвращаем stdout и stderr'''
    docker = aiodocker.Docker(url='unix:///var/run/docker.sock')
    try:
        container = await docker.containers.create_or_replace(
            name='user_code_executor',
            config={
                'Image': 'python:3.14.2-slim',
                'Cmd': ['python', '-c', code],
                'HostConfig': {
                    'AutoRemove': False,
                    'Memory': 50 * 1024 * 1024,  # Ограничение памяти до 50MB
                    'NetworkMode': 'none'  # Отключение сети для безопасности
                }
            }
        )
        await container.start()
        exit_code = await container.wait()
        logs = await container.log(stdout=True, stderr=True)
        stdout = ''.join([line for line in logs if not line.startswith('stderr:')])
        stderr = ''.join([line[7:] for line in logs if line.startswith('stderr:')])
        return {
            'exit_code': exit_code.get('StatusCode', -1),
            'stdout': stdout,
            'stderr': stderr
        }
    finally:
        await container.delete(force=True)
        await docker.close()


