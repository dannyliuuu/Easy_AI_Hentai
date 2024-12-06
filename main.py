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
    # make_scene("调戏", ", (seductive_smile:1.1) ")
    # make_scene("调戏", "")
    # make_scene("进一步调戏", "")
    # make_scene("口交", nsfw_clothed_tags + ", (oral_sex), (seductive_smile:1.1), heart, ")
    # make_scene("口交结束", nsfw_clothed_tags + ", (oral_sex), (seductive_smile:1.1), heart, ")
    # make_scene("准备", nsfw_clothed_tags + ", (pussy), (breasts_out), ")
    # make_scene("进行", nsfw_clothed_tags)
    # make_scene("进行", nsfw_half_nude_tags)
    # make_scene("进行", nsfw_complete_nude_tags)
    # make_scene(
    #     "进行",
    #     nsfw_cum_tags
    #     + random.choice(
    #         [
    #             "fucked_silly",
    #             "breasts_grab, breasts_squeeze, lactation",
    #             "(head_back:1.2), excessive pussy juice, fingering,",
    #         ]
    #     ),
    # )
    # make_scene("事后", ",nsfw,")

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
    req = request.Request("http://127.0.0.1:8188/prompt", data=data)
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
    with open("prompt_template.json", "r", encoding="utf-8") as file:
        print("_".join(scene_prefix_list))
        prompt_template = json.load(file)

        seed = generate_random_15_digit_number()
        prompt_template["3"]["inputs"]["seed"] = seed
        prompt_template["6"]["inputs"]["text"] = scene_cfg["tags"]

        prompt_template["5"]["inputs"]["width"] = 960
        prompt_template["5"]["inputs"]["height"] = 1440
        prompt_template["9"]["inputs"]["filename_prefix"] = "_".join(
            scene_prefix_list + ["竖", str(seed)]
        )

        queue_prompt(prompt_template)
        time.sleep(1)

        prompt_template["5"]["inputs"]["width"] = 1440
        prompt_template["5"]["inputs"]["height"] = 960
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

def env_test():
    preset_test([
        ("简单黑背景", "崩铁卡夫卡", "角色默认服装"),
        ("简单白背景", "崩铁卡夫卡", "圣诞老人"),
        ("简单灰背景", "崩铁卡夫卡", "铁十字军装"),
        ("教室", "崩铁卡夫卡", "OL_suit"),
        ("室内篮球场", "崩铁卡夫卡", "吴京健身服"),
        ("器材室", "崩铁卡夫卡", "日式运动服"),
        ("图书馆", "崩铁卡夫卡", "JK"),
        ("校园走廊", "崩铁卡夫卡", "厚黑JK"),
        ("酒店大床夜晚窗户", "崩铁卡夫卡", "圣姨银色礼服"),
        ("演唱会", "崩铁卡夫卡", "偶像演出服"),
        ("淋浴浴室", "崩铁卡夫卡", "裸体浴巾"),
        ("浴缸浴室", "崩铁卡夫卡", "裸体浴巾"),
        ("海滩", "崩铁卡夫卡", "美国国旗比基尼"),
        ("室内泳池", "崩铁卡夫卡", "连体泳衣"),
        ("露天泳池", "崩铁卡夫卡", "连体泳衣"),
        ("公园", "崩铁卡夫卡", "裸体大衣"),
        ("酷刑室", "崩铁卡夫卡", "警官_浅蓝色"),
        ("小巷", "崩铁卡夫卡", "挎包口罩学生服"),
        ("赌场", "崩铁卡夫卡", "逆兔女郎蕾丝翻边"),
        ("赛车场", "崩铁卡夫卡", "巴尔的摩赛车女郎"),
        ("咖啡厅", "崩铁卡夫卡", "角色默认服装"),
        ("中世纪酒馆", "崩铁卡夫卡", "舞者"),
        ("现代酒吧", "崩铁卡夫卡", "渔网袜比基尼拉皮条"),
        ("办公室", "崩铁卡夫卡", "OL_suit"),
        ("监狱", "崩铁卡夫卡", "警官_浅蓝色"),
        ("脱衣舞秀钢管舞", "崩铁卡夫卡", "逆兔女郎"),
        ("地下拳场", "崩铁卡夫卡", "健身房服"),
        ("温泉", "崩铁卡夫卡", "裸体浴巾"),
        ("病房", "崩铁卡夫卡", "护士"),
        ("健身房", "崩铁卡夫卡", "健身房服"),
        ("电车", "崩铁卡夫卡", "挎包口罩学生服"),
        ("神社", "崩铁卡夫卡", "巫女"),
        ("和室", "崩铁卡夫卡", "和服"),
        ("大街", "崩铁卡夫卡", "旗袍"),
        ("收银台", "崩铁卡夫卡", "便利店员工"),
        ("中式豪华室内", "崩铁卡夫卡", "旗袍"),
        ("录制现场", "崩铁卡夫卡", "爱宕赛车女郎"),
        ("练舞室", "崩铁卡夫卡", "芭蕾舞者"),
        ("沙发", "崩铁卡夫卡", "裸体围裙"),
    ])
    


if __name__ == "__main__":
    # random_test(n_film = 50)
    # env_test()
    preset_test([
        ("简单灰背景", "崩铁卡夫卡", "铁十字军装"),
        ("教室", "崩铁卡夫卡", "OL_suit"),
        ("室内篮球场", "崩铁卡夫卡", "吴京健身服"),
        ("图书馆", "崩铁卡夫卡", "JK"),
        ("公园", "崩铁卡夫卡", "裸体大衣"),
        ("酷刑室", "崩铁卡夫卡", "警官_浅蓝色"),
        ("小巷", "崩铁卡夫卡", "挎包口罩学生服"),
        ("中世纪酒馆", "崩铁卡夫卡", "舞者"),
        ("赌场", "崩铁卡夫卡", "逆兔女郎蕾丝翻边"),
        ("赛车场", "崩铁卡夫卡", "巴尔的摩赛车女郎"),
        ("收银台", "崩铁卡夫卡", "便利店员工"),
        ("练舞室", "崩铁卡夫卡", "芭蕾舞者"),
    ])

    
    # preset_test([
    #     ("赌场", "崩铁卡夫卡", "黑色兔女郎"),
    #     ("小巷", "亚丝娜", "挎包口罩学生服"),
    #     ("校园走廊", "短发瘦小JK", "厚黑JK"),
    #     ("海滩", "马尾宝多六花", "宝多六花比基尼"), 
    # ])
