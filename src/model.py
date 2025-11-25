from transformers import AutoModelForTokenClassification, AutoConfig
from labels import LABEL2ID, ID2LABEL


def create_model(model_name: str, dropout: float = 0.3):
    """
    Create token classification model with custom dropout for better generalization
    """
    config = AutoConfig.from_pretrained(
        model_name,
        num_labels=len(LABEL2ID),
        id2label=ID2LABEL,
        label2id=LABEL2ID,
        hidden_dropout_prob=dropout,
        attention_probs_dropout_prob=dropout,
    )
    
    model = AutoModelForTokenClassification.from_pretrained(
        model_name,
        config=config,
    )
    return model
