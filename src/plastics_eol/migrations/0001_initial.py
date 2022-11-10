# Generated by Django 4.1.3 on 2022-11-09 15:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Scenario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField(default=django.utils.timezone.now)),
                ("name", models.TextField()),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReExportedPlastic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ethylene", models.FloatField(default=0.0)),
                ("vinyl_chloride", models.FloatField(default=0.0)),
                ("styrene", models.FloatField(default=0.0)),
                ("other", models.FloatField(default=0.0)),
                (
                    "scenario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="plastics_eol.scenario",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PlasticReportedRecycled",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pet", models.FloatField(default=0.0)),
                ("hdpe", models.FloatField(default=0.0)),
                ("pvc", models.FloatField(default=0.0)),
                ("ldpe", models.FloatField(default=0.0)),
                ("pal", models.FloatField(default=0.0)),
                ("pp", models.FloatField(default=0.0)),
                ("ps", models.FloatField(default=0.0)),
                ("other", models.FloatField(default=0.0)),
                (
                    "scenario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="plastics_eol.scenario",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PlasticRecycling",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pet", models.FloatField(default=0.0)),
                ("hdpe", models.FloatField(default=0.0)),
                ("pvc", models.FloatField(default=0.0)),
                ("ldpe", models.FloatField(default=0.0)),
                ("pal", models.FloatField(default=0.0)),
                ("pp", models.FloatField(default=0.0)),
                ("ps", models.FloatField(default=0.0)),
                ("other", models.FloatField(default=0.0)),
                (
                    "scenario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="plastics_eol.scenario",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PlasticLandfill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pet", models.FloatField(default=0.0)),
                ("hdpe", models.FloatField(default=0.0)),
                ("pvc", models.FloatField(default=0.0)),
                ("ldpe", models.FloatField(default=0.0)),
                ("pal", models.FloatField(default=0.0)),
                ("pp", models.FloatField(default=0.0)),
                ("ps", models.FloatField(default=0.0)),
                ("other", models.FloatField(default=0.0)),
                (
                    "scenario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="plastics_eol.scenario",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PlasticIncineration",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pet", models.FloatField(default=0.0)),
                ("hdpe", models.FloatField(default=0.0)),
                ("pvc", models.FloatField(default=0.0)),
                ("ldpe", models.FloatField(default=0.0)),
                ("pal", models.FloatField(default=0.0)),
                ("pp", models.FloatField(default=0.0)),
                ("ps", models.FloatField(default=0.0)),
                ("other", models.FloatField(default=0.0)),
                (
                    "scenario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="plastics_eol.scenario",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MSWRecycling",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("inorganic", models.FloatField(default=0.0)),
                ("other", models.FloatField(default=0.0)),
                ("yard_trimmings", models.FloatField(default=0.0)),
                ("food", models.FloatField(default=0.0)),
                ("rubber_leather_textiles", models.FloatField(default=0.0)),
                ("wood", models.FloatField(default=0.0)),
                ("metals", models.FloatField(default=0.0)),
                ("glass", models.FloatField(default=0.0)),
                ("paper", models.FloatField(default=0.0)),
                ("plastics", models.FloatField(default=0.0)),
                ("total_mass", models.FloatField(default=0.0)),
                (
                    "scenario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="plastics_eol.scenario",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MSWLandfill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("inorganic", models.FloatField(default=0.0)),
                ("other", models.FloatField(default=0.0)),
                ("yard_trimmings", models.FloatField(default=0.0)),
                ("food", models.FloatField(default=0.0)),
                ("rubber_leather_textiles", models.FloatField(default=0.0)),
                ("wood", models.FloatField(default=0.0)),
                ("metals", models.FloatField(default=0.0)),
                ("glass", models.FloatField(default=0.0)),
                ("paper", models.FloatField(default=0.0)),
                ("plastics", models.FloatField(default=0.0)),
                ("total_mass", models.FloatField(default=0.0)),
                (
                    "scenario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="plastics_eol.scenario",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MSWIncineration",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("inorganic", models.FloatField(default=0.0)),
                ("other", models.FloatField(default=0.0)),
                ("yard_trimmings", models.FloatField(default=0.0)),
                ("food", models.FloatField(default=0.0)),
                ("rubber_leather_textiles", models.FloatField(default=0.0)),
                ("wood", models.FloatField(default=0.0)),
                ("metals", models.FloatField(default=0.0)),
                ("glass", models.FloatField(default=0.0)),
                ("paper", models.FloatField(default=0.0)),
                ("plastics", models.FloatField(default=0.0)),
                ("total_mass", models.FloatField(default=0.0)),
                (
                    "scenario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="plastics_eol.scenario",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MSWCompost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("inorganic", models.FloatField(default=0.0)),
                ("other", models.FloatField(default=0.0)),
                ("yard_trimmings", models.FloatField(default=0.0)),
                ("food", models.FloatField(default=0.0)),
                ("rubber_leather_textiles", models.FloatField(default=0.0)),
                ("wood", models.FloatField(default=0.0)),
                ("metals", models.FloatField(default=0.0)),
                ("glass", models.FloatField(default=0.0)),
                ("paper", models.FloatField(default=0.0)),
                ("plastics", models.FloatField(default=0.0)),
                ("total_mass", models.FloatField(default=0.0)),
                (
                    "scenario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="plastics_eol.scenario",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MSWComposition",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("inorganic", models.FloatField(default=0.0)),
                ("other", models.FloatField(default=0.0)),
                ("yard_trimmings", models.FloatField(default=0.0)),
                ("food", models.FloatField(default=0.0)),
                ("rubber_leather_textiles", models.FloatField(default=0.0)),
                ("wood", models.FloatField(default=0.0)),
                ("metals", models.FloatField(default=0.0)),
                ("glass", models.FloatField(default=0.0)),
                ("paper", models.FloatField(default=0.0)),
                ("plastics", models.FloatField(default=0.0)),
                (
                    "scenario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="plastics_eol.scenario",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ImportedPlastic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ethylene", models.FloatField(default=0.0)),
                ("vinyl_chloride", models.FloatField(default=0.0)),
                ("styrene", models.FloatField(default=0.0)),
                ("other", models.FloatField(default=0.0)),
                (
                    "scenario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="plastics_eol.scenario",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ExportedPlastic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ethylene", models.FloatField(default=0.0)),
                ("vinyl_chloride", models.FloatField(default=0.0)),
                ("styrene", models.FloatField(default=0.0)),
                ("other", models.FloatField(default=0.0)),
                (
                    "scenario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="plastics_eol.scenario",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Condition",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("total_msw", models.FloatField(default=0.0)),
                ("total_waste", models.FloatField(default=0.0)),
                ("total_recyc", models.FloatField(default=0.0)),
                ("domestic_recyc", models.FloatField(default=0.0)),
                ("export", models.FloatField(default=0.0)),
                ("re_export", models.FloatField(default=0.0)),
                ("recyc_efficiency", models.FloatField(default=0.0)),
                ("incinerated", models.FloatField(default=0.0)),
                ("landfilled", models.FloatField(default=0.0)),
                ("waste_facility_emissions", models.FloatField(default=0.0)),
                ("landfill_emissions", models.FloatField(default=0.0)),
                (
                    "scenario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="plastics_eol.scenario",
                    ),
                ),
            ],
        ),
    ]