# Easy_AI_Hentai 色图八股

色图是八股文，因为：
1. 一些tag必须组合使用才有效果。
2. 观众习惯了某个体位和某个视角的组合
3. 穿什么衣服做什么事，穿着比基尼在赌场做爱就显得太奇怪了（最终我发现随机组合那个函数 `random_test` 实在是意义不大，还是用 `preset_test` 吧）

我试图让每个人都能像 Pixiv 上那些卖AI图的人一样，可以快速生成一个俗套剧本指导下的图集。

# 使用方法
1. 先启动comfyui (https://github.com/comfyanonymous/ComfyUI), 工作流可以用你自己的，保存成API格式，替换掉 `prompt_template.json` ，把main.py里对应节点的定义也改了。如果你用我这个，那么确保你本地已经有模型： `obsessionIllustrious_v30.safetensors` 和 lora:  `Hyper-SDXL-12steps-CFG-lora.safetensors`, 这是默认的 `prompt_template.json` 里使用的。
2. 启动main.py 这个脚本没有额外的依赖，你只要有一个python环境就行

# LICENSE
本项目使用 MIT LICENSE, 如果你用了这个项目，还请引用本仓库，保留协议。
