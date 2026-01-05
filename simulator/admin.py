from django.contrib import admin

from .models import Participant, Simulation, Dialogue, DialogueLine, LineRecording


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "speaker_name", "is_system", "created_at")
    list_filter = ("user", "is_system", "created_at")
    date_hierarchy = "created_at"


@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "status",
        "current_dialogue",
        "current_line",
        "final_audio",
        "created_at",
        "completed_at",
    )
    list_filter = ("current_dialogue", "created_at", "completed_at")
    date_hierarchy = "created_at"


@admin.register(Dialogue)
class DialogueAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "simulation",
        "title",
        "description",
        "difficulty_level",
        "order",
        "created_at",
    )
    list_filter = ("simulation", "created_at")
    raw_id_fields = ("participants",)
    date_hierarchy = "created_at"


@admin.register(DialogueLine)
class DialogueLineAdmin(admin.ModelAdmin):
    list_display = ("id", "dialogue", "participant", "order", "text")
    list_filter = ("dialogue", "participant")


@admin.register(LineRecording)
class LineRecordingAdmin(admin.ModelAdmin):
    list_display = ("dialogue_line", "audio_file", "recorded_at")
    list_filter = ("dialogue_line", "recorded_at")
