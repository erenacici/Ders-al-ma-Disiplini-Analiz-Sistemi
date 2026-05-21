import cv2
import mediapipe as mp
import time

# --- KALİBRASYON ALANI ---
# Neden kullandık? Farklı kameralar ve oturuş mesafeleri için kodu yeniden 
# derlemeden, sadece bu değerleri değiştirerek sistemi kolayca kalibre etmek için. 
# oturma değeri 0.53 , ayakta değer 0.75 olduğu için ara değeri kullandık
MESAFE_ESIK = 0.64 
OMUZ_Y_ESIK = 0.30 
# -------------------------

# MediaPipe Pose: İnsan vücudundaki 33 kritik eklem noktasını gerçek zamanlı tespit eden model.
# min_detection_confidence: Modelin "bu bir insandır" demesi için gereken güven eşiği.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(1)
toplam_sure, calisma_suresi = 0, 0
baslangic = time.time()
show_report = False 

print("Sistem çalışıyor.\n's' tuşu: Raporu göster/gizle\n'q' tuşu: Çıkış")

while cap.isOpened():
    success, img = cap.read()
    if not success: break
    
    # Kamera görüntüsünü aynalama: Kullanıcı kendini aynada görüyormuş gibi hissetmesi için (UX/Kullanıcı Deneyimi).
    img = cv2.flip(img, 1)
    
    if not show_report:
        # BGR to RGB: MediaPipe kütüphanesi görüntüleri RGB formatında işlediği için dönüşüm şart.
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(img_rgb)
        
        # Süre hesaplama: Analiz doğruluğu için iki kare arası geçen süreyi (delta time) hesaplıyoruz.
        gecen = time.time() - baslangic
        baslangic = time.time()
        
        durum = "Mola"
        uyari = ""
        
        if results.pose_landmarks:
            # Landmark verileri: 11-12 omuzları, 23-24 kalçayı temsil eder.
            # Oturma/Ayakta olma durumunu ayırt etmek için dikey koordinatları (y) kullanıyoruz.
            lms = results.pose_landmarks.landmark
            omuz_y = (lms[11].y + lms[12].y) / 2
            kalca_y = (lms[23].y + lms[24].y) / 2
            dikey_mesafe = kalca_y - omuz_y
            
            # Mantık: Kişi oturuyorsa omuz ve kalça yakın (dikey_mesafe küçük), ayaktaysa mesafe artar.
            if omuz_y > OMUZ_Y_ESIK and dikey_mesafe < MESAFE_ESIK:
                durum = "Calisiyor"
                calisma_suresi += gecen
            else:
                uyari = "Ayaktasin!"
            toplam_sure += gecen
        else:
            # Kişi kameradan çıkarsa: Hata yerine uyarı vererek etkileşimi yönetiyoruz.
            uyari = "Kisi masadan uzaklasti!"
            toplam_sure += gecen
            
        # Yüzde hesaplama: Toplam sürenin ne kadarında "Çalışıyor" durumunda olunduğu bilgisi.
        yuzde = (calisma_suresi / toplam_sure * 100) if toplam_sure > 0 else 0
        
        # cv2.putText: Analiz sonuçlarını video karesinin üzerine anlık olarak işliyoruz.
        cv2.putText(img, f"Durum: {durum}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img, f"Disiplin: %{int(yuzde)}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        if uyari:
            cv2.putText(img, uyari, (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Rapor ekranı: İstatistiksel verileri kullanıcıya profesyonel bir arayüzle sunmak için.
    else:
        cv2.rectangle(img, (50, 50), (590, 400), (255, 255, 255), -1) # Arka plan temizliği
        cv2.putText(img, "DERS CALISMA RAPORU", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(img, f"Toplam Sure: {int(toplam_sure)} sn", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        cv2.putText(img, f"Calisma Suresi: {int(calisma_suresi)} sn", (100, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        cv2.putText(img, f"Disiplin Yuzdesi: %{int(yuzde)}", (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow("Duruş Analizli Disiplin Sistemi", img)
    
    key = cv2.waitKey(1) & 0xFF
    # 'q' tuşu: Programdan çıkmak için, 's' tuşu: Rapor ekranını açıp kapatmak için kullanılır.
    if key == ord('q'): break
    elif key == ord('s'): show_report = not show_report 

cap.release()
cv2.destroyAllWindows()