#!/usr/bin/env python3
"""Create lessons 16-56 for the learning platform"""

import json
import os

lessons_data = [
    {
        "id": "16_list_slicing",
        "title": "Liste Dilimleme (Slicing)",
        "order": 16,
        "week": 5,
        "description": "Liste parçalarını almayı öğren",
        "sections": [
            {
                "type": "theory",
                "title": "Liste Dilimleme",
                "content": "Listeden bir kısmını alabilirsin. **liste[başlangıç:bitiş]** şeklinde kullanılır.",
                "examples": [
                    {
                        "title": "Dilimleme Örneği",
                        "explanation": "Liste parçaları alma:",
                        "code": "sayilar = [0, 1, 2, 3, 4, 5]\nprint(sayilar[1:4])  # 1, 2, 3\nprint(sayilar[:3])   # 0, 1, 2\nprint(sayilar[3:])   # 3, 4, 5",
                        "output": "[1, 2, 3]\n[0, 1, 2]\n[3, 4, 5]"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "Dilimleme Egzersizi",
                "exercise": {
                    "id": "slicing",
                    "instructions": "Liste [10, 20, 30, 40, 50] ile başlangıç ve bitiş belirleyerek ortadaki 3 elemanı al",
                    "starter_code": "sayilar = [10, 20, 30, 40, 50]\nprint(sayilar[1:4])",
                    "test_cases": [{"input": "", "expected_output": "[20, 30, 40]"}],
                    "hints": ["Başlangıç indeksi 1", "Bitiş indeksi 4"]
                }
            }
        ]
    },
    {
        "id": "17_dictionaries",
        "title": "Sözlükler (Dictionaries)",
        "order": 17,
        "week": 5,
        "description": "Anahtar-değer çiftleri ile çalışmayı öğren",
        "sections": [
            {
                "type": "theory",
                "title": "Dictionary Nedir?",
                "content": "**Dictionary**, anahtar-değer çiftleri saklar. Küme parantezi **{}** ile oluşturulur.",
                "examples": [
                    {
                        "title": "Dictionary Oluşturma",
                        "explanation": "Kişi bilgileri:",
                        "code": "kisi = {'ad': 'Ahmet', 'yas': 25, 'sehir': 'Istanbul'}\nprint(kisi['ad'])\nprint(kisi['yas'])",
                        "output": "Ahmet\n25"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "Dictionary Egzersizi",
                "exercise": {
                    "id": "dict_basic",
                    "instructions": "Bir kişinin adı, yaşı ve şehri bilgilerini dictionary'de sakla ve yazdır",
                    "starter_code": "ogrenci = {'ad': 'Ali', 'yas': 16, 'sehir': 'Ankara'}\nprint(ogrenci['ad'])\nprint(ogrenci['yas'])\nprint(ogrenci['sehir'])",
                    "test_cases": [{"input": "", "expected_output": "Ali"}],
                    "hints": ["Dictionary küme parantezi ile oluştur", "Değerlere anahtar ile erişim"]
                }
            }
        ]
    },
    {
        "id": "18_functions_intro",
        "title": "Fonksiyonlara Giriş",
        "order": 18,
        "week": 6,
        "description": "Kendi fonksiyonlarını yazacağını öğren",
        "sections": [
            {
                "type": "theory",
                "title": "def ile Fonksiyon Tanımlama",
                "content": "**def** ile yeniden kullanılabilir kod blokları oluşturabilirsin.",
                "examples": [
                    {
                        "title": "Fonksiyon Tanımlama",
                        "explanation": "Selamlama fonksiyonu:",
                        "code": "def selam():\n    print('Merhaba Dünya!')\n\nselam()\nselam()",
                        "output": "Merhaba Dünya!\nMerhaba Dünya!"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "Fonksiyon Egzersizi",
                "exercise": {
                    "id": "func_intro",
                    "instructions": "Bir selamla() fonksiyonu yaz ve iki kez çağır",
                    "starter_code": "def selamla():\n    print('Selam!')\n\nselamla()\nselamla()",
                    "test_cases": [{"input": "", "expected_output": "Selam!"}],
                    "hints": ["def ile fonksiyon tanımla", "Parantez ile çağır"]
                }
            }
        ]
    },
    {
        "id": "19_function_parameters",
        "title": "Fonksiyon Parametreleri",
        "order": 19,
        "week": 6,
        "description": "Fonksiyonlara veri geçirmeyi öğren",
        "sections": [
            {
                "type": "theory",
                "title": "Parametreler ve Argümanlar",
                "content": "Fonksiyonlara veri geçmek için parantez içinde parametreler tanımlarız.",
                "examples": [
                    {
                        "title": "Parametre Örneği",
                        "explanation": "İsim parametresi alan fonksiyon:",
                        "code": "def selamla(ad):\n    print('Merhaba ' + ad)\n\nselamla('Ahmet')\nselamla('Zeynep')",
                        "output": "Merhaba Ahmet\nMerhaba Zeynep"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "Parametre Egzersizi",
                "exercise": {
                    "id": "func_params",
                    "instructions": "İki sayıyı toplayan bir fonksiyon yaz ve sonuç yazdır",
                    "starter_code": "def topla(a, b):\n    sonuc = a + b\n    print(sonuc)\n\ntopla(5, 3)\ntopla(10, 20)",
                    "test_cases": [{"input": "", "expected_output": "8"}],
                    "hints": ["Parametreleri parantez içinde tanımla", "İki parametre kullan"]
                }
            }
        ]
    },
    {
        "id": "20_function_return",
        "title": "return ile Değer Döndürme",
        "order": 20,
        "week": 6,
        "description": "Fonksiyonlardan değer döndürmeyi öğren",
        "sections": [
            {
                "type": "theory",
                "title": "return Kullanımı",
                "content": "**return** ile fonksiyon bir değer geri döndürebilir.",
                "examples": [
                    {
                        "title": "return Örneği",
                        "explanation": "Karenin alanını hesaplayan fonksiyon:",
                        "code": "def kare_alan(kenar):\n    alan = kenar * kenar\n    return alan\n\nsonuc = kare_alan(5)\nprint('5x5 karenin alanı:', sonuc)",
                        "output": "5x5 karenin alanı: 25"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "return Egzersizi",
                "exercise": {
                    "id": "func_return",
                    "instructions": "İki sayıyı çarpan bir fonksiyon yaz ve sonucu return et",
                    "starter_code": "def carp(a, b):\n    return a * b\n\nsonuc = carp(4, 5)\nprint(sonuc)",
                    "test_cases": [{"input": "", "expected_output": "20"}],
                    "hints": ["return ile sonuç döndür", "Sonucu değişkene ata"]
                }
            }
        ]
    },
    {
        "id": "21_tuples",
        "title": "Tuple'lar (Sabit Listeler)",
        "order": 21,
        "week": 6,
        "description": "Değiştirilemez listeler öğren",
        "sections": [
            {
                "type": "theory",
                "title": "Tuple Nedir?",
                "content": "**Tuple**, listeler gibi birden fazla değer saklar ama değiştirilemeyen sabit bir veri tipidir. Normal parantez () ile oluşturulur.",
                "examples": [
                    {
                        "title": "Tuple Oluşturma",
                        "explanation": "Koordinatlar tuple'da sakla:",
                        "code": "koordinat = (10, 20)\nprint(koordinat[0])\nprint(koordinat[1])\n\nrenkler = ('kırmızı', 'yeşil', 'mavi')\nfor renk in renkler:\n    print(renk)",
                        "output": "10\n20\nkırmızı\nyeşil\nmavi"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "Tuple Egzersizi",
                "exercise": {
                    "id": "tuple_basic",
                    "instructions": "Bir tuple oluştur ve elemanlarına eriş",
                    "starter_code": "nokta = (5, 15)\nprint(nokta[0])\nprint(nokta[1])",
                    "test_cases": [{"input": "", "expected_output": "5"}],
                    "hints": ["Tuple normal parantez ile oluştur", "Indeks ile eriş"]
                }
            }
        ]
    },
    {
        "id": "22_sets",
        "title": "Kümeler (Sets)",
        "order": 22,
        "week": 6,
        "description": "Tekrarsız değer koleksiyonları öğren",
        "sections": [
            {
                "type": "theory",
                "title": "Set Nedir?",
                "content": "**Set**, benzersiz (tekrarsız) değerleri saklar. Küme parantezi {} ile oluşturulur ama dictionary farklıdır.",
                "examples": [
                    {
                        "title": "Set Oluşturma",
                        "explanation": "Benzersiz sayılar:",
                        "code": "sayilar = {1, 2, 2, 3, 3, 3}\nprint(sayilar)  # Tekrarlar otomatik silinir\nprint(len(sayilar))",
                        "output": "{1, 2, 3}\n3"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "Set Egzersizi",
                "exercise": {
                    "id": "set_basic",
                    "instructions": "Tekrarlayan sayıları içeren bir set oluştur ve benzersiz sayıları yazdır",
                    "starter_code": "sayilar = {1, 2, 2, 3, 3, 4, 4, 5}\nprint(sayilar)",
                    "test_cases": [{"input": "", "expected_output": "{1, 2, 3, 4, 5}"}],
                    "hints": ["Set {} ile oluştur", "Tekrarlar otomatik silinir"]
                }
            }
        ]
    },
    {
        "id": "23_string_methods",
        "title": "String Metodları",
        "order": 23,
        "week": 7,
        "description": "String ile işlem yapmayı öğren",
        "sections": [
            {
                "type": "theory",
                "title": "String Metodları",
                "content": "Stringler üzerinde işlem yapmak için metodlar kullanırız:\n- **upper()**: Büyük harfe çevir\n- **lower()**: Küçük harfe çevir\n- **capitalize()**: İlk harfi büyüt\n- **replace()**: Değiştir",
                "examples": [
                    {
                        "title": "String Metodları",
                        "explanation": "String işlemleri:",
                        "code": "metin = 'merhaba'\nprint(metin.upper())\nprint(metin.capitalize())\nprint(metin.replace('a', 'o'))",
                        "output": "MERHABA\nMerhaba\nmerhobο"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "String Metodu Egzersizi",
                "exercise": {
                    "id": "string_methods",
                    "instructions": "Bir string'i büyük harfe çevir ve yazdır",
                    "starter_code": "metin = 'python programlama'\nprint(metin.upper())",
                    "test_cases": [{"input": "", "expected_output": "PYTHON PROGRAMLAMA"}],
                    "hints": ["upper() metodunu kullan"]
                }
            }
        ]
    },
    {
        "id": "24_string_split_join",
        "title": "String split() ve join()",
        "order": 24,
        "week": 7,
        "description": "String'leri parçalara ayırıp birleştirmeyi öğren",
        "sections": [
            {
                "type": "theory",
                "title": "split() ve join() Metodları",
                "content": "- **split()**: String'i parça\n- **join()**: Parçaları birleştir",
                "examples": [
                    {
                        "title": "split ve join",
                        "explanation": "String işlemleri:",
                        "code": "cumle = 'Python çok eğlenceli'\nkelimeler = cumle.split()  # Boşluğa göre böl\nprint(kelimeler)\n\nbirlesik = ' '.join(kelimeler)  # Boşlukla birleştir\nprint(birlesik)",
                        "output": "['Python', 'çok', 'eğlenceli']\nPython çok eğlenceli"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "split() Egzersizi",
                "exercise": {
                    "id": "split_join",
                    "instructions": "Bir cümleyi kelimelere böl ve kelime sayısını yazdır",
                    "starter_code": "cumle = 'Python programlama dili'\nkelimeler = cumle.split()\nprint(len(kelimeler))",
                    "test_cases": [{"input": "", "expected_output": "3"}],
                    "hints": ["split() boşluğa göre böler"]
                }
            }
        ]
    },
    {
        "id": "25_file_read",
        "title": "Dosya Okuma",
        "order": 25,
        "week": 7,
        "description": "Dosyalardan veri okumayı öğren",
        "sections": [
            {
                "type": "theory",
                "title": "open() ile Dosya Okuma",
                "content": "- **open()**: Dosya aç\n- **read()**: Dosyanın tamamını oku\n- **close()**: Dosyayı kapat",
                "examples": [
                    {
                        "title": "Dosya Okuma",
                        "explanation": "Dosya okuma örneği:",
                        "code": "dosya = open('ornek.txt', 'r')\nicerik = dosya.read()\nprint(icerik)\ndosya.close()",
                        "output": "Dosyadaki içerik buraya yazılır"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "Dosya Okuma Egzersizi",
                "exercise": {
                    "id": "file_read",
                    "instructions": "Dosya okuma kavramını anla (gerçek dosya işlemi platform'da)",
                    "starter_code": "# Dosya okuma örneği\n# dosya = open('test.txt', 'r')\n# print(dosya.read())\n# dosya.close()\n\nprint('Dosya okuma kavramı anladım')",
                    "test_cases": [{"input": "", "expected_output": "Dosya okuma kavramı anladım"}],
                    "hints": ["open() ile dosya aç", "read() ile içeriği oku", "close() ile kapat"]
                }
            }
        ]
    },
    {
        "id": "26_modules",
        "title": "Modüller (Modules)",
        "order": 26,
        "week": 8,
        "description": "Hazır kodları kullanmayı öğren",
        "sections": [
            {
                "type": "theory",
                "title": "import ile Modül Kullanma",
                "content": "**import** ile Python'un hazır modüllerini kullanabilirsin.\n\nPopüler modüller:\n- **math**: Matematik işlemleri\n- **random**: Rastgele sayılar\n- **time**: Zaman işlemleri",
                "examples": [
                    {
                        "title": "math Modülü",
                        "explanation": "Matematiksel işlemler:",
                        "code": "import math\nprint(math.sqrt(16))  # Karekök\nprint(math.pi)        # Pi sayısı\nprint(math.pow(2, 3)) # 2 üzeri 3",
                        "output": "4.0\n3.141592653589793\n8.0"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "Modül Egzersizi",
                "exercise": {
                    "id": "modules",
                    "instructions": "math modülü kullanarak 25'in karekökünü hesapla",
                    "starter_code": "import math\nsqrt = math.sqrt(25)\nprint(sqrt)",
                    "test_cases": [{"input": "", "expected_output": "5"}],
                    "hints": ["import math ile modülü yükle", "math.sqrt() karekök"]
                }
            }
        ]
    }
]

# Daha fazla ders ekleyelim (26-56)
more_lessons = [
    {"id": "27_random_module", "title": "random Modülü", "order": 27, "week": 8, "description": "Rastgele sayılar ve seçimler"},
    {"id": "28_list_comprehension", "title": "Liste Comprehension", "order": 28, "week": 8, "description": "Listeler oluşturmanın hızlı yolu"},
    {"id": "29_exception_handling", "title": "Hata İşleme (try-except)", "order": 29, "week": 8, "description": "Hataları yakalaması öğren"},
    {"id": "30_datetime_module", "title": "datetime Modülü", "order": 30, "week": 9, "description": "Tarih ve zaman işlemleri"},
    {"id": "31_json_handling", "title": "JSON Verisi", "order": 31, "week": 9, "description": "JSON formatında veri işle"},
    {"id": "32_object_oriented", "title": "Nesne Yönelimli Programlama", "order": 32, "week": 9, "description": "Sınıflar ve nesneler"},
    {"id": "33_classes", "title": "Sınıflar (Classes)", "order": 33, "week": 9, "description": "Kendi sınıflarını oluştur"},
    {"id": "34_inheritance", "title": "Kalıtım (Inheritance)", "order": 34, "week": 10, "description": "Sınıfları miras al"},
    {"id": "35_decorators", "title": "Dekoratörler", "order": 35, "week": 10, "description": "Fonksiyon manipülasyonu"},
    {"id": "36_lambda", "title": "Lambda Fonksiyonları", "order": 36, "week": 10, "description": "Anonim fonksiyonlar"},
    {"id": "37_map_filter", "title": "map() ve filter()", "order": 37, "week": 11, "description": "Fonksiyonel programlama"},
    {"id": "38_sorting", "title": "Sıralama (Sorting)", "order": 38, "week": 11, "description": "Verileri sıralamayı öğren"},
    {"id": "39_searching", "title": "Arama Algoritmaları", "order": 39, "week": 11, "description": "Verilerde arama yap"},
    {"id": "40_turtle_intro", "title": "Turtle Graphics'e Giriş", "order": 40, "week": 12, "description": "Grafik çizim başlangıcı"},
    {"id": "41_turtle_shapes", "title": "Turtle ile Şekiller", "order": 41, "week": 12, "description": "Geometrik şekiller çiz"},
    {"id": "42_turtle_colors", "title": "Turtle Renkleri ve Stilleri", "order": 42, "week": 12, "description": "Renklendirilmiş çizimler"},
    {"id": "43_turtle_loops", "title": "Turtle ile Döngüler", "order": 43, "week": 13, "description": "Tekrarlayan çizimler"},
    {"id": "44_turtle_events", "title": "Turtle Olayları", "order": 44, "week": 13, "description": "Fare ve klavye olayları"},
    {"id": "45_turtle_animation", "title": "Turtle Animasyon", "order": 45, "week": 13, "description": "Hareket eden çizimler"},
    {"id": "46_turtle_collision", "title": "Turtle Çarpışma Tespiti", "order": 46, "week": 14, "description": "Nesneler arasında çarpışma"},
    {"id": "47_game_basics", "title": "Oyun Geliştirme Temelleri", "order": 47, "week": 14, "description": "Basit oyun yapısı"},
    {"id": "48_snake_game", "title": "Yılan Oyunu Projesi", "order": 48, "week": 14, "description": "Yılan oyununu yap"},
    {"id": "49_pong_game", "title": "Pong Oyunu Projesi", "order": 49, "week": 15, "description": "Pong oyununu yap"},
    {"id": "50_memory_game", "title": "Hafıza Oyunu", "order": 50, "week": 15, "description": "Bellek oyunu yap"},
    {"id": "51_web_requests", "title": "Web İstekleri (requests)", "order": 51, "week": 15, "description": "İnternetten veri al"},
    {"id": "52_api_integration", "title": "API Entegrasyonu", "order": 52, "week": 15, "description": "API'lerle çalış"},
    {"id": "53_final_project_1", "title": "Final Projesi - Kalkülator", "order": 53, "week": 16, "description": "Gelişmiş kalkülator yap"},
    {"id": "54_final_project_2", "title": "Final Projesi - Hava Durumu", "order": 54, "week": 16, "description": "Hava durumu uygulaması"},
    {"id": "55_best_practices", "title": "En İyi Pratikler", "order": 55, "week": 16, "description": "Profesyonel kod yazımı"},
    {"id": "56_next_steps", "title": "Sonraki Adımlar", "order": 56, "week": 16, "description": "Python sonrasında ne yapmalı"}
]

# İlk 10 ders için detaylı veriler oluştur
for lesson in lessons_data:
    section = {
        "type": "practice",
        "title": f"{lesson['id'].replace('_', ' ').title()} Egzersizi",
        "exercise": {
            "id": f"{lesson['id']}_practice",
            "instructions": f"{lesson['description'].lower()} pratiği yapın",
            "starter_code": "print('Egzersiz alanı')",
            "test_cases": [{"input": "", "expected_output": "Egzersiz"}],
            "hints": ["Adımları takip et", "Konsolu kontrol et"]
        }
    }
    lesson.get("sections", []).append(section)

# Kalan dersler için basit yapı oluştur
for lesson in more_lessons:
    lesson.update({
        "sections": [
            {
                "type": "theory",
                "title": lesson["title"],
                "content": lesson["description"],
                "examples": [
                    {
                        "title": "Örnek",
                        "explanation": "Bu konuyu daha sonra öğreneceksiniz",
                        "code": "# Örnek kod\npass",
                        "output": "Başarılı"
                    }
                ]
            },
            {
                "type": "practice",
                "title": f"{lesson['title']} Egzersizi",
                "exercise": {
                    "id": f"{lesson['id']}_ex",
                    "instructions": f"{lesson['description'].lower()} egzersizi",
                    "starter_code": "print('Egzersiz yapıyorum')",
                    "test_cases": [{"input": "", "expected_output": "Egzersiz"}],
                    "hints": ["Öğrendikleri uygula"]
                }
            }
        ]
    })

all_lessons = lessons_data + more_lessons

# Oluştur
lessons_dir = 'backend/data/lessons'
os.makedirs(lessons_dir, exist_ok=True)

for lesson in all_lessons:
    filename = f"{lessons_dir}/{lesson['id']}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(lesson, f, ensure_ascii=False, indent=2)
    print(f"Olusturuldu: {lesson['order']} - {lesson['title']}")

print(f"\nToplam {len(all_lessons)} ders olusturuldu!")
