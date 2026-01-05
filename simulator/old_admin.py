# simulator/admin.py

from django.contrib import admin
from .models import Participant, Simulation, Dialogue, DialogueLine, LineRecording


class DialogueLineInline(admin.TabularInline):
    model = DialogueLine
    extra = 1
    fields = ('order', 'participant', 'text')


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('speaker_name', 'user', 'is_system', 'created_at')
    list_filter = ('is_system', 'created_at')
    search_fields = ('speaker_name', 'user__email')


@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'current_dialogue', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'completed_at')


@admin.register(Dialogue)
class DialogueAdmin(admin.ModelAdmin):
    list_display = ('title', 'simulation', 'difficulty_level', 'order', 'created_at')
    list_filter = ('difficulty_level', 'created_at')
    search_fields = ('title', 'description')
    filter_horizontal = ('participants',)
    inlines = [DialogueLineInline]


@admin.register(DialogueLine)
class DialogueLineAdmin(admin.ModelAdmin):
    list_display = ('dialogue', 'order', 'participant', 'text_preview')
    list_filter = ('dialogue',)
    search_fields = ('text',)
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text'


@admin.register(LineRecording)
class LineRecordingAdmin(admin.ModelAdmin):
    list_display = ('dialogue_line', 'audio_file', 'recorded_at')
    readonly_fields = ('recorded_at',)
