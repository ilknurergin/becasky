# --- GİRİŞ BİLGİLERİ ---
HANDLE = 'becaecosystem.bsky.social'  
PASSWORD = '4z3v-advq-dqkd-fro2'       

# --- BEYAZ LİSTE ---
WHITE_LIST = ['bsky.app', 'python.org', 'gemini.google.com']

client = Client()

def beca_operasyonu():
    try:
        print("🚀 Beca Ekosistem Görevlisi Bağlanıyor...")
        client.login(HANDLE, PASSWORD)
        
        print("🔍 Analiz yapılıyor, lütfen bekleyin...")
        
        # Takip ettiklerini çek
        following = []
        cursor = None
        while True:
            res = client.get_follows(actor=HANDLE, cursor=cursor)
            following.extend(res.follows)
            if not res.cursor: break
            cursor = res.cursor

        # Takipçilerini çek
        followers = set()
        cursor = None
        while True:
            res = client.get_followers(actor=HANDLE, cursor=cursor)
            for f in res.followers: followers.add(f.did)
            if not res.cursor: break
            cursor = res.cursor

        # Hainleri bul (Seni takip etmeyenler)
        hainler = [f for f in following if f.did not in followers and f.handle not in WHITE_LIST]

        # --- İMZAN VE EKRAN ÇIKTISI ---
        print("\n" + "="*60)
        print("🌟 BECA EKOSİSTEMİ SOSYAL YÖNETİM ASİSTANI")
        print("beca ekosistem sahibi ilknur ergin tarafından geliştirilmiştir.")
        print("="*60)

        print(f"\n✅ Analiz Tamamlandı!")
        print(f"Toplam Takip Ettiklerin: {len(following)}")
        print(f"Seni Takip Edenler: {len(followers)}")
        print(f"Seni Geri Takip Etmeyen: {len(hainler)}")

        if not hainler:
            print("\nEkosisteminiz tertemiz! İşleme gerek yok.")
            return

        print(f"\n⚠️ KARAR ANI: Bu {len(hainler)} kişiyi 2 saniye arayla silmemi ister misiniz?")
        secim = input("Onaylıyor musunuz? (evet / hayır): ")

        if secim.lower() == 'evet':
            print(f"\n🔥 Operasyon başladı. İnternet kopsa bile sistem bekleyecektir.")
            for index, kisi in enumerate(hainler, 1):
                while True: # İNATÇI DÖNGÜ: İnternet gelene kadar dener
                    try:
                        client.delete_follow(kisi.viewer.following)
                        print(f"[{index}/{len(hainler)}] 🗑️ Silindi: {kisi.handle}")
                        time.sleep(2) # Güvenli bekleme süresi
                        break # Başarılıysa döngüden çık, sıradakine geç
                    except Exception as e:
                        print(f"⚠️ Bağlantı sorunu! 10 saniye sonra tekrar denenecek... (Hata: {e})")
                        time.sleep(10)
            
            print("\n✨ Beca Ekosistem Görevlisi işini başarıyla tamamladı!")
        else:
            print("\nOperasyon iptal edildi. Kimse silinmedi.")

    except Exception as e:
        print(f"❌ Kritik bir hata oluştu: {e}")

if _name_ == "_main_":
    beca_operasyonu()