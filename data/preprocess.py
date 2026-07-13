def preprocess_function(examples, tokenizer):
    inputs = tokenizer(
        examples["source"],
        max_length=256,
        truncation=True,
        padding="max_length"
    )
    
    labels = tokenizer(
        text_target=examples["target"],
        max_length=128,
        truncation=True,
        padding="max_length",
    )

    '''with tokenizer.as_target_tokenizer():
        labels = tokenizer(
            examples["target"],
            max_length=128,
            truncation=True,
            padding="max_length"
        )'''

    inputs["labels"] = labels["input_ids"]
    return inputs
