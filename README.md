# Easy_AI_Hentai 色图八股

色图是八股文，因为：
1. 一些tag必须组合使用才有效果。
2. 观众习惯了某个体位和某个视角的组合
3. 穿什么衣服做什么事，穿着比基尼在赌场做爱就显得太奇怪了（最终我发现随机组合那个函数 `random_test` 实在是意义不大，还是用 `preset_test` 吧）

我试图让每个人都能像 Pixiv 上那些卖AI图的人一样，可以快速生成一个俗套剧本指导下的图集。

# 前置需求
确保你已经能够成功安装并使用 ComfyUI (https://github.com/comfyanonymous/ComfyUI)

# 使用方法
1. 在命令行中执行 

    `git clone https://github.com/dannyliuuu/Easy_AI_Hentai.git`
2. 进入目录 `Easy_AI_Hentai`，根据自己需要修改：
   - `tags/static_tags` 里的负面tag
   - `workflow_templates/0lora.json`的4号节点，将 `ckpt_name` 修改为你自己的大模型的名字
   - `config/example.yml`，修改端口号为你自己安装的ComfyUI的端口号（默认应该是8188，但也有可能你的端口号并不一样）。修改图片大小为你需要的长和宽。
   - `config/example.yml`，修改`film`的参数，人物请参考`tags/chara.yml`，衣装请参考`tags/female_outfit.yml`，地点请参考`tags/env.yml`，如果没有你需要的，请在对应的yml文件里添加配置，英文tag均遵循 danbooru (https://danbooru.donmai.us/) 格式
3. 启动 ComfyUI
4. 命令行执行 `python main.py`，正常的话，你的ComfyUI会接收到一堆 prompts, 并开始绘图。默认配置下，每个体位会生成4张纵向图和4张横向图，这是因为我发现有些体位对于图片的纵向或横向很敏感，横向可以完美出图，但纵向就一团糟（反之亦然），所以索性全都生成一遍。

# 预设工作流 & 自定义工作流 
目前包含三个预设模板：

1. `workflow_templates/0lora.json` 直接使用大模型生成，默认使用的是 `obsessionIllustrious_v30`
2. `workflow_templates/1lora_hyper_sdxl.json` 使用 大模型 + 一个 lora 生成，默认使用的是 `obsessionIllustrious_v30` 和 `Hyper-SDXL-12steps-CFG-lora`，这个生成速度会快一点
3. `workflow_templates/1lora_自炼coolsummer.json` 我自己测试用的，请无视它

如果你想用你自己的工作流，请先用 ComfyUI 将其保存为 API 格式 （Export (API)），放置在`workflow_templates`目录中，并修改`config/example.yml`的配置`workflow_filepath`。另外，这个项目的目标是用提示词组合大批量生成图片，因此稍微复杂的工作流（比如图生图）是不支持的。基本上，你只能在预设工作流上调调参数、换换模型。

# 用户：“你写的提示词太烂了，根本生成不出来能用的图！”
额，确实如此。如果你发现生成的图很烂，可以尝试修改`tags`目录下的定义，英文tag均遵循 danbooru (https://danbooru.donmai.us/) 格式

# LICENSE
本项目使用 MIT LICENSE, 如果你用了这个项目，还请引用本仓库，保留协议。
