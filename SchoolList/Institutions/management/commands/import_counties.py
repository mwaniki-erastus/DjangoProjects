from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction

from Institutions.models import County, Region   # ← Import Region too


class Command(BaseCommand):
    help = "Import counties from Excel file"

    def handle(self, *args, **kwargs):
        BASE_DIR = Path(__file__).resolve().parents[3]
        file_path = BASE_DIR / "data" / "imports" / "counties.xlsx"

        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        # Read the Excel file (force string dtype to avoid type guessing issues)
        df = pd.read_excel(
            file_path,
            dtype=str,                    # Read everything as string first
            engine='openpyxl'             # Explicit engine (good for .xlsx)
        )

        # Clean column names
        df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

        # Check required columns exist
        required_cols = {"county_name", "county_code", "region_code"}
        if not required_cols.issubset(df.columns):
            missing = required_cols - set(df.columns)
            self.stdout.write(self.style.ERROR(f"Missing columns: {missing}"))
            return

        # Build a cache of Region objects (much faster than querying inside the loop)
        region_cache = {str(region.id): region for region in Region.objects.all()}

        created_count = 0
        skipped = 0

        with transaction.atomic():   # Makes the whole import atomic (faster + safer)
            for _, row in df.iterrows():
                region_id_str = str(row["region_code"]).strip()

                if region_id_str not in region_cache:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Skipping row: Region with ID '{region_id_str}' not found "
                            f"(County: {row.get('county_name', 'N/A')})"
                        )
                    )
                    skipped += 1
                    continue

                try:
                    County.objects.create(
                        county_name=row["county_name"].strip(),
                        county_code=row["county_code"].strip(),
                        region_code=region_cache[region_id_str],   # Pass the Region instance
                        # Alternative (faster): region_code_id=region_id_str
                    )
                    created_count += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error creating county {row.get('county_name')}: {e}")
                    )
                    skipped += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import completed! Created: {created_count} | Skipped: {skipped}"
            )
        )