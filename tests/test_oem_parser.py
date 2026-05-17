from pathlib import Path

from scripts.comparar_sgp4_oem import cargar_oem, cargar_satelite_desde_tle


def test_cargar_oem_lee_vectores(tmp_path):
    ruta = Path(tmp_path) / "oem.txt"
    ruta.write_text(
        "\n".join(
            [
                "CCSDS_OEM_VERS = 2.0",
                "META_START",
                "OBJECT_NAME = ISS",
                "META_STOP",
                "2026-05-17T10:00:00.000 1.0 2.0 3.0 0.1 0.2 0.3",
                "2026-05-17T10:04:00.000 4.0 5.0 6.0 0.4 0.5 0.6",
            ]
        ),
        encoding="utf-8",
    )

    df = cargar_oem(ruta)

    assert len(df) == 2
    assert list(df.columns) == [
        "fecha_hora",
        "oem_x_km",
        "oem_y_km",
        "oem_z_km",
        "oem_vx_km_s",
        "oem_vy_km_s",
        "oem_vz_km_s",
    ]
    assert df.loc[0, "oem_x_km"] == 1.0
    assert df.loc[1, "oem_vz_km_s"] == 0.6


def test_cargar_tle_acepta_lineas_en_blanco(tmp_path):
    ruta = Path(tmp_path) / "iss_tle.txt"
    ruta.write_text(
        "\n".join(
            [
                "ISS (ZARYA)",
                "",
                "1 25544U 98067A   26137.35937137  .00004742  00000+0  93391-4 0  9992",
                "",
                "2 25544  51.6321  92.7073 0007563  68.1412 292.0380 15.49241279566972",
            ]
        ),
        encoding="utf-8",
    )

    satelite = cargar_satelite_desde_tle(ruta)

    assert satelite.name == "ISS (ZARYA)"
