import torch
from prompt_to_prompt_pipeline import Prompt2PromptPipeline

if __name__ == "__main__":

    device = torch.device('cuda:0') if torch.cuda.is_available() else torch.device('cpu')
    if device.type == "cuda":
        pipe = Prompt2PromptPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0",
                                                    torch_dtype=torch.float16, use_safetensors=True).to(device)
    else:
        pipe = Prompt2PromptPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0",
                                                    torch_dtype=torch.float32, use_safetensors=False).to(device)
    seed = 864
    g_cpu = torch.Generator().manual_seed(seed)

    # prompts = ["a pink bear riding a bicycle on the beach", "a pink dragon riding a bicycle on the beach"]
    # cross_attention_kwargs = {"edit_type": "replace",
    #                           "n_self_replace": 0.4,
    #                           "n_cross_replace": {"default_": 1.0, "dragon": 0.4},
    #                           }

    prompts = ["a chocolate cake", "a confetti chocolate cake"]
    cross_attention_kwargs = {"edit_type": "refine",
                              "n_self_replace": 0.4,
                              "n_cross_replace": {"default_": 1.0, "confetti": 0.8},
                              }

    image = pipe(prompts, cross_attention_kwargs=cross_attention_kwargs, generator=g_cpu)
    print(f"Num images: {len(image['images'])}")
    from IPython.display import display

    for img in image['images']:
        display(img)
