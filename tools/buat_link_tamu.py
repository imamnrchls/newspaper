"""Buat file Excel daftar tamu (2 sheet): "Daftar Tamu" untuk input + hasil link, dan "Petunjuk".

  python tools/buat_link_tamu.py OUT.xlsx [--contoh "Nama" "08xx"]

Isi nama dan nomor WhatsApp; kolom link undangan dan tombol "Kirim WA" terisi otomatis lewat rumus.
"""
import sys
from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

DOMAIN = "https://contoh-domain.web.id"
ROWS = 500

INK = "161513"
F = "Arial"
HEAD_IN = PatternFill("solid", fgColor=INK)
HEAD_OUT = PatternFill("solid", fgColor="615C53")
INPUT_FILL = PatternFill("solid", fgColor="F5F1E8")
THIN = Side(style="thin", color="C9C1B3")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
BODY = Font(name=F, size=11)


def build(out, example=None):
    wb = Workbook()
    d = wb.active
    d.title = "Daftar Tamu"
    cols = [
        ("No", 6, HEAD_OUT),
        ("Nama Tamu\n(tampil di undangan)", 38, HEAD_IN),
        ("No. WhatsApp", 18, HEAD_IN),
        ("Kategori\n(opsional)", 16, HEAD_IN),
        ("Sudah dikirim?", 14, HEAD_IN),
        ("Kirim WA\n(otomatis)", 14, HEAD_OUT),
        ("No. WA 62\n(otomatis)", 17, HEAD_OUT),
        ("Link Undangan\n(otomatis)", 56, HEAD_OUT),
    ]
    for i, (title, width, fill) in enumerate(cols, 1):
        c = d.cell(row=1, column=i, value=title)
        c.font, c.fill, c.border = Font(name=F, bold=True, color="FFFFFF", size=11), fill, BOX
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        d.column_dimensions[c.column_letter].width = width
    d.row_dimensions[1].height = 34
    d.freeze_panes = "C2"

    for r in range(2, ROWS + 2):
        name = f"TRIM(B{r})"
        enc = (f'SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE({name},"%","%25"),'
               f'"&","%26"),"#","%23"),"+","%2B")," ","+")')
        digits = (f'SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE('
                  f'TRIM(C{r})," ",""),"-",""),".",""),"(",""),")",""),"+","")')
        blank = f'B{r}=""'
        d.cell(row=r, column=1, value=f'=IF({blank},"",ROW()-1)')
        d.cell(row=r, column=6, value=f'=IF({blank},"",HYPERLINK("{DOMAIN}/wa?n="&G{r}&"&to="&{enc},"Kirim WA"))')
        d.cell(row=r, column=7, value=(f'=IF(OR({blank},C{r}=""),"",IF(LEFT({digits},1)="0","62"&MID({digits},2,30),'
                                       f'IF(LEFT({digits},1)="8","62"&{digits},{digits})))'))
        d.cell(row=r, column=8, value=f'=IF({blank},"",HYPERLINK("{DOMAIN}/?to="&{enc},"{DOMAIN}/?to="&{enc}))')
        for col in range(1, 9):
            c = d.cell(row=r, column=col)
            c.font, c.border = BODY, BOX
            if col in (2, 3, 4, 5):
                c.fill = INPUT_FILL
        d.cell(row=r, column=3).number_format = "@"
        d.cell(row=r, column=7).number_format = "@"
        d.cell(row=r, column=6).font = Font(name=F, size=11, bold=True, color="1F6F44", underline="single")
        d.cell(row=r, column=6).alignment = Alignment(horizontal="center")
        d.cell(row=r, column=8).font = Font(name=F, size=10, color=INK, underline="single")

    if example:
        d["B2"], d["C2"], d["D2"] = example[0], example[1], "Uji coba"

    dv = DataValidation(type="textLength", operator="lessThanOrEqual", formula1="80", allow_blank=True,
                        errorTitle="Nama terlalu panjang", error="Nama tamu maksimal 80 karakter.")
    d.add_data_validation(dv)
    dv.add(f"B2:B{ROWS + 1}")
    sent = DataValidation(type="list", formula1='"Ya,Belum"', allow_blank=True)
    d.add_data_validation(sent)
    sent.add(f"E2:E{ROWS + 1}")
    d.conditional_formatting.add(f"A2:H{ROWS + 1}",
                                 FormulaRule(formula=['$E2="Ya"'], fill=PatternFill("solid", fgColor="E2F0E6")))

    p = wb.create_sheet("Petunjuk")
    p.column_dimensions["A"].width = 105
    lines = [
        ("Cara pakai", True),
        ("1. Di sheet 'Daftar Tamu', isi kolom berwarna krem (judul kolom hitam):", False),
        ("     - Nama Tamu: persis seperti yang ingin tampil di undangan, mis. 'Bapak Budi Santoso & Keluarga'.", False),
        ("     - No. WhatsApp: boleh 08xx, +62xx, atau pakai spasi/tanda hubung. Kosongkan jika tidak ada.", False),
        ("     - Kategori: opsional, mis. Keluarga / Kantor / Teman.", False),
        ("2. Kolom berjudul abu-abu terisi otomatis: tombol 'Kirim WA', nomor WA format 62, dan link undangan.", False),
        ("3. Klik 'Kirim WA' untuk membuka WhatsApp dengan pesan yang sudah terisi.", False),
        ("4. Setelah terkirim, pilih 'Ya' di kolom 'Sudah dikirim?'. Baris tamu berubah hijau.", False),
    ]
    for i, (t, bold) in enumerate(lines, 1):
        p.cell(row=i, column=1, value=t).font = Font(name=F, size=11, bold=bold, color=INK if bold else "000000")

    wb.active = 0
    wb.save(out)


if __name__ == "__main__":
    ex = None
    if "--contoh" in sys.argv:
        i = sys.argv.index("--contoh")
        ex = (sys.argv[i + 1], sys.argv[i + 2])
    build(sys.argv[1], ex)
