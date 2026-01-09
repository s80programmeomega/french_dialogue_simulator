# simulator/urls.py

from django.urls import path
from . import views

app_name = "simulator"

urlpatterns = [
    path("", views.home, name="home"),
    # Simulations
    path("simulations/", views.simulation_list, name="simulation_list"),
    path("simulations/create/", views.simulation_create, name="simulation_create"),
    path("simulations/<int:pk>/", views.simulation_detail, name="simulation_detail"),
    path("simulations/<int:pk>/run/", views.simulation_run, name="simulation_run"),
    path(
        "simulations/<int:pk>/next/",
        views.next_dialogue,
        name="next_dialogue",
    ),
    path(
        "simulations/<int:pk>/complete/",
        views.complete_simulation,
        name="simulation_complete",
    ),
    # Participants
    path("participants/", views.participant_list, name="participant_list"),
    path("participants/create/", views.participant_create, name="participant_create"),
    path(
        "participants/<int:pk>/delete/",
        views.participant_delete,
        name="participant_delete",
    ),
    # Dialogues
    path(
        "simulations/<int:simulation_pk>/dialogue/create/",
        views.dialogue_create,
        name="dialogue_create",
    ),
    path("dialogue/<int:pk>/edit/", views.dialogue_edit, name="dialogue_edit"),
    path(
        "dialogue/<int:pk>/add-participant/",
        views.dialogue_add_participant,
        name="dialogue_add_participant",
    ),
    # Lines
    path(
        "dialogue/<int:dialogue_pk>/line/create/", views.line_create, name="line_create"
    ),
    path("line/<int:pk>/delete/", views.line_delete, name="line_delete"),
    # API
    path("api/line/<int:line_id>/record/", views.record_line, name="record_line"),
    path(
        "api/line/<int:line_id>/generate/",
        views.generate_system_audio,
        name="generate_system_audio",
    ),
    path(
        "api/dialogue/<int:dialogue_id>/generate-complete/",
        views.generate_complete_dialogue_audio,
        name="generate_complete_dialogue_audio",
    ),
    path(
        "api/simulation/<int:pk>/generate-audio/",
        views.generate_simulation_audio_view,
        name="generate_simulation_audio",
    ),
    path(
        "dialogue/<int:pk>/participant/create/",
        views.participant_create_inline,
        name="participant_create_inline",
    ),
]
