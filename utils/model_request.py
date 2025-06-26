import random
import string
import time


def generate_random_id(length=24):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def mock_openai_completion_chunk(event_id, model_name, message_content):
    event_id = generate_random_id()
    created = int(time.time())
    first_data = {
        "id": event_id,
        "object": "chat.completion.chunk",
        "created": created,
        "model": model_name,
        "service_tier": "default",
        "system_fingerprint": "fp_4691090a87",
        "choices": [{
            "index": 0,
            "delta": {"content": "本模型暂时仅针对Pro用户开放，后续敬请期待....\n"},  # 空的delta
            "logprobs": "null",
            "finish_reason": "stop"  # 标记流结束
        }]
    }