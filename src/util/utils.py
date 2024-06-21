import os
import shutil
from collections import defaultdict
from const import event_translations

def limpiar_carpetas(carpetas):
    for carpeta in carpetas:
        if os.path.exists(carpeta):
            shutil.rmtree(carpeta)
        os.makedirs(carpeta)

def filter_close_frames(events, threshold=2):
    events.sort(key=lambda x: x['frame'])
    filtered_events = []
    last_event = None

    for event in events:
        if last_event and event['frame'] - last_event['frame'] <= threshold:
            if event['score'] > last_event['score']:
                last_event = event
        else:
            if last_event:
                filtered_events.append(last_event)
            last_event = event

    if last_event:
        filtered_events.append(last_event)

    return filtered_events

def combine_model_results(model1, model2, model3, frame_threshold=2):
    all_events = defaultdict(list)

    def collect_events(model):
        for item in model:
            video = item['video']
            for event in item['events']:
                all_events[video].append(event)

    collect_events(model1)
    collect_events(model2)
    collect_events(model3)

    final_results = []
    for video, events in all_events.items():
        events = filter_close_frames(events, threshold=frame_threshold)
        final_results.append({'video': video, 'events': events, 'fps': model1[0]['fps']})

    return final_results

def procesar_resultados(data):
    event_details = []
    for match in data:
        video = match['video']
        fps = match['fps']
        events = match['events']
        for event in events:
            label = event['label']
            frame = event['frame']
            second = round(frame / fps)
            if second >= 60:
                minutes = int(second // 60)
                seconds = int(second % 60)
                time_str = f"minuto {minutes}:{seconds:02d}"
            else:
                time_str = f"segundo {int(second)}"
            label_es = event_translations.get(label, label)
            event_details.append(f"{label_es} en el {time_str}")

    return video, event_details