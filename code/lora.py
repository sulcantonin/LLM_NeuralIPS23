import re

def prompt_formatter(question, answer = ""):
    # https://github.com/lm-sys/FastChat/blob/main/docs/vicuna_weights_version.md
    return f'### Human:\n{question}\n### Assistant:{answer}\n'
    # return f'USER: {question}\nASSISTANT: {answer}</s>'
    

def test(q, model, tokenizer, max_length, temperature):
    device = model.device
    inputs = tokenizer(q, return_tensors="pt", return_token_type_ids=False).to(device)

    outputs = model.generate(
        **inputs,
        max_length=max_length,
        # repetition_penalty=1.05,
        eos_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_p=1.0,  
        # top_k=64,
        temperature=temperature,
    )
    for output in outputs:
        answer = tokenizer.decode(output, skip_special_tokens=True)
        answer = re.sub(r'\n+','\n',answer)
        print(f"{answer}\n---------")