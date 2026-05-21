# Ders-al-ma-Disiplini-Analiz-Sistemi
OpenCV ve MediaPipe tabanlı, çalışma duruşunu analiz eden ve disiplin yüzdesini hesaplayan gerçek zamanlı takip sistemi.
1. Amaç  

Günümüz uzaktan eğitim süreçlerinde öğrencilerin çalışma disiplinini korumaları ve odaklanma sürelerini artırmaları önemli bir zorluktur. Bu projenin temel amacı, bilgisayar başında geçirilen sürenin verimliliğini takip eden, kullanıcıya anlık geri bildirimler sunan ve çalışma disiplinini istatistiksel bir yüzde ile raporlayan özgün bir "Akıllı Disiplin Takip Sistemi" geliştirmektir. Sistem, insan-bilgisayar etkileşimi prensiplerini kullanarak, kullanıcının duruş bozukluklarını (ayağa kalkma) veya masadan uzaklaşma durumlarını tespit ederek çalışma verimliliğini optimize etmeyi hedefler. 

 
2. Kullanılan Yöntem  

Yöntem: Proje kapsamında görüntü işleme teknikleri kullanılmıştır. Yazılım dili olarak Python, görüntü işleme süreçleri için OpenCV kütüphanesi, iskelet tespiti ve analiz süreçleri için ise MediaPipe kütüphanesi tercih edilmiştir. 

Veri Alımı: Sistem, bilgisayar kamerası (webcam) üzerinden gerçek zamanlı görüntü akışı almaktadır. 

İskelet Analizi: MediaPipe Pose modeli kullanılarak, kullanıcının vücudundaki 33 kritik nokta (landmark) sürekli izlenmektedir. 

Duruş Tespiti: Kişinin oturma veya ayakta olma durumu, omuz (11, 12) ve kalça (23, 24) noktalarının dikey (y) koordinatları karşılaştırılarak belirlenmiştir. Belirlenen eşik değerleri (MESAFE_ESIK ve OMUZ_Y_ESIK) sayesinde sistem, kullanıcının fiziksel konumuyla uyumlu çalışacak şekilde kalibre edilmiştir. 

Zaman ve Verimlilik Analizi: Sistemin çalıştığı toplam süre ile kullanıcının aktif çalışma (oturma) süresi time kütüphanesi ile anlık olarak tutulmuş ve "Disiplin Yüzdesi" formülize edilmiştir. 

 
3. Elde Edilen Sonuçlar  

Elde Edilen Sonuçlar: Yapılan testler sonucunda sistemin, öğrencinin çalışma disiplinini yüksek doğrulukla analiz ettiği görülmüştür: 

Canlı Geri Bildirim: Sistem, kişi masadan uzaklaştığında veya ayağa kalktığında anlık uyarılar vererek kullanıcıyı tekrar çalışma pozisyonuna yönlendirmiştir. 

Veri Raporlama: 's' tuşu ile tetiklenen "Ders Çalışma Raporu" ekranı sayesinde, öğrenci toplam çalışma süresini ve disiplin başarısını bir özetiyle görüntüleyebilmektedir. 

Performans: OpenCV ve MediaPipe entegrasyonu sayesinde sistem, düşük donanımlı cihazlarda bile yüksek kare hızıyla (FPS) çalışabilmekte ve gerçek zamanlı analiz kriterini tam olarak karşılamaktadır. Proje, görüntü üzerinden veri analizi yaparak, disiplin takibini otomatikleştirilmiş ve dijital bir boyuta taşımıştır. 
