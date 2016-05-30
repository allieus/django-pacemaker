from os.path import dirname, exists, join
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.template import engines


class Command(BaseCommand):
    help = 'Create config file for Azure WebApp'

    def add_arguments(self, parser):
        parser.add_argument('azure_settings', type=str,
                help='Azure WebApp에서 쓰일 django settings module 의 경로를 지정해주세요.')

    def handle(self, *args, **options):
        self.stdout.write('Azure WebApp for Django by AskDjango')

        azure_settings = options['azure_settings']
        self.stdout.write('- DJANGO_SETTINGS_MODULE로서 {}를 적용해서, Azure WebApp 설정을 생성합니다.'.format(azure_settings))

        asset_path = join(dirname(dirname(dirname(__file__))), 'assets_azurewebapp')

        engine = engines['django']

        filenames = ['ptvs_virtualenv_proxy.py', '.deployment', 'deploy.py', 'deploy_settings.py', 'web.3.4.config']
        for filename in filenames:
            filepath = join(asset_path, filename)
            with open(filepath, 'r') as f:
                template_code = f.read()
                template = engine.from_string(template_code)
                content = template.render({
                    'DJANGO_SETTINGS_MODULE': azure_settings,
                })

                self.stdout.write('')
                self.stdout.write(filename)

                dst_path = join(settings.BASE_DIR, filename)
                if not exists(dst_path):
                    self.stdout.write('- 저장했습니다.'.format(filename))
                    open(dst_path, 'w').write(content)
                else:
                    answer = input('- 덮어쓰시겠습니까? (Y/n) : '.format(filename)).lower().strip()
                    if (not answer) or ('y' in answer):
                        self.stdout.write('- 저장했습니다.'.format(filename))
                        open(dst_path, 'w').write(content)
                    else:
                        self.stdout.write('- 무시했습니다.'.format(filename))

