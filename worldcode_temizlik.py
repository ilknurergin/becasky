import time
from atproto import Client

# --- KULLANICI BİLGİLERİ ---
HANDLE = 'becaecosystem.bsky.social'
PASSWORD = '7w6j-y5b2-rftg-hl5g' # Küçük harf olarak güncellendi

def beca_sky_final_scan():
    client = Client()
    try:
        print("🔑 Giriş yapılıyor...")
        client.login(HANDLE, PASSWORD)
        
        # 1. TAKİPÇİLER (Seni takip edenler)
        follower_dids = set()
        cursor = None
        print("📥 Takipçiler çekiliyor...")
        while True:
            f_resp = client.get_followers(actor=HANDLE, cursor=cursor)
            for f in f_resp.followers:
                follower_dids.add(f.did)
            cursor = f_resp.cursor
            if not cursor: break
            time.sleep(0.3)

        # 2. TAKİP EDİLENLER (Derin Tarama - 3900+ aranıyor)
        following_list = []
        cursor = None
        print("📥 Takip edilenler çekiliyor (Son kişiye kadar)...")
        while True:
            try:
                fg_resp = client.get_follows(actor=HANDLE, cursor=cursor)
                following_list.extend(fg_resp.follows)
                print(f"--- Şu ana kadar {len(following_list)} hesap bulundu...")
                cursor = fg_resp.cursor
                if not cursor: break
                time.sleep(0.3) 
            except Exception as e:
                print(f"⚠️ Sunucu yanıt vermedi, tekrar deneniyor: {e}")
                time.sleep(2)
                continue

        # 3. ANALİZ VE GRUPLAMA
        dostlar = []
        takip_etmeyenler = []

        for user in following_list:
            isim_satiri = f"{user.handle} ({user.display_name or 'İsimsiz'})"
            if user.did in follower_dids:
                dostlar.append(isim_satiri)
            else:
                takip_etmeyenler.append(isim_satiri)

        # 4. DOSYAYA YAZDIRMA
        filename = "FULL_EKOSISTEM_RAPORU.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"--- BECA ECOSYSTEM NİHAİ TARAMA RAPORU ---\n")
            f.write(f"Tarih: {time.ctime()}\n")
            f.write(f"Profilde Görünen Takip Edilen: ~3900\n")
            f.write(f"Kodun Çekebildiği Toplam: {len(following_list)}\n")
            f.write(f"Kayıp/Hayalet Sayısı: {3900 - len(following_list)}\n")
            f.write(f"Toplam Takipçi Sayın: {len(follower_dids)}\n")
            f.write("="*60 + "\n\n")

            f.write(f"❌ SENİ GERİ TAKİP ETMEYENLER ({len(takip_etmeyenler)} Kişi)\n")
            f.write("-" * 40 + "\n")
            for i, isim in enumerate(takip_etmeyenler, 1):
                f.write(f"{i}. {isim}\n")

            f.write("\n\n✅ KARŞILIKLI TAKİPLEŞTİĞİN DOSTLAR ({len(dostlar)} Kişi)\n")
            f.write("-" * 40 + "\n")
            for i, isim in enumerate(dostlar, 1):
                f.write(f"{i}. {isim}\n")

        print(f"\n✨ BAŞARILI! '{filename}' dosyası oluşturuldu.")
        print(f"👉 Şimdi o dosyayı aç ve o hayalet 110 kişinin farkını isim isim incele!")

    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    beca_sky_final_scan()