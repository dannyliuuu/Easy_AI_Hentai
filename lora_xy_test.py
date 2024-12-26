import json
from urllib import request, parse
import random
from datetime import datetime
import yaml
import json
import time
import os

current_script_path = os.path.abspath(__file__)
current_script_dir = os.path.dirname(current_script_path)
os.chdir(current_script_dir)


def generate_random_15_digit_number():
    random.seed(int(time.time()))
    return str(random.randint(10**14, 10**15 - 1))


def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode("utf-8")
    req = request.Request("http://127.0.0.1:8089/prompt", data=data)
    try:
        with request.urlopen(req) as response:
            response_data = response.read().decode("utf-8")
            parsed_data = json.loads(response_data)
            prompt_id = parsed_data.get("prompt_id", "Unknown ID")
            images = parsed_data.get("images", [])
            print(f"Prompt ID: {prompt_id}")
            return parsed_data
    except Exception as e:
        print(f"Error during API request: {e}")
        return None


def construct_prompt():
    with open("prompt_template_coolsummer_lora.json", "r", encoding="utf-8") as file:
        prompt_template = json.load(file)

        for strengh in [0.2, 0.4, 0.6, 0.8, 1.0]:
            for lora in [
                "coolsummer-000001.safetensors",
                "coolsummer-000002.safetensors",
                "coolsummer-000003.safetensors",
                "coolsummer-000004.safetensors",
                "coolsummer-000005.safetensors",
                "coolsummer-000006.safetensors",
                "coolsummer-000007.safetensors",
                "coolsummer-000008.safetensors",
                "coolsummer-000009.safetensors",
                "coolsummer-000010.safetensors",
                "coolsummer-000011.safetensors",
                "coolsummer-000012.safetensors",
                "coolsummer-000013.safetensors",
                "coolsummer-000014.safetensors",
                "coolsummer-000015.safetensors",
                "coolsummer-000016.safetensors",
                "coolsummer-000017.safetensors",
                "coolsummer-000018.safetensors",
                "coolsummer-000019.safetensors",
                "coolsummer-000020.safetensors",
            ]:
                seed = generate_random_15_digit_number()
                prompt_template["3"]["inputs"]["seed"] = seed

                prompt_template["10"]["inputs"]["lora_name"] = lora
                prompt_template["10"]["inputs"]["strength_model"] = strengh

                prompt_template["6"]["inputs"][
                    "text"
                ] = "nsfw, breasts, cum, eula_(genshin_impact), censored, hetero, cum in pussy, large breasts, sex, nipples, penis, nude, heart, ahegao, pussy, completely nude, leash, 1girl, tongue out, tongue, navel, blue hair, vaginal, hairband, grabbing, outdoors, grabbing another's breast, rolling eyes, collar, open mouth, blush, night, public indecency, spread legs, hair ornament, reverse cowgirl position, grabbing from behind, thighs, stomach, black hairband, multiple boys, cum on body, sex from behind, tree, straddling, medium hair, testicles, solo focus, 1boy, girl on top, cum on breasts, fucked silly, saliva, cum overflow, animal collar"

                prompt_template["5"]["inputs"]["width"] = 960
                prompt_template["5"]["inputs"]["height"] = 1440
                prompt_template["5"]["inputs"]["batch_size"] = 1

                filename_prefix = (
                    "lora_test_" + str(strengh) + "_" + lora.replace(".safetensors", "")
                )
                print(filename_prefix)
                prompt_template["9"]["inputs"]["filename_prefix"] = filename_prefix

                queue_prompt(prompt_template)
                time.sleep(1)


construct_prompt()
