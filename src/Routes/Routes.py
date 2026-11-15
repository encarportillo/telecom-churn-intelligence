from pathlib import Path



ROOT_ROUTE = Path(__file__).parent.parent.parent

ROUTES = {
    'config': ROOT_ROUTE / 'config',
    'dashboard': ROOT_ROUTE / 'dashboard',
    'docker': ROOT_ROUTE / 'docker',
    'input': ROOT_ROUTE / 'input',
    'notebooks': ROOT_ROUTE / 'notebooks',
    'outputs': ROOT_ROUTE / 'outputs',
    'src': ROOT_ROUTE / 'src',
    'api': ROOT_ROUTE / 'src' / 'api',
    'etl': ROOT_ROUTE / 'src' / 'etl',
    'models': ROOT_ROUTE / 'src' / 'models',
    'tests': ROOT_ROUTE / 'tests',
}

