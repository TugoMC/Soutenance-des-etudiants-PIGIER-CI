from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand

class Command(BaseCommand):
    help = 'Crée un super utilisateur sans exiger d\'adresse email'

    def add_arguments(self, parser):
        parser.add_argument('--username', dest='username', required=True, help='Nom d\'utilisateur du super utilisateur')
        parser.add_argument('--password', dest='password', required=True, help='Mot de passe du super utilisateur')

    def handle(self, *args, **options):
        options.setdefault('database', None)  # Ajoutez cette ligne pour éviter l'erreur de clé manquante
        options.setdefault('email', None)     # Vous pouvez également définir d'autres options par défaut si nécessaire

        username = options['username']
        password = options['password']
        
        # Créer le super utilisateur sans adresse email
        self.UserModel._default_manager.db_manager(options['database']).create_superuser(username=username, password=password)

        # Affiche un message de succès
        self.stdout.write(self.style.SUCCESS(f'Super utilisateur "{username}" créé avec succès.'))

