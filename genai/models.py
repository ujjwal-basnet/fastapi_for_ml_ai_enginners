import torch 
from transformers import Pipeline, pipeline

system_prompt= "you are an ai helper , you only answer in 10 words"
prompt= "what is numpy"


def load_text_model(device= "cpu"):
    pipe = pipeline(
        "text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", 
        dtype=torch.bfloat16,
        device= device
    )
    return pipe

def generate_text(pipe: Pipeline , prompt:str, temperature: float=0.7) -> str:
    messages= [ 
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    prompt= pipe.tokenizer.apply_chat_template(
        messages, tokenize= False, add_generation_prompt= True
    )
    
    prediction= pipe(
        prompt, 
        temperature= temperature,
        max_new_tokens=20, ## max tokens are making less for fast output , this will lead in inaccurate result
        do_sample= True,
        top_k=5, # keep most 5 probable tokens discard rest (keeping only 5 because i want fast answer for testing , but this will downgraded the output accuraccy)
        top_p=0.95 ## necleus sampling keep probaab greater then 95% proba and do necleus sampling
    )

    output= prediction[0]['generated_text'].split('</s>\n<|assistant|>\n')[-1]
    return output


if __name__ == "__main__":
    model= load_text_model(device="cuda")
    print(generate_text(model, prompt= prompt))
