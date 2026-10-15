"""Genera una demostración animada del alta de lavados, sin usar datos reales."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "public" / "guia-crear-lavado.gif"
FONT_DIR = Path("C:/Windows/Fonts")
REGULAR = FONT_DIR / "segoeui.ttf"
BOLD = FONT_DIR / "segoeuib.ttf"
W, H = 1200, 700


def font(size, bold=False):
    return ImageFont.truetype(str(BOLD if bold else REGULAR), size)


def rounded(draw, box, fill, radius=12, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def label(draw, xy, value, size=18, color="#254252", bold=False):
    draw.text(xy, value, font=font(size, bold), fill=color)


def field(draw, x, y, width, title, value, active=False, cursor=False):
    label(draw, (x, y), title, 15, "#526773", True)
    box = (x, y + 23, x + width, y + 70)
    rounded(draw, box, "#ffffff", 8, "#07877e" if active else "#bed0d4", 3 if active else 1)
    if value:
        label(draw, (x + 13, y + 32), value, 19, "#163947", True)
    else:
        label(draw, (x + 13, y + 32), "Seleccionar...", 18, "#9aaab0")
    if cursor:
        text_width = draw.textbbox((0, 0), value, font=font(19, True))[2]
        draw.line((x + 14 + text_width, y + 34, x + 14 + text_width, y + 55), fill="#07877e", width=2)


def pointer(draw, x, y):
    draw.polygon([(x, y), (x + 2, y + 27), (x + 8, y + 20), (x + 15, y + 34),
                  (x + 20, y + 31), (x + 13, y + 17), (x + 23, y + 15)],
                 fill="#173947", outline="white")
    draw.ellipse((x + 17, y + 27, x + 28, y + 38), outline="#07877e", width=2)


STEPS = [
    ("Cliente y auto", "Escribí la chapa y la marca o modelo."),
    ("Lavador", "Seleccioná a quien realizará el trabajo."),
    ("Grupo Auto", "Filtrá los servicios por grupo Auto."),
    ("Servicio", "Elegí el servicio y revisá el precio."),
    ("Guardar", "Guardá y confirmá el resumen."),
]


def frame(step, phase):
    image = Image.new("RGB", (W, H), "#edf3f4")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 93), fill="#103b4b")
    rounded(draw, (37, 28, 76, 66), "#0ca095", 10)
    label(draw, (49, 30), "L", 25, "white", True)
    label(draw, (91, 25), "CREAR UN LAVADO", 27, "white", True)
    label(draw, (92, 59), "Demostración · datos de ejemplo", 14, "#c7e6e3")
    rounded(draw, (937, 27, 1159, 66), "#225767", 19)
    label(draw, (964, 34), f"PASO {step + 1} DE 5", 16, "white", True)

    for index, (name, _) in enumerate(STEPS):
        x = 46 + index * 231
        selected = index == step
        completed = index < step
        color = "#07877e" if selected or completed else "#d7e2e4"
        rounded(draw, (x, 115, x + 216, 121), color, 3)
        label(draw, (x, 129), f"{index + 1:02d}  {name}", 15,
              "#086c66" if selected else "#758791", selected)

    rounded(draw, (38, 177, 796, 658), "#ffffff", 18, "#d6e3e6")
    label(draw, (67, 196), "Nuevo lavado", 25, "#183c48", True)
    draw.line((67, 236, 768, 236), fill="#e3ebed", width=2)
    label(draw, (67, 253), "CLIENTE RÁPIDO", 14, "#087f78", True)

    chapa = ""
    modelo = ""
    if step == 0:
        chapa = ["A", "ABC 123", "ABC 123"][min(phase, 2)]
        modelo = "Toyota Corolla" if phase >= 2 else ""
    else:
        chapa, modelo = "ABC 123", "Toyota Corolla"
    field(draw, 67, 279, 325, "Chapa", chapa, step == 0 and phase < 2, step == 0 and phase < 2)
    field(draw, 414, 279, 344, "Marca / modelo", modelo, step == 0 and phase >= 2, step == 0 and phase == 2)

    label(draw, (67, 374), "PERSONAL", 14, "#087f78", True)
    selected_personal = step > 1 or step == 1 and phase >= 1
    rounded(draw, (67, 401, 255, 445), "#e1f5f1" if selected_personal else "#ffffff",
            8, "#07877e" if step == 1 or selected_personal else "#bed0d4", 2 if step == 1 else 1)
    label(draw, (91, 409), "Juan Pérez", 18, "#076c64" if selected_personal else "#344f5b", True)

    label(draw, (67, 463), "SERVICIOS", 14, "#087f78", True)
    selected_group = step > 2 or step == 2 and phase >= 1
    rounded(draw, (67, 492, 185, 535), "#e1f5f1" if selected_group else "#ffffff",
            8, "#07877e" if step == 2 or selected_group else "#bed0d4", 2 if step == 2 else 1)
    label(draw, (101, 499), "Auto", 18, "#076c64" if selected_group else "#344f5b", True)
    rounded(draw, (195, 492, 317, 535), "#ffffff", 8, "#d2dfe2")
    label(draw, (224, 499), "Moto", 18, "#84959e")

    service = "Lavado completo" if step > 3 or step == 3 and phase >= 1 else ""
    field(draw, 67, 552, 493, "Servicio", service, step == 3)
    field(draw, 575, 552, 183, "Precio", "Gs. 60.000" if service else "", step == 3 and phase >= 2)

    rounded(draw, (827, 177, 1162, 658), "#ffffff", 18, "#d6e3e6")
    label(draw, (857, 207), f"{step + 1:02d} / 05", 16, "#087f78", True)
    label(draw, (857, 246), STEPS[step][0], 29, "#183c48", True)
    label(draw, (857, 299), STEPS[step][1], 18, "#526773")
    if step == 0:
        label(draw, (857, 383), "1. Chapa: ABC 123", 17, "#526773")
        label(draw, (857, 413), "2. Modelo: Toyota Corolla", 17, "#526773")
        pointer(draw, 576 if phase >= 2 else 205, 340)
    elif step == 1:
        label(draw, (857, 383), "Personal: Juan Pérez", 17, "#526773")
        pointer(draw, 192, 415)
    elif step == 2:
        label(draw, (857, 383), "Grupo: Auto", 17, "#526773")
        pointer(draw, 144, 511)
    elif step == 3:
        label(draw, (857, 383), "Servicio: Lavado completo", 17, "#526773")
        label(draw, (857, 413), "Total: Gs. 60.000", 17, "#526773")
        pointer(draw, 345 if phase < 2 else 687, 598)
    else:
        rounded(draw, (853, 364, 1136, 543), "#f1f8f7", 12, "#b7dcda")
        label(draw, (875, 383), "Confirmar nuevo lavado", 19, "#183c48", True)
        label(draw, (875, 420), "ABC 123 · Toyota Corolla", 16)
        label(draw, (875, 447), "Juan Pérez · Lavado completo", 16)
        label(draw, (875, 474), "Total: Gs. 60.000", 16, "#087f78", True)
        rounded(draw, (875, 504, 945, 532), "#087f78" if phase >= 2 else "#bdd8d5", 6)
        label(draw, (898, 506), "SI", 16, "white", True)
        pointer(draw, 924, 516)

    if step == 4:
        rounded(draw, (67, 617, 758, 648), "#087f78", 7)
        label(draw, (349, 619), "Guardar lavado", 16, "white", True)
    return image


def main():
    frames = []
    durations = []
    for step in range(5):
        for phase in range(3):
            frames.append(frame(step, phase).quantize(colors=128, method=Image.Quantize.MEDIANCUT))
            durations.append(600 if phase < 2 else 1100)
    durations[-1] = 1800
    frames[0].save(OUTPUT, save_all=True, append_images=frames[1:], duration=durations,
                   loop=0, optimize=True, disposal=2)
    print(OUTPUT)


if __name__ == "__main__":
    main()
