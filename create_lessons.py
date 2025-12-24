#!/usr/bin/env python3
"""Script to create all 56 lesson files for the Python learning platform"""

import json
import os

lessons_data = [
    {
        "id": "05_input",
        "title": "Input - Kullanıcı Girdisi Alma",
        "order": 5,
        "week": 2,
        "description": "Kullanıcıdan veri almayı öğren",
        "sections": [
            {
                "type": "theory",
                "title": "input() Fonksiyonu",
                "content": "Kullanıcıdan veri almak için **input()** fonksiyonunu kullanırız. input() fonksiyonu daima string (metin) döndürür.",
                "examples": [
                    {
                        "title": "Kullanıcı Girdisi Alma",
                        "explanation": "Basit input() kullanımı:",
                        "code": "ad = input('Adınızı girin: ')\nprint('Merhaba ' + ad)",
                        "output": "Adınızı girin: Ahmet\nMerhaba Ahmet"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "Input Egzersizi",
                "exercise": {
                    "id": "input_practice",
                    "instructions": "Kullanıcıdan ismini al ve ekrana 'Hoş geldiniz İsim!' şeklinde yazdır",
                    "starter_code": "# Kullanıcıdan isim al\nisim = input('Adınız: ')\n\n# Ekrana yazdır",
                    "test_cases": [{"input": "", "expected_output": "Adınız:"}],
                    "hints": ["input() fonksiyonu ile kullanıcıdan veri al", "String birleştirme ile mesaj oluştur", "print() ile sonucu yazdır"]
                }
            }
        ]
    },
    {
        "id": "06_type_conversion",
        "title": "Tür Dönüşümü (Type Conversion)",
        "order": 6,
        "week": 2,
        "description": "Veri tiplerini dönüştürmeyi öğren",
        "sections": [
            {
                "type": "theory",
                "title": "int(), float(), str() Fonksiyonları",
                "content": "input() string döndürür ama matematik yapmak istiyorsak sayıya dönüştürmemiz gerekir.\n\n- **int()**: String'i tam sayıya dönüştür\n- **float()**: String'i ondalık sayıya dönüştür\n- **str()**: Herhangi bir değeri string'e dönüştür",
                "examples": [
                    {
                        "title": "Tür Dönüşümü",
                        "explanation": "String girdisini sayıya dönüştürmek:",
                        "code": "yas_text = input('Yaşınız: ')\nyas = int(yas_text)\n\nprint('Siz ' + str(yas) + ' yaşındasınız')\nprint('5 yıl sonra ' + str(yas + 5) + ' yaşında olacaksınız')",
                        "output": "Yaşınız: 15\nSiz 15 yaşındasınız\n5 yıl sonra 20 yaşında olacaksınız"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "Yaş Hesaplama",
                "exercise": {
                    "id": "age_calc",
                    "instructions": "Kullanıcıdan yaşını al (string olarak gelir), tam sayıya dönüştür ve 10 yıl sonraki yaşını hesapla",
                    "starter_code": "yas = input('Yaşınız: ')\n\n# Tam sayıya dönüştür\n\n# 10 yıl sonraki yaş\n\n# Sonucu yazdır",
                    "test_cases": [{"input": "", "expected_output": "Yaşınız:"}],
                    "hints": ["int() ile string'i sayıya dönüştür", "Dönüştürülen değeri başka değişkene ata", "Yaşa 10 ekle ve yazdır"]
                }
            }
        ]
    },
    {
        "id": "07_if_statement",
        "title": "If (Eğer) İfadeleri",
        "order": 7,
        "week": 3,
        "description": "Koşullu komutları öğren",
        "sections": [
            {
                "type": "theory",
                "title": "if İfadesi",
                "content": "**if** ile belirli bir koşul doğru ise kodu çalıştırabilirsin.\n\nYaygın karşılaştırma operatörleri:\n- **==** : Eşit mi?\n- **!=** : Eşit değil mi?\n- **>** : Büyük mü?\n- **<** : Küçük mü?\n- **>=** : Büyük veya eşit mi?\n- **<=** : Küçük veya eşit mi?",
                "examples": [
                    {
                        "title": "if Örneği",
                        "explanation": "Basit if ifadesi:",
                        "code": "yas = 15\n\nif yas >= 18:\n    print('Yetişkinsiniz')\nelse:\n    print('Reşit değilsiniz')",
                        "output": "Reşit değilsiniz"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "Yaş Kontrolü",
                "exercise": {
                    "id": "age_check",
                    "instructions": "Kullanıcıdan yaşını al. Eğer 18 veya daha büyükse 'Yetişkinsiniz' yazdır, değilse 'Reşit değilsiniz' yazdır",
                    "starter_code": "yas = int(input('Yaşınız: '))\n\nif yas >= 18:\n    print('Yetişkinsiniz')\nelse:\n    print('Reşit değilsiniz')",
                    "test_cases": [{"input": "", "expected_output": "Yaşınız:"}],
                    "hints": ["input() ile yaş al", "int() ile dönüştür", ">= operatörü kullan"]
                }
            }
        ]
    },
    {
        "id": "08_elif",
        "title": "elif (Başka Eğer) İfadeleri",
        "order": 8,
        "week": 3,
        "description": "Birden fazla koşulu kontrol etmeyi öğren",
        "sections": [
            {
                "type": "theory",
                "title": "elif ve else",
                "content": "- **if**: İlk koşulu kontrol et\n- **elif**: İf yanlışsa, başka bir koşulu kontrol et\n- **else**: Tüm koşullar yanlışsa bunu çalıştır",
                "examples": [
                    {
                        "title": "elif Örneği",
                        "explanation": "Not sınıflandırması:",
                        "code": "not_ = 85\n\nif not_ >= 90:\n    print('A')\nelif not_ >= 80:\n    print('B')\nelif not_ >= 70:\n    print('C')\nelse:\n    print('F')",
                        "output": "B"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "Not Sınıflandırması",
                "exercise": {
                    "id": "grade_classify",
                    "instructions": "Kullanıcıdan not al. 90-100: A, 80-89: B, 70-79: C, <70: F yazdır",
                    "starter_code": "not_ = int(input('Notunuz: '))\n\nif not_ >= 90:\n    print('A')\nelif not_ >= 80:\n    print('B')\nelif not_ >= 70:\n    print('C')\nelse:\n    print('F')",
                    "test_cases": [{"input": "", "expected_output": "Notunuz:"}],
                    "hints": ["elif ile çoklu koşul kontrol et", "Sıra önemli - en büyük koşuldan başla", ">= operatörü kullan"]
                }
            }
        ]
    },
    {
        "id": "09_logical_operators",
        "title": "Mantıksal Operatörler (and, or, not)",
        "order": 9,
        "week": 3,
        "description": "Birden fazla koşulu birleştirmeyi öğren",
        "sections": [
            {
                "type": "theory",
                "title": "and, or, not Operatörleri",
                "content": "- **and**: HER İKİ koşul da doğru ise True\n- **or**: HERHANGI BİRİ koşul doğru ise True\n- **not**: Koşulu tersine çevir",
                "examples": [
                    {
                        "title": "and Operatörü",
                        "explanation": "Her iki koşul da sağlanmalı:",
                        "code": "yas = 15\n\nif yas >= 13 and yas < 20:\n    print('Genç')\nelse:\n    print('Genç değil')",
                        "output": "Genç"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "Mantıksal Operatör Egzersizi",
                "exercise": {
                    "id": "logical_ops",
                    "instructions": "Kullanıcıdan yaş ve para miktarı al. Eğer yaş 18 ve para 100 ve üstüyse 'Evet' yazdır, değilse 'Hayır' yazdır",
                    "starter_code": "yas = int(input('Yaş: '))\npara = int(input('Para: '))\n\nif yas >= 18 and para >= 100:\n    print('Evet')\nelse:\n    print('Hayır')",
                    "test_cases": [{"input": "", "expected_output": "Yaş:"}],
                    "hints": ["and operatörü ile iki koşulu birleştir", "Parantez kullanarak açıklık sağla"]
                }
            }
        ]
    },
    {
        "id": "10_while_loop",
        "title": "While Döngüsü",
        "order": 10,
        "week": 4,
        "description": "Tekrarlayan kod yazacağını öğren",
        "sections": [
            {
                "type": "theory",
                "title": "while İfadesi",
                "content": "**while** döngüsü, bir koşul doğru olduğu sürece kodu tekrarlar.",
                "examples": [
                    {
                        "title": "while Döngüsü",
                        "explanation": "1'den 5'e kadar yazdır:",
                        "code": "i = 1\nwhile i <= 5:\n    print(i)\n    i = i + 1",
                        "output": "1\n2\n3\n4\n5"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "1'den 10'a Kadar Yazdırma",
                "exercise": {
                    "id": "while_1_to_10",
                    "instructions": "while döngüsü ile 1'den 10'a kadar sayıları yazdır",
                    "starter_code": "i = 1\nwhile i <= 10:\n    print(i)\n    i = i + 1",
                    "test_cases": [{"input": "", "expected_output": "1"}],
                    "hints": ["i = 1 ile başla", "Koşulu i <= 10 yap", "i = i + 1 ile artır"]
                }
            }
        ]
    },
    {
        "id": "11_for_loop",
        "title": "For Döngüsü",
        "order": 11,
        "week": 4,
        "description": "range() ile döngüleri öğren",
        "sections": [
            {
                "type": "theory",
                "title": "for ve range()",
                "content": "**for** döngüsü, **range()** ile tanımlı sayılar kadar tekrar eder.\n\n- **range(5)**: 0, 1, 2, 3, 4\n- **range(1, 6)**: 1, 2, 3, 4, 5\n- **range(0, 10, 2)**: 0, 2, 4, 6, 8",
                "examples": [
                    {
                        "title": "for Döngüsü",
                        "explanation": "for ile 1'den 5'e kadar:",
                        "code": "for i in range(1, 6):\n    print(i)",
                        "output": "1\n2\n3\n4\n5"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "for Döngüsü Egzersizi",
                "exercise": {
                    "id": "for_loop_practice",
                    "instructions": "for döngüsü ile 0'dan 9'a kadar sayıları yazdır",
                    "starter_code": "for i in range(10):\n    print(i)",
                    "test_cases": [{"input": "", "expected_output": "0"}],
                    "hints": ["range(10) 0'dan 9'a kadar sayıları verir", "range() içinde sayıları tanımla"]
                }
            }
        ]
    },
    {
        "id": "12_nested_loops",
        "title": "İç İçe Döngüler",
        "order": 12,
        "week": 4,
        "description": "Döngüleri iç içe kullanmayı öğren",
        "sections": [
            {
                "type": "theory",
                "title": "Nested Loops",
                "content": "Döngü içinde döngü oluşturabilirsin. İç döngü, dış döngünün her bir adımında komple çalışır.",
                "examples": [
                    {
                        "title": "İç İçe Döngü",
                        "explanation": "3x3 kare çizmek:",
                        "code": "for i in range(3):\n    for j in range(3):\n        print('*', end=' ')\n    print()",
                        "output": "* * * \n* * * \n* * *"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "Döngü Deseni",
                "exercise": {
                    "id": "nested_loops",
                    "instructions": "İç içe döngü ile 4x4 yıldız deseni çiz",
                    "starter_code": "for i in range(4):\n    for j in range(4):\n        print('*', end=' ')\n    print()",
                    "test_cases": [{"input": "", "expected_output": "*"}],
                    "hints": ["Dış döngü satır sayısı", "İç döngü sütun sayısı", "print('', end=' ') aynı satırda yazdırır"]
                }
            }
        ]
    },
    {
        "id": "13_break_continue",
        "title": "break ve continue",
        "order": 13,
        "week": 4,
        "description": "Döngü akışını kontrol etmeyi öğren",
        "sections": [
            {
                "type": "theory",
                "title": "break ve continue Komutları",
                "content": "- **break**: Döngüyü tamamen durdurun\n- **continue**: Şu adımı atlayın ve sonrakine geçin",
                "examples": [
                    {
                        "title": "break Örneği",
                        "explanation": "5 bulunca dur:",
                        "code": "for i in range(1, 11):\n    if i == 5:\n        break\n    print(i)",
                        "output": "1\n2\n3\n4"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "break ve continue Egzersizi",
                "exercise": {
                    "id": "break_continue",
                    "instructions": "1'den 10'a kadar, ama 5'i atla ve 8'de dur",
                    "starter_code": "for i in range(1, 11):\n    if i == 5:\n        continue\n    if i == 8:\n        break\n    print(i)",
                    "test_cases": [{"input": "", "expected_output": "1"}],
                    "hints": ["continue ile atla", "break ile döngüyü sonlandır"]
                }
            }
        ]
    },
    {
        "id": "14_lists",
        "title": "Listeler (Lists)",
        "order": 14,
        "week": 5,
        "description": "Birden fazla değeri bir yerde saklamayı öğren",
        "sections": [
            {
                "type": "theory",
                "title": "Liste Nedir?",
                "content": "**Liste**, birden fazla değeri bir değişkende saklar. Köşeli parantez **[]** ile oluşturulur.",
                "examples": [
                    {
                        "title": "Liste Oluşturma",
                        "explanation": "Liste oluşturma ve erişme:",
                        "code": "renkler = ['kırmızı', 'yeşil', 'mavi']\n\nprint(renkler[0])  # İlk öğe\nprint(renkler[1])  # İkinci öğe\nprint(renkler[2])  # Üçüncü öğe",
                        "output": "kırmızı\nyeşil\nmavi"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "Liste Egzersizi",
                "exercise": {
                    "id": "lists_basic",
                    "instructions": "İçinde 3 meyve adı olan bir liste oluştur ve hepsini yazdır",
                    "starter_code": "meyveler = ['elma', 'armut', 'muz']\n\nprint(meyveler[0])\nprint(meyveler[1])\nprint(meyveler[2])",
                    "test_cases": [{"input": "", "expected_output": "elma"}],
                    "hints": ["Liste köşeli parantez ile oluştur", "Öğelere index ile erişim: liste[0], liste[1]"]
                }
            }
        ]
    },
    {
        "id": "15_list_operations",
        "title": "Liste Operasyonları",
        "order": 15,
        "week": 5,
        "description": "Listelerle işlem yapmayı öğren",
        "sections": [
            {
                "type": "theory",
                "title": "append, len, for ile Listeler",
                "content": "- **append()**: Listeye yeni öğe ekle\n- **len()**: Listedeki eleman sayısını öğren\n- **for**: Listedeki her öğeyi döngü ile işle",
                "examples": [
                    {
                        "title": "Liste İşlemleri",
                        "explanation": "Listeyi kullanma:",
                        "code": "sayilar = [1, 2, 3]\nsayilar.append(4)\nsayilar.append(5)\n\nprint('Sayılar:', sayilar)\nprint('Toplam:', len(sayilar))\n\nfor sayi in sayilar:\n    print(sayi)",
                        "output": "Sayılar: [1, 2, 3, 4, 5]\nToplam: 5\n1\n2\n3\n4\n5"
                    }
                ]
            },
            {
                "type": "practice",
                "title": "Liste İşlem Egzersizi",
                "exercise": {
                    "id": "list_operations",
                    "instructions": "Boş bir liste oluştur, 5 sayı ekle, hepsini yazdır",
                    "starter_code": "sayilar = []\nsayilar.append(10)\nsayilar.append(20)\nsayilar.append(30)\nsayilar.append(40)\nsayilar.append(50)\n\nfor sayi in sayilar:\n    print(sayi)",
                    "test_cases": [{"input": "", "expected_output": "10"}],
                    "hints": ["append() ile ekle", "for ile döngü yap"]
                }
            }
        ]
    }
]

# Create lessons directory if it doesn't exist
lessons_dir = 'backend/data/lessons'
os.makedirs(lessons_dir, exist_ok=True)

# Write all lessons
for lesson in lessons_data:
    filename = f"{lessons_dir}/{lesson['id']}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(lesson, f, ensure_ascii=False, indent=2)
    print(f"Created: {filename}")

print(f"\n✅ {len(lessons_data)} lessons created successfully!")
