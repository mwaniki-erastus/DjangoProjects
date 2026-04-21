from pathlib import Path
import pandas as pd
from django.core.management.base import BaseCommand
from Institutions.models import Region

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        BASE_DIR = Path(__file__).resolve().parents[3]
        file_path = BASE_DIR / "data" / "imports" / "regions.xlsx"

        df = pd.read_excel(file_path)
        df.columns = df.columns.str.lower().str.replace(" ", "_")

        for _, row in df.iterrows():
            Region.objects.create(
                region_name=row["region_name"],
                region_code=row["region_code"],
            )

        self.stdout.write(self.style.SUCCESS("Regions imported successfully"))