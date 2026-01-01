# simulator/management/commands/create_sample_data.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from simulator.models import Participant, Simulation, Dialogue, DialogueLine

User = get_user_model()


class Command(BaseCommand):
    help = "Create sample data for testing"

    def handle(self, *args, **kwargs):
        # Get or create user
        user, created = User.objects.get_or_create(
            email="test@example.com",
            defaults={"first_name": "Test", "last_name": "User"},
        )
        if created:
            user.set_password("password123")
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created user: {user.email}"))

        # Create participants
        marie = Participant.objects.create(
            user=user, speaker_name="Marie", is_system=False
        )

        serveur = Participant.objects.create(
            user=user, speaker_name="Serveur", is_system=True
        )

        self.stdout.write(self.style.SUCCESS("Created participants"))

        # Create simulation
        simulation = Simulation.objects.create(title="Au Restaurant")

        # Create dialogue
        dialogue = Dialogue.objects.create(
            simulation=simulation,
            title="Commander au restaurant",
            description="Une conversation simple pour commander un repas",
            difficulty_level="beginner",
            order=1,
        )

        dialogue.participants.add(marie, serveur)

        # Create dialogue lines
        lines_data = [
            (serveur, 1, "Bonjour! Bienvenue au restaurant. Vous avez réservé?"),
            (marie, 2, "Bonjour! Oui, une table pour deux personnes au nom de Marie."),
            (serveur, 3, "Parfait! Suivez-moi, s'il vous plaît. Voici votre table."),
            (marie, 4, "Merci beaucoup. Pouvez-vous me donner le menu?"),
            (
                serveur,
                5,
                "Bien sûr! Voici la carte. Je reviens dans quelques minutes pour prendre votre commande.",
            ),
            (marie, 6, "D'accord, merci!"),
        ]

        for participant, order, text in lines_data:
            DialogueLine.objects.create(
                dialogue=dialogue, participant=participant, order=order, text=text
            )

        simulation.current_dialogue = dialogue
        simulation.save()

        self.stdout.write(self.style.SUCCESS(f"Created simulation: {simulation.title}"))
        self.stdout.write(
            self.style.SUCCESS(f"Created dialogue with {len(lines_data)} lines")
        )
        self.stdout.write(self.style.SUCCESS("Sample data created successfully!"))
