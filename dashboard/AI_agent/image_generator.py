import os
import base64
import multiprocessing
from together import Together
from dotenv import load_dotenv

load_dotenv()

def _generate_internal(prompt: str, steps: int, width: int, height: int):
    """
    Calls the Together API. Returns base64-encoded image data or raises.
    """
    client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
    if not client:
        raise RuntimeError("Together client init failed")
    resp = client.images.generate(
        model="black-forest-labs/FLUX.1-schnell-Free",
        prompt=prompt,
        steps=steps,
        width=width,
        height=height,
        response_format="b64_json",
    )
    if not (resp and getattr(resp, "data", None)):
        raise RuntimeError("No data in response")
    b64 = resp.data[0].b64_json
    if not b64:
        raise RuntimeError("Empty image returned")
    return b64

def generate_image(
    prompt: str,
    index: int,
    output_dir: str,
    steps: int = 2,
    width: int = 1024,
    height: int = 1024,
    timeout_seconds: int = 60,
    max_retries: int = 3,
) -> str:
    """
    Generates an image using Together API,
    saves as 'images/{index}.png', and returns the filepath.
    Retries and times out as needed.
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{index}.png"
    filepath = os.path.join(output_dir, filename)

    for attempt in range(1, max_retries + 1):
        with multiprocessing.Pool(1) as pool:
            async_res = pool.apply_async(
                _generate_internal,
                (prompt, steps, width, height)
            )
            try:
                b64_data = async_res.get(timeout=timeout_seconds)
            except multiprocessing.TimeoutError:
                print(f"[⏰] Timeout after {timeout_seconds}s. Retrying {attempt}/{max_retries}…")
                pool.terminate()
                pool.join()
                continue
            except Exception as e:
                print(f"[❌] Generation error ({e}). Retrying {attempt}/{max_retries}…")
                continue

            try:
                img_bytes = base64.b64decode(b64_data)
                with open(filepath, "wb") as f:
                    f.write(img_bytes)
                print(f"[✅] Image saved at: {filepath}")
                return filepath
            except Exception as e:
                print(f"[❌] Failed to save image ({e}). Retrying {attempt}/{max_retries}…")
                continue

    print(f"[🚫] All {max_retries} attempts failed. No image generated.")
    return ""
