from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('product', '0002_departamento_district_province_product_departamento_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS product_departamento (
                id BIGSERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL
            );
            """
        ),
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS product_province (
                id BIGSERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL
            );
            """
        ),
        migrations.RunSQL(
            "ALTER TABLE product_product ADD COLUMN IF NOT EXISTS departamento VARCHAR(100);"
        ),
        migrations.RunSQL(
            "ALTER TABLE product_product ADD COLUMN IF NOT EXISTS provincia VARCHAR(100);"
        ),
        migrations.RunSQL(
            "ALTER TABLE product_product ADD COLUMN IF NOT EXISTS distrito VARCHAR(100);"
        ),
    ] 