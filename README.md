# Undangan Pernikahan Online — Edisi Newspaper

Halaman undangan pernikahan satu file (`index.html`) berformat **koran broadsheet multi-lembar** (*The Wedding News*): sampul depan terlipat (*Folded Newsstand Cover*) dengan label alamat tamu & stempel pos, navigasi indeks seksi koran (*sticky section bar*), **Sheet I — Front Page** (*masthead* dengan *ear boxes* lokasi & *weather forecast*, *headline* `BREAKING NEWS — GETTING MARRIED`, *lead article* dengan *drop cap* & kutipan ayat, stempel *Save the Date*, dan hitung mundur), **Sheet II — Society & Feature** (profil mempelai 2 kolom, *Stories from Their Families*, *The Journey of Us* 2 kolom + *Milestones Along the Way*, serta statistik perjalanan), **Sheet III — Schedule & Etiquette** (*Order of the Day*, *dispatch* Akad & Resepsi dengan peta & kalender Google/Apple `.ics`, *Dress Code*, dan *Live Streaming* opsional), **Sheet IV — Photo Essay & Leisure** (galeri *contact-sheet* + *lightbox*, mini-game *Wedding Word Search* interaktif, kotak *Capture & Share*, dan *Fun Facts*), **Sheet V — Classifieds & Guestbook** (*Wedding Gift* bergaya iklan baris, kupon gunting *Tear-Off RSVP Slip*, dan *Letters to the Couple*), serta **Back Page** penutup.

## Cara mengubah isi
Buka `index.html`, cari objek `CONFIG` di bagian `<script>`, lalu ubah:

- **Identitas koran**: `paperTitle`, `kickerMast`, `issue`, `city`, `venueShort`, `forecast`, `hashtag`, `heroCaption`, dan `frontLead`.
- **Mempelai & keluarga**: `bride`, `groom`, `brideFirst`, `date`, dan `familyQuotes` (kutipan keluarga di Sheet II; kosongkan array untuk menyembunyikan).
- **Acara**: `events` (Akad Nikah & Resepsi), `timeline` (*Order of the Day*), `dressCode`, dan `stream` (`null` untuk menyembunyikan).
- **Love Story, Fun Facts & Puzzle**: `story` (tiap item memiliki `date`, `title`, `summary` untuk kolom *Milestones*, dan `text` untuk artikel 2 kolom), `stats`, `funFacts`, dan `puzzle` (`null` untuk menyembunyikan *Wedding Word Search*).
- **Foto**: taruh file di folder `img/`, lalu isi path-nya di `photos`, `bride.photo`, `groom.photo`, `events[i].photo`, dan `gallery`.
- **Musik**: taruh file `.mp3` di folder `audio/`, lalu isi `music` dan `musicTitle`. Jika kosong, pemutar musik otomatis disembunyikan.
- **Nama tamu / kirim undangan**: buka `/kirim` untuk membuat link personal (`/?to=Nama+Tamu`) dan mengirim langsung lewat WhatsApp. Nama tamu tampil di label alamat sampul depan dan otomatis terisi di kupon RSVP.
- **Ucapan untuk semua tamu**: tanpa backend, ucapan tersimpan di `localStorage` browser tamu. Pasang `apps-script.gs` di Google Sheets (langkah lengkap ada di bagian atas file itu), lalu tempel Web App URL-nya ke `CONFIG.rsvpEndpoint`.

## Hosting
Langsung deploy ke Vercel, Netlify, atau GitHub Pages tanpa proses build.
