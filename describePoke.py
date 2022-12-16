from transformers import AutoImageProcessor, GPT2TokenizerFast, VisionEncoderDecoderModel
from PIL import Image


def create_description(model_name: str, image_ref: Image) -> str:
    """function for performing inference on an image to text
        Parmaters:
            model_name (str) can be file path to locally stored model or remote hosted on huggingface

            image_ref (PIL.Image) PIL image object
        Returns:
            description (str) Generated description
    """
    # load our fine-tuned image captioning model and corresponding tokenizer and image processor
    model = VisionEncoderDecoderModel.from_pretrained(model_name)
    tokenizer = GPT2TokenizerFast.from_pretrained(model_name)
    image_processor = AutoImageProcessor.from_pretrained(model_name)


    # inference on an image
    pixel_values = image_processor(image_ref.convert("RGB"), return_tensors="pt").pixel_values

    # generate caption
    generated_ids = model.generate(pixel_values)
    generated_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    #TODO generated text polishing
    return generated_text


def main():
    #testing function
    model_name = "models/vit-base-patch16-224-in21k-gpt2-finetuned-to-pokemon-descriptions"
    #url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png"


    #image = Image.open('/Users/tylerkarren/poke/poke-server/test.png')
    
    #description = create_description(model_name=model_name, image_ref=image)
    #print(description)

    #TODO test/measure inference time



if __name__ == "__main__":
    main()