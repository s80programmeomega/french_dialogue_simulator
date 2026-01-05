# simulator/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.utils import timezone
import base64
import os
from .models import Simulation, Dialogue, Participant, DialogueLine, LineRecording
from .utils import text_to_speech


def home(request):
    stats = {
        "simulations": Simulation.objects.count(),
        "dialogues": Dialogue.objects.count(),
        "participants": Participant.objects.count(),
        "completed": Simulation.objects.filter(status="completed").count(),
    }

    recent_simulations = Simulation.objects.all()[:5]

    context = {
        "stats": stats,
        "recent_simulations": recent_simulations,
    }

    return render(request, "simulator/home.html", context)


def simulation_list(request):
    simulations = Simulation.objects.all()
    return render(
        request, "simulator/simulation_list.html", {"simulations": simulations}
    )


def simulation_detail(request, pk):
    simulation = get_object_or_404(Simulation, pk=pk)
    dialogues = simulation.dialogues.all()
    return render(
        request,
        "simulator/simulation_detail.html",
        {"simulation": simulation, "dialogues": dialogues},
    )


def simulation_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        simulation = Simulation.objects.create(title=title)
        messages.success(request, "Simulation créée avec succès!")
        return redirect("simulator:simulation_detail", pk=simulation.pk)

    return render(request, "simulator/simulation_form.html")


def simulation_run(request, pk):
    simulation = get_object_or_404(Simulation, pk=pk)

    if simulation.status == "pending":
        simulation.status = "in_progress"
        simulation.save()

    dialogues = simulation.dialogues.all()
    current_dialogue = simulation.current_dialogue or dialogues.first()
    
    if current_dialogue:
        if not simulation.current_dialogue:
            simulation.current_dialogue = current_dialogue
            simulation.save()
        lines = current_dialogue.lines.select_related("participant").all()
    else:
        lines = []

    return render(
        request,
        "simulator/simulation_run.html",
        {
            "simulation": simulation,
            "current_dialogue": current_dialogue,
            "dialogues": dialogues,
            "lines": lines,
        },
    )


@csrf_exempt
def record_line(request, line_id):
    if request.method == "POST":
        line = get_object_or_404(DialogueLine, pk=line_id)
        audio_data = request.POST.get("audio_data")

        if audio_data:
            format, audiostr = audio_data.split(";base64,")
            ext = format.split("/")[-1]
            audio_file = ContentFile(
                base64.b64decode(audiostr), name=f"line_{line_id}.{ext}"
            )

            recording, created = LineRecording.objects.update_or_create(
                dialogue_line=line, defaults={"audio_file": audio_file}
            )

            return JsonResponse(
                {"success": True, "audio_url": recording.audio_file.url}
            )

        return JsonResponse({"success": False, "error": "No audio data"})

    return JsonResponse({"success": False, "error": "Invalid method"})


def generate_system_audio(request, line_id):
    line = get_object_or_404(DialogueLine, pk=line_id)

    if not line.participant.is_system:
        return JsonResponse({"success": False, "error": "Not a system line"})

    try:
        recording = LineRecording.objects.get(dialogue_line=line)
        return JsonResponse({"success": True, "audio_url": recording.audio_file.url})
    except LineRecording.DoesNotExist:
        pass

    from django.conf import settings

    output_path = os.path.join(
        settings.MEDIA_ROOT, "simulations", "lines", f"system_{line_id}.mp3"
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    text_to_speech(line.text, output_path, lang="fr")

    recording = LineRecording.objects.create(
        dialogue_line=line, audio_file=f"simulations/lines/system_{line_id}.mp3"
    )

    return JsonResponse({"success": True, "audio_url": recording.audio_file.url})


def next_dialogue(request, pk):
    simulation = get_object_or_404(Simulation, pk=pk)
    dialogues = simulation.dialogues.all().order_by('order')
    
    if simulation.current_dialogue:
        current_order = simulation.current_dialogue.order
        next_dialogue = dialogues.filter(order__gt=current_order).first()
        
        if next_dialogue:
            simulation.current_dialogue = next_dialogue
            simulation.save()
            messages.success(request, f"Dialogue suivant: {next_dialogue.title}")
            return redirect("simulator:simulation_run", pk=pk)
    
    simulation.status = "completed"
    simulation.completed_at = timezone.now()
    simulation.save()
    messages.success(request, "Simulation terminée avec succès!")
    return redirect("simulator:simulation_detail", pk=pk)


def complete_simulation(request, pk):
    simulation = get_object_or_404(Simulation, pk=pk)
    simulation.status = "completed"
    simulation.completed_at = timezone.now()
    simulation.save()

    messages.success(request, "Simulation terminée avec succès!")
    return redirect("simulator:simulation_detail", pk=pk)


# Participant Management
def participant_list(request):
    participants = (
        Participant.objects.filter(user=request.user)
        if request.user.is_authenticated
        else []
    )
    return render(
        request, "simulator/participant_list.html", {"participants": participants}
    )


def participant_create(request):
    if request.method == "POST":
        speaker_name = request.POST.get("speaker_name")
        is_system = request.POST.get("is_system") == "on"

        Participant.objects.create(
            user=request.user, speaker_name=speaker_name, is_system=is_system
        )
        messages.success(request, "Participant créé avec succès!")
        return redirect("simulator:participant_list")

    return render(request, "simulator/participant_form.html")


def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk, user=request.user)
    participant.delete()
    messages.success(request, "Participant supprimé!")
    return redirect("simulator:participant_list")


# Dialogue Management
def dialogue_create(request, simulation_pk):
    simulation = get_object_or_404(Simulation, pk=simulation_pk)

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        difficulty_level = request.POST.get("difficulty_level")
        order = simulation.dialogues.count() + 1

        dialogue = Dialogue.objects.create(
            simulation=simulation,
            title=title,
            description=description,
            difficulty_level=difficulty_level,
            order=order,
        )

        messages.success(request, "Dialogue créé avec succès!")
        return redirect("simulator:dialogue_edit", pk=dialogue.pk)

    return render(request, "simulator/dialogue_form.html", {"simulation": simulation})


def dialogue_edit(request, pk):
    dialogue = get_object_or_404(Dialogue, pk=pk)
    participants = (
        Participant.objects.filter(user=request.user)
        if request.user.is_authenticated
        else []
    )
    lines = dialogue.lines.all()

    return render(
        request,
        "simulator/dialogue_edit.html",
        {"dialogue": dialogue, "participants": participants, "lines": lines},
    )


def dialogue_add_participant(request, pk):
    dialogue = get_object_or_404(Dialogue, pk=pk)
    participant_id = request.POST.get("participant_id")
    participant = get_object_or_404(Participant, pk=participant_id)
    dialogue.participants.add(participant)
    messages.success(request, "Participant ajouté!")
    return redirect("simulator:dialogue_edit", pk=pk)


def line_create(request, dialogue_pk):
    dialogue = get_object_or_404(Dialogue, pk=dialogue_pk)

    if request.method == "POST":
        participant_id = request.POST.get("participant_id")
        text = request.POST.get("text")
        order = dialogue.lines.count() + 1

        participant = get_object_or_404(Participant, pk=participant_id)

        DialogueLine.objects.create(
            dialogue=dialogue, participant=participant, order=order, text=text
        )

        messages.success(request, "Ligne ajoutée!")
        return redirect("simulator:dialogue_edit", pk=dialogue_pk)

    return redirect("simulator:dialogue_edit", pk=dialogue_pk)


def line_delete(request, pk):
    line = get_object_or_404(DialogueLine, pk=pk)
    dialogue_pk = line.dialogue.pk
    line.delete()
    messages.success(request, "Ligne supprimée!")
    return redirect("simulator:dialogue_edit", pk=dialogue_pk)


def participant_create_inline(request, pk):
    """Create participant and add to dialogue in one step"""
    dialogue = get_object_or_404(Dialogue, pk=pk)

    if request.method == "POST":
        speaker_name = request.POST.get("speaker_name")
        is_system = request.POST.get("is_system") == "on"

        participant = Participant.objects.create(
            user=request.user, speaker_name=speaker_name, is_system=is_system
        )

        dialogue.participants.add(participant)
        messages.success(request, f'Participant "{speaker_name}" créé et ajouté!')
        return redirect("simulator:dialogue_edit", pk=pk)

    return redirect("simulator:dialogue_edit", pk=pk)
