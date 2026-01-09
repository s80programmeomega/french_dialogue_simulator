from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Participant(models.Model):
    """A speaker/character that can be reused across dialogues."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="participants"
    )
    speaker_name = models.CharField(
        max_length=100, help_text="Character name (e.g., 'Marie', 'Waiter')"
    )
    is_system = models.BooleanField(
        default=False, help_text="System auto-generates TTS"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["user", "speaker_name"]

    def __str__(self):
        return f"{self.speaker_name} ({self.user.email})"


class Simulation(models.Model):
    """Practice session with multiple dialogues."""

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    current_dialogue = models.ForeignKey(
        "Dialogue",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="active_simulations",
    )
    current_line = models.PositiveIntegerField(default=1)
    final_audio = models.FileField(
        upload_to="simulations/final/", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.status})"


class Dialogue(models.Model):
    """Conversation template."""

    DIFFICULTY_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    simulation = models.ForeignKey(
        Simulation, on_delete=models.CASCADE, related_name="dialogues"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    difficulty_level = models.CharField(
        max_length=20, choices=DIFFICULTY_CHOICES, default="beginner"
    )
    participants = models.ManyToManyField(Participant, related_name="dialogues")
    order = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], help_text="Order in simulation"
    )
    complete_audio = models.FileField(
        upload_to="dialogues/complete/", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["simulation", "order"]
        unique_together = ["simulation", "order"]

    def __str__(self):
        return self.title
    
    def generate_complete_audio(self):
        """Generate complete dialogue audio by concatenating line recordings"""
        from .utils import concatenate_dialogue_audio
        
        audio_path = concatenate_dialogue_audio(self)
        if audio_path:
            self.complete_audio = audio_path
            self.save()
            return True
        return False


class DialogueLine(models.Model):
    """Individual speech line."""

    dialogue = models.ForeignKey(
        Dialogue, on_delete=models.CASCADE, related_name="lines"
    )
    participant = models.ForeignKey(
        Participant, on_delete=models.CASCADE, related_name="lines"
    )
    order = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    text = models.TextField()

    class Meta:
        ordering = ["dialogue", "order"]
        unique_together = ["dialogue", "order"]

    def __str__(self):
        return f"{self.dialogue.title} - Line {self.order}"


class LineRecording(models.Model):
    """Audio recording for a dialogue line (one-to-one)."""

    dialogue_line = models.OneToOneField(
        DialogueLine,
        on_delete=models.CASCADE,
        related_name="recording",
        primary_key=True,
    )
    audio_file = models.FileField(upload_to="simulations/lines/")
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recording: {self.dialogue_line}"
