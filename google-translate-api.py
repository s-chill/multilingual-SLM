import os
from google.cloud import translate_v3beta1 as translate

with open("./data/test.txt", "r", encoding="utf-8") as file:
    text = file.read()

def translate_text(text=text, project_id="zippy-entry-437816-i6", target_language="ta"):
    if len(text) > 30000:
        print("too long, need to split this document up")
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "en-US",
            "target_language_code": target_language,
        }
    )

    # for translation in response.translations:
        # print("Translated text: {}".format(translation.translated_text))
    
    return response.translations[0].translated_text

def translate_all_files(project_id="zippy-entry-437816-i6", input_folder="data", output_folder="translated"):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):  # only text files
            file_path = os.path.join(input_folder, filename)
            
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            
            translated_content = translate_text(text=content)
            
            translated_filename = filename.replace(".txt", "_tamil.txt")
            output_path = os.path.join(output_folder, translated_filename)

            with open(output_path, "w", encoding="utf-8") as translated_file:
                translated_file.write(translated_content)

            print(f"Translated {filename} -> {translated_filename}")

translate_all_files()