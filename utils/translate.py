import os
import boto3
import polib
from django.conf import settings

def translate_text(text, source_language, target_language):
    translate = boto3.client(
        "translate",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )

    result = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    return result.get("TranslatedText")


def translate_po_files():
    dirs = [
        d for d in os.listdir("locale") if os.path.isdir(os.path.join("locale", d))
    ]
    for dir in dirs:
        po = polib.pofile(f"locale/{dir}/LC_MESSAGES/django.po")
        target_language = po.metadata['Language']
        for entry in po:
            if not entry.translated():
                translated_text = translate_text(entry.msgid, 'auto', target_language)
                entry.msgstr = translated_text
        po.save()
