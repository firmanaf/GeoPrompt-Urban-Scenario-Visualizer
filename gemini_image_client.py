# -*- coding: utf-8 -*-
import io


def edit_image_with_gemini(api_key: str, model: str, input_png: str, prompt: str) -> bytes:
    """
    Send QGIS exported PNG + prompt to Google Gemini image model.

    Tested target model family:
    - gemini-2.5-flash-image
    - gemini-3-pro-image-preview where available

    The google-genai package is required in the QGIS Python environment.
    """
    if not api_key:
        raise RuntimeError("Google Gemini API key is empty. Enter an API key or set the GOOGLE_API_KEY / GEMINI_API_KEY environment variable.")
    if not model:
        raise RuntimeError("Gemini model is empty. Select a model or enter a custom model ID.")

    try:
        from google import genai
        from google.genai import types
    except Exception as e:
        raise RuntimeError(
            "Python package 'google-genai' is not available in the QGIS environment. "
            "Install it using QGIS Python, for example: python -m pip install google-genai"
        ) from e

    try:
        from PIL import Image
    except Exception as e:
        raise RuntimeError(
            "Python package 'Pillow' is not available in the QGIS environment. "
            "Install it using QGIS Python, for example: python -m pip install Pillow"
        ) from e

    try:
        client = genai.Client(api_key=api_key)
        image = Image.open(input_png)

        response = client.models.generate_content(
            model=model,
            contents=[prompt, image],
            config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
        )

        candidates = getattr(response, "candidates", None) or []
        for cand in candidates:
            content = getattr(cand, "content", None)
            parts = getattr(content, "parts", None) or []
            for part in parts:
                inline_data = getattr(part, "inline_data", None)
                if inline_data is not None and getattr(inline_data, "data", None):
                    data = inline_data.data
                    return data if isinstance(data, bytes) else bytes(data)

        # Fallback for SDK response shapes.
        parts = getattr(response, "parts", None) or []
        for part in parts:
            inline_data = getattr(part, "inline_data", None)
            if inline_data is not None and getattr(inline_data, "data", None):
                data = inline_data.data
                return data if isinstance(data, bytes) else bytes(data)

        text = getattr(response, "text", "")
        if text:
            raise RuntimeError(
                "Gemini returned text instead of an image. "
                "Make sure the selected model supports image generation/editing. "
                f"Text response: {text[:500]}"
            )

        raise RuntimeError("Gemini did not return inline image data.")

    except Exception as e:
        msg = str(e)
        low = msg.lower()
        if "resource_exhausted" in low or "quota exceeded" in low or "free_tier_requests" in low or "rate-limits" in low:
            raise RuntimeError(
                "Gemini API quota has been exhausted or the free tier for this project/model is zero. "
                "Enable billing or a paid plan in Google AI Studio or the Google Cloud project used by the API key, "
                "wait for quota reset, or use another provider such as OpenAI. "
                "This is not a plugin error and not a google-genai package issue."
            ) from e
        if "api key" in low or "permission" in low or "unauthorized" in low or "403" in low:
            raise RuntimeError(
                "Gemini access was denied. Check your Google Gemini API key and model access in Google AI Studio."
            ) from e
        if "model" in low and ("not found" in low or "not supported" in low or "not available" in low):
            raise RuntimeError(
                f"Gemini model '{model}' is not available or does not support generateContent for this API key. "
                "Use the default Gemini image model: gemini-2.5-flash-image. "
                "For Gemini 3 Pro Image Preview, make sure the API key has access to gemini-3-pro-image-preview."
            ) from e
        raise
