# coordinator.py
from connectors.openai_connector import detect_language_openai
from connectors.gemini_connector import detect_language_gemini
from connectors.sarvam_connector import detect_language_sarvam
from connectors.elevenlabs_connector import detect_language_elevenlabs

def coordinate_detection(audio_file_path: str):
    results = []
    
    openai_result = detect_language_openai(audio_file_path)
    results.append({
        "provider": "OpenAI",
        **openai_result
    })
    
    gemini_result = detect_language_gemini(audio_file_path)
    results.append({
        "provider": "Google Gemini",
        **gemini_result
    })
    
    sarvam_result = detect_language_sarvam(audio_file_path)
    results.append({
        "provider": "Sarvam AI",
        **sarvam_result
    })
    
    elevenlabs_result = detect_language_elevenlabs(audio_file_path)
    results.append({
        "provider": "ElevenLabs",
        **elevenlabs_result
    })
    
    return results