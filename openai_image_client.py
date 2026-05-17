# -*- coding: utf-8 -*-
import base64
import urllib.request


def edit_image_with_openai(api_key: str, model: str, input_png: str, prompt: str, size: str, quality: str) -> bytes:
    if not api_key:
        raise RuntimeError("OpenAI API key is empty. Please enter an API key first.")
    if not model:
        raise RuntimeError("Model ID is empty. Select a model or enter a custom model ID.")
    try:
        from openai import OpenAI
    except Exception as e:
        raise RuntimeError(
            "Python package 'openai' is not available in the QGIS environment. "
            "Install it using QGIS Python, for example: python -m pip install openai"
        ) from e

    client = OpenAI(api_key=api_key)
    image_file = open(input_png, "rb")
    kwargs = {
        "model": model,
        "image": image_file,
        "prompt": prompt,
        "size": size,
    }

    # Legacy DALL·E 2 edit endpoint is stricter: one square PNG, no quality parameter.
    if model != "dall-e-2" and quality and quality != "default":
        kwargs["quality"] = quality

    try:
        result = client.images.edit(**kwargs)
    except Exception as e:
        msg = str(e)
        if "must be verified" in msg or "verified" in msg and "organization" in msg:
            raise RuntimeError(
                f"Model '{model}' requires a verified organization on the OpenAI Platform. "
                "Use gpt-image-1.5, gpt-image-1, gpt-image-1-mini, or gpt-image-2 if available for your account, "
                "or verify your organization on the OpenAI Platform."
            ) from e
        if "dall-e-2" in model and ("square" in msg.lower() or "png" in msg.lower()):
            raise RuntimeError(
                "DALL·E 2 only supports one square PNG input and limited sizes. "
                "Use Square 1024x1024 output size or choose a GPT Image model."
            ) from e
        if "model" in msg.lower() and ("not found" in msg.lower() or "does not exist" in msg.lower() or "access" in msg.lower()):
            raise RuntimeError(
                f"Model '{model}' is not available for this API key/project. "
                "Choose another model available in your OpenAI account or use a valid custom model ID."
            ) from e
        raise
    finally:
        try:
            image_file.close()
        except Exception:
            pass

    if not getattr(result, "data", None):
        raise RuntimeError("OpenAI did not return image data.")

    item = result.data[0]
    b64 = getattr(item, "b64_json", None)
    if b64:
        return base64.b64decode(b64)

    url = getattr(item, "url", None)
    if url:
        with urllib.request.urlopen(url, timeout=120) as r:
            return r.read()

    raise RuntimeError("The OpenAI response does not contain b64_json or an image URL.")
