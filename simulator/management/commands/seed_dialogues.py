"""
Django management command to seed the database with sample French dialogue data.

Usage:
    python manage.py seed_dialogues
    python manage.py seed_dialogues --clear  # Clear existing data first
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from simulator.models import Participant, Simulation, Dialogue, DialogueLine

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds the database with sample French dialogue simulations"

    def add_arguments(self, parser):
        """Add optional --clear flag to remove existing data."""
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing simulation data before seeding",
        )

    def handle(self, *args, **options):
        """Main seeder logic."""

        if options["clear"]:
            self.stdout.write("Clearing existing data...")
            DialogueLine.objects.all().delete()
            Dialogue.objects.all().delete()
            Simulation.objects.all().delete()
            Participant.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("✓ Data cleared"))

        # Get or create test user
        user, created = User.objects.get_or_create(
            email="test@example.com",
            defaults={"first_name": "Test", "last_name": "User"},
        )
        if created:
            user.set_password("testpass123")
            user.save()
            self.stdout.write(self.style.SUCCESS(f"✓ Created user: {user.email}"))

        # Create participants
        participants_data = [
            {"speaker_name": "Marie", "is_system": False},
            {"speaker_name": "Serveur", "is_system": True},
            {"speaker_name": "Jean", "is_system": True},
            {"speaker_name": "Vendeur", "is_system": True},
        ]

        participants = {}
        for p_data in participants_data:
            participant = Participant.objects.filter(
                user=user,
                speaker_name=p_data["speaker_name"]
            ).first()
            
            if not participant:
                participant = Participant.objects.create(
                    user=user,
                    speaker_name=p_data["speaker_name"],
                    is_system=p_data["is_system"]
                )
                self.stdout.write(f"✓ Created participant: {participant.speaker_name}")
            else:
                self.stdout.write(f"✓ Using existing participant: {participant.speaker_name}")
            
            participants[p_data["speaker_name"]] = participant

        # Create simulation
        simulation = Simulation.objects.create(
            title="French Conversation Practice - Beginner", status="pending"
        )
        self.stdout.write(
            self.style.SUCCESS(f"✓ Created simulation: {simulation.title}")
        )

        # Dialogue 1: Restaurant
        dialogue1 = Dialogue.objects.create(
            simulation=simulation,
            title="Au Restaurant",
            description="Ordering food at a French restaurant",
            difficulty_level="beginner",
            order=1,
        )
        dialogue1.participants.set([participants["Marie"], participants["Serveur"]])

        lines1 = [
            {
                "participant": "Serveur",
                "order": 1,
                "text": "Bonjour! Bienvenue au restaurant. Vous avez réservé?",
            },
            {
                "participant": "Marie",
                "order": 2,
                "text": "Oui, une table pour deux personnes au nom de Marie.",
            },
            {
                "participant": "Serveur",
                "order": 3,
                "text": "Parfait! Suivez-moi, s'il vous plaît.",
            },
            {"participant": "Marie", "order": 4, "text": "Merci beaucoup."},
            {
                "participant": "Serveur",
                "order": 5,
                "text": "Voici le menu. Que désirez-vous boire?",
            },
            {
                "participant": "Marie",
                "order": 6,
                "text": "Un verre d'eau, s'il vous plaît.",
            },
        ]

        for line_data in lines1:
            DialogueLine.objects.create(
                dialogue=dialogue1,
                participant=participants[line_data["participant"]],
                order=line_data["order"],
                text=line_data["text"],
            )
        self.stdout.write(
            f"✓ Created dialogue: {dialogue1.title} ({len(lines1)} lines)"
        )

        # Dialogue 2: Shopping
        dialogue2 = Dialogue.objects.create(
            simulation=simulation,
            title="Au Magasin",
            description="Shopping for clothes",
            difficulty_level="beginner",
            order=2,
        )
        dialogue2.participants.set([participants["Marie"], participants["Vendeur"]])

        lines2 = [
            {
                "participant": "Vendeur",
                "order": 1,
                "text": "Bonjour madame, je peux vous aider?",
            },
            {
                "participant": "Marie",
                "order": 2,
                "text": "Oui, je cherche une robe bleue.",
            },
            {
                "participant": "Vendeur",
                "order": 3,
                "text": "Quelle taille faites-vous?",
            },
            {"participant": "Marie", "order": 4, "text": "Je fais du 38."},
            {
                "participant": "Vendeur",
                "order": 5,
                "text": "Voici plusieurs modèles. La cabine est là-bas.",
            },
            {
                "participant": "Marie",
                "order": 6,
                "text": "Merci, je vais essayer celle-ci.",
            },
        ]

        for line_data in lines2:
            DialogueLine.objects.create(
                dialogue=dialogue2,
                participant=participants[line_data["participant"]],
                order=line_data["order"],
                text=line_data["text"],
            )
        self.stdout.write(
            f"✓ Created dialogue: {dialogue2.title} ({len(lines2)} lines)"
        )

        # Dialogue 3: Meeting someone
        dialogue3 = Dialogue.objects.create(
            simulation=simulation,
            title="Rencontre",
            description="Meeting someone for the first time",
            difficulty_level="beginner",
            order=3,
        )
        dialogue3.participants.set([participants["Marie"], participants["Jean"]])

        lines3 = [
            {
                "participant": "Jean",
                "order": 1,
                "text": "Bonjour! Comment tu t'appelles?",
            },
            {"participant": "Marie", "order": 2, "text": "Je m'appelle Marie. Et toi?"},
            {"participant": "Jean", "order": 3, "text": "Moi, c'est Jean. Enchanté!"},
            {
                "participant": "Marie",
                "order": 4,
                "text": "Enchantée! Tu habites à Paris?",
            },
            {
                "participant": "Jean",
                "order": 5,
                "text": "Oui, j'habite dans le 5ème arrondissement.",
            },
            {"participant": "Marie", "order": 6, "text": "Ah, c'est un beau quartier!"},
        ]

        for line_data in lines3:
            DialogueLine.objects.create(
                dialogue=dialogue3,
                participant=participants[line_data["participant"]],
                order=line_data["order"],
                text=line_data["text"],
            )
        self.stdout.write(
            f"✓ Created dialogue: {dialogue3.title} ({len(lines3)} lines)"
        )

        # Summary
        self.stdout.write(self.style.SUCCESS("\n" + "=" * 50))
        self.stdout.write(
            self.style.SUCCESS("Database seeding completed successfully!")
        )
        self.stdout.write(self.style.SUCCESS("=" * 50))
        self.stdout.write(f"Participants: {Participant.objects.count()}")
        self.stdout.write(f"Simulations: {Simulation.objects.count()}")
        self.stdout.write(f"Dialogues: {Dialogue.objects.count()}")
        self.stdout.write(f"Dialogue Lines: {DialogueLine.objects.count()}")
        self.stdout.write(self.style.SUCCESS("=" * 50))
