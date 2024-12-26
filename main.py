import json
from urllib import request, parse
import random
from datetime import datetime
import yaml
import json
import time
import os
import argparse

current_script_path = os.path.abspath(__file__)
current_script_dir = os.path.dirname(current_script_path)
os.chdir(current_script_dir)


with open("tags/static_tags.yml", "r", encoding="utf-8") as file:
    static_tags_data = yaml.safe_load(file)

single_male_tags = static_tags_data["一男一女"]
multi_male_tags = static_tags_data["多男一女"]
camera_tags = static_tags_data["多样镜头"]
nsfw_clothed_tags = static_tags_data["NSFW着衣"]
nsfw_half_nude_tags = static_tags_data["NSFW半裸"]
nsfw_complete_nude_tags = static_tags_data["NSFW全裸"]
nsfw_cum_tags = static_tags_data["NSFW中出"]
quality_tags = static_tags_data["质量"]


def pick_by_category(category):
    data = {}
    with open("tags/sex.yml", "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
        topic_name = random.choice(list(data[category].keys()))
        return topic_name, data[category][topic_name]


def pick(data, key=""):
    if key == "":
        random_key = random.choice(list(data.keys()))
        return random_key, ", " + data[random_key] + ", "
    else:
        return key, ", " + data[key] + ", "


def pick_env(env_name=""):
    with open("tags/env.yml", "r", encoding="utf-8") as file:
        envs = yaml.safe_load(file)
    return pick(envs, env_name)


def pick_chara(chara_name=""):
    with open("tags/chara.yml", "r", encoding="utf-8") as file:
        charas = yaml.safe_load(file)
    return pick(charas, chara_name)


def pick_outfit(outfit_name=""):
    with open("tags/female_outfit.yml", "r", encoding="utf-8") as f:
        outfits = yaml.safe_load(f)
    return pick(outfits, outfit_name)


def get_film_cfg(outfit_name="", env_name="", chara_name=""):
    if outfit_name == "":
        outfit_name, outfit = pick_outfit()
    else:
        outfit_name, outfit = pick_outfit(outfit_name)

    if env_name == "":
        env_name, env = pick_env()
    else:
        env_name, env = pick_env(env_name)

    if chara_name == "":
        chara_name, chara = pick_chara()
    else:
        chara_name, chara = pick_chara(chara_name)

    static_tags = ", ".join([chara, outfit, env, quality_tags])

    scene_cfgs = []

    def make_scene(topic_category, extra_tags: str):
        topic_name, topic = pick_by_category(topic_category)
        spell = f", (one girl doing {topic} with nude man), "

        if "(" in topic or ")" in topic:
            topic = topic
        else:
            topic = ", (" + topic + ": 1.2), "
        final_tags = static_tags + topic + extra_tags
        final_tags = final_tags.replace(", ,", ", ")
        final_tags = final_tags.replace(",,", ", ")

        scene_cfg = {
            "category": topic_category,
            "name": topic_name,
            "tags": final_tags,
        }
        scene_cfgs.append(scene_cfg)

    make_scene("自我展示", "")
    make_scene("调戏", "")
    make_scene("进一步调戏", "")
    make_scene("口交", nsfw_clothed_tags + ", (seductive_smile:1.1), heart, ")
    make_scene("口交结束", nsfw_clothed_tags + ", heart, ")
    make_scene("准备", nsfw_clothed_tags + ", (pussy), (breasts_out), ")
    make_scene("进行", nsfw_clothed_tags)
    make_scene("进行", nsfw_half_nude_tags)
    make_scene("进行", nsfw_complete_nude_tags)
    make_scene(
        "进行",
        nsfw_cum_tags
        + random.choice(
            [
                "fucked_silly",
                "breasts_grab, breasts_squeeze, lactation",
                "(head_back:1.2), excessive pussy juice, fingering,",
            ]
        ),
    )
    make_scene("事后", ",nsfw,")

    for scene_cfg in scene_cfgs:
        if scene_cfg["category"] != "自我展示":
            scene_cfg["tags"] = scene_cfg["tags"] + " , " + single_male_tags

    film_cfg = {
        "scene_cfgs": scene_cfgs,
        "outfit_name": outfit_name,
        "env_name": env_name,
        "chara_name": chara_name,
    }
    return film_cfg


def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode("utf-8")
    req = request.Request(
        f"http://{cfg['COMFYUI_IP']}:{cfg['COMFYUI_PORT']}/prompt", data=data
    )
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


def construct_prompt(scene_prefix_list, scene_cfg):
    with open(cfg["workflow_filepath"], "r", encoding="utf-8") as file:
        print("_".join(scene_prefix_list))
        prompt_template = json.load(file)

        for i in range(cfg["n_repeat_vert_img"]):
            seed = generate_random_15_digit_number()
            prompt_template["3"]["inputs"]["seed"] = seed
            prompt_template["6"]["inputs"]["text"] = scene_cfg["tags"]
            prompt_template["5"]["inputs"]["width"] = cfg["vert_img_width"]
            prompt_template["5"]["inputs"]["height"] = cfg["vert_img_height"]
            prompt_template["5"]["inputs"]["batch_size"] = cfg["n_batch_vert_img"]
            prompt_template["9"]["inputs"]["filename_prefix"] = "_".join(
                scene_prefix_list + ["竖", str(seed)]
            )
            queue_prompt(prompt_template)
            time.sleep(1)

        for i in range(cfg["n_repeat_hor_img"]):
            seed = generate_random_15_digit_number()
            prompt_template["3"]["inputs"]["seed"] = seed
            prompt_template["6"]["inputs"]["text"] = scene_cfg["tags"]
            prompt_template["5"]["inputs"]["width"] = cfg["hor_img_width"]
            prompt_template["5"]["inputs"]["height"] = cfg["hor_img_height"]
            prompt_template["5"]["inputs"]["batch_size"] = cfg["n_batch_hor_img"]
            prompt_template["9"]["inputs"]["filename_prefix"] = "_".join(
                scene_prefix_list + ["横", str(seed)]
            )
            queue_prompt(prompt_template)
            time.sleep(1)


def generate_random_15_digit_number():
    random.seed(int(time.time()))
    return str(random.randint(10**14, 10**15 - 1))


def random_test(n_film=50):
    for i in range(n_film):
        film_cfg = get_film_cfg()

        for scene_cfg in film_cfg["scene_cfgs"]:
            scene_prefix_list = [
                datetime.now().strftime("%Y%m%d"),
                film_cfg["env_name"],
                film_cfg["chara_name"],
                film_cfg["outfit_name"],
                scene_cfg["name"],
            ]
            construct_prompt(scene_prefix_list, scene_cfg)


def preset_test(presets):
    for preset in presets:
        film_cfg = get_film_cfg(
            outfit_name=preset[2], env_name=preset[0], chara_name=preset[1]
        )

        for scene_cfg in film_cfg["scene_cfgs"]:
            scene_prefix_list = [
                datetime.now().strftime("%Y%m%d"),
                film_cfg["env_name"],
                film_cfg["chara_name"],
                film_cfg["outfit_name"],
                scene_cfg["name"],
            ]
            construct_prompt(scene_prefix_list, scene_cfg)


cfg = None
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config_file", type=str, default="config/example.yml", help="配置文件的路径"
    )

    args = parser.parse_args()
    with open(args.config_file, "r", encoding="utf-8") as file:
        cfg = yaml.safe_load(file)

    print(cfg)
    preset_test(cfg["films"])
