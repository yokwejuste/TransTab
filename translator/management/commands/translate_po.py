from django.core.management.base import BaseCommand
from utils.translate import translate_po_files


class Command(BaseCommand):
    help = "Translates all .po files using AWS Translate"

    def handle(self, *args, **options):
        translate_po_files()
        self.stdout.write(self.style.SUCCESS("Successfully translated .po files."))
