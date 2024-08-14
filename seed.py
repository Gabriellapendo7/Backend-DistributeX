#!/usr/bin/env python3
# seed.py
# Standard library imports
from random import choice as rc
from random import randint

from app import commit_session, get_or_create_category
from config import app, db
from faker import Faker
from flask_bcrypt import Bcrypt
from helpers import dollar_to_cents
from models import Order, OrderDetail, Product, ProductCategory, User
from sqlalchemy.exc import IntegrityError, NoResultFound

products_data = [{
  "name": "Oysters - Smoked",
  "imageSrc": "http://dummyimage.com/125x100.png/dddddd/000000",
  "imageAlt": "Leannon, Bogan and Yost",
  "category_name": "Standardized Grass Pollen, Bluegrass, Kentucky (June)"
}, {
  "name": "Sage Ground Wiberg",
  "imageSrc": "http://dummyimage.com/163x100.png/5fa2dd/ffffff",
  "imageAlt": "Hintz Inc",
  "category_name": "Loratadine"
}, {
  "name": "Bread - Flat Bread",
  "imageSrc": "http://dummyimage.com/136x100.png/cc0000/ffffff",
  "imageAlt": "Klein, Hammes and Toy",
  "category_name": "Bismuth subsalicylate"
}, {
  "name": "Ice Cream Bar - Oreo Cone",
  "imageSrc": "http://dummyimage.com/246x100.png/cc0000/ffffff",
  "imageAlt": "Daugherty, Sawayn and Nicolas",
  "category_name": "Penicillin V Potassium"
}, {
  "name": "Beans - Long, Chinese",
  "imageSrc": "http://dummyimage.com/129x100.png/cc0000/ffffff",
  "imageAlt": "Considine-Gerlach",
  "category_name": "lorazepam"
}, {
  "name": "Pike - Frozen Fillet",
  "imageSrc": "http://dummyimage.com/117x100.png/ff4444/ffffff",
  "imageAlt": "Johnston and Sons",
  "category_name": "lacosamide"
}, {
  "name": "Beer - Upper Canada Light",
  "imageSrc": "http://dummyimage.com/215x100.png/ff4444/ffffff",
  "imageAlt": "Gutmann, Pfeffer and Jaskolski",
  "category_name": "Sodium Fluoride"
}, {
  "name": "Cup - 3.5oz, Foam",
  "imageSrc": "http://dummyimage.com/227x100.png/5fa2dd/ffffff",
  "imageAlt": "Jakubowski, Huels and Nikolaus",
  "category_name": "Dicyclomine Hydrochloride"
}, {
  "name": "Venison - Denver Leg Boneless",
  "imageSrc": "http://dummyimage.com/199x100.png/cc0000/ffffff",
  "imageAlt": "Emmerich LLC",
  "category_name": "West Cottonwood"
}, {
  "name": "Extract - Almond",
  "imageSrc": "http://dummyimage.com/167x100.png/dddddd/000000",
  "imageAlt": "Stanton, Hilll and Hettinger",
  "category_name": "VALPROIC ACID"
}, {
  "name": "Pate - Liver",
  "imageSrc": "http://dummyimage.com/120x100.png/5fa2dd/ffffff",
  "imageAlt": "Kreiger, Beahan and Hilll",
  "category_name": "Arnica e pl. tota 3"
}, {
  "name": "Swiss Chard - Red",
  "imageSrc": "http://dummyimage.com/157x100.png/ff4444/ffffff",
  "imageAlt": "Labadie, Kuhn and Johns",
  "category_name": "itanium dioxide, Octinoxate, Octisalate, Zinc Oxide"
}, {
  "name": "Tray - Foam, Square 4 - S",
  "imageSrc": "http://dummyimage.com/223x100.png/ff4444/ffffff",
  "imageAlt": "Jacobson, Jenkins and Funk",
  "category_name": "Tomato"
}, {
  "name": "Cheese - Woolwich Goat, Log",
  "imageSrc": "http://dummyimage.com/127x100.png/ff4444/ffffff",
  "imageAlt": "Frami, Johns and Grimes",
  "category_name": "cyclosporine"
}, {
  "name": "Seedlings - Clamshell",
  "imageSrc": "http://dummyimage.com/130x100.png/ff4444/ffffff",
  "imageAlt": "Rolfson-Schultz",
  "category_name": "HYDROQUINONE"
}, {
  "name": "Lemonade - Kiwi, 591 Ml",
  "imageSrc": "http://dummyimage.com/134x100.png/dddddd/000000",
  "imageAlt": "Davis, Kuhlman and Sporer",
  "category_name": "dextromethorphan hydrobromide, brompheniramine maleate, phenylephrine hydrochloride"
}, {
  "name": "Pasta - Fettuccine, Egg, Fresh",
  "imageSrc": "http://dummyimage.com/159x100.png/cc0000/ffffff",
  "imageAlt": "Emmerich-Hessel",
  "category_name": "MENTHOL"
}, {
  "name": "Goat - Leg",
  "imageSrc": "http://dummyimage.com/175x100.png/5fa2dd/ffffff",
  "imageAlt": "Gottlieb, Lesch and Bruen",
  "category_name": "Aesculus hippocastanum, Arnica montana, Bellis perennis, Bryonia, Calcarea carbonica, Calcarea fluorica, Cimicifuga racemosa, Cobaltum metallicum, Gnaphalium polycephalum, Hypericum perforatum, Kali carbonicum, Kali phosphoricum, Magnesia phosphorica, Oxalicum acidum, Phosphorus, Rhus toxicodendron, Ruta graveolens, Zincum metallicum"
}, {
  "name": "Bar Mix - Lime",
  "imageSrc": "http://dummyimage.com/119x100.png/cc0000/ffffff",
  "imageAlt": "Windler LLC",
  "category_name": "Clarithromycin"
}, {
  "name": "Tea - Herbal Sweet Dreams",
  "imageSrc": "http://dummyimage.com/131x100.png/ff4444/ffffff",
  "imageAlt": "Farrell-Hegmann",
  "category_name": "PANAX GINSENG WHOLE"
}, {
  "name": "Wine - White, Chardonnay",
  "imageSrc": "http://dummyimage.com/215x100.png/dddddd/000000",
  "imageAlt": "Schultz, Schultz and Bode",
  "category_name": "chlorhexidine gluconate"
}, {
  "name": "Wine - Magnotta, White",
  "imageSrc": "http://dummyimage.com/220x100.png/cc0000/ffffff",
  "imageAlt": "Schneider, Kassulke and Jerde",
  "category_name": "Benzocaine"
}, {
  "name": "Grapefruit - Pink",
  "imageSrc": "http://dummyimage.com/145x100.png/5fa2dd/ffffff",
  "imageAlt": "Sipes-Gottlieb",
  "category_name": "ISOPROPYL ALCOHOL"
}, {
  "name": "Sloe Gin - Mcguinness",
  "imageSrc": "http://dummyimage.com/155x100.png/ff4444/ffffff",
  "imageAlt": "Schultz, Dietrich and Shields",
  "category_name": "Acetaminophen, Chlorpheniramine Maleate, Dextromethorphan Hydrobromide, Phenylephrine Hydrochloride"
}, {
  "name": "Flower - Commercial Spider",
  "imageSrc": "http://dummyimage.com/195x100.png/dddddd/000000",
  "imageAlt": "Kulas, Ward and Yundt",
  "category_name": "Metformin Hydrochloride"
}, {
  "name": "Lobak",
  "imageSrc": "http://dummyimage.com/130x100.png/5fa2dd/ffffff",
  "imageAlt": "Balistreri-Bogan",
  "category_name": "mineral oil, petrolatum, phenylephrine HCl"
}, {
  "name": "Wine - Red, Mosaic Zweigelt",
  "imageSrc": "http://dummyimage.com/194x100.png/5fa2dd/ffffff",
  "imageAlt": "Kemmer-Howe",
  "category_name": "Enalapril Maleate"
}, {
  "name": "Milk - 2% 250 Ml",
  "imageSrc": "http://dummyimage.com/213x100.png/cc0000/ffffff",
  "imageAlt": "Ullrich and Sons",
  "category_name": "Anacardium orientale, Antimon.crud., Arg. nit., Berber. vulg., Bryonia, Chelidonium majus, Digitalis, Graphites, Humulus,Iris versicolor, Kali carb., Lycopodium, Nat. carb.,Nat. sulphuricum, Nux vom., Pulsatilla, Rhus. toxicodendron, Scutellaria lateriflora, Sepia,Stramonium, Chamomilla, Passiflora, Valeriana."
}, {
  "name": "Icecream - Dstk Cml And Fdg",
  "imageSrc": "http://dummyimage.com/247x100.png/ff4444/ffffff",
  "imageAlt": "Pagac Inc",
  "category_name": "Diphenhydramine HCl"
}, {
  "name": "Pork - Ham, Virginia",
  "imageSrc": "http://dummyimage.com/147x100.png/cc0000/ffffff",
  "imageAlt": "Purdy, Nitzsche and Berge",
  "category_name": "Alcohol"
}, {
  "name": "Soup - Campbells Bean Medley",
  "imageSrc": "http://dummyimage.com/236x100.png/5fa2dd/ffffff",
  "imageAlt": "Kuhic, Wunsch and McKenzie",
  "category_name": "Cetirizine Hydrochloride"
}, {
  "name": "Initation Crab Meat",
  "imageSrc": "http://dummyimage.com/167x100.png/ff4444/ffffff",
  "imageAlt": "Prosacco, Runolfsson and Gottlieb",
  "category_name": "Naproxen"
}, {
  "name": "Godiva White Chocolate",
  "imageSrc": "http://dummyimage.com/122x100.png/ff4444/ffffff",
  "imageAlt": "Legros and Sons",
  "category_name": "diphenoxylate hydrochloride and atropine sulfate"
}, {
  "name": "Vinegar - Balsamic",
  "imageSrc": "http://dummyimage.com/167x100.png/ff4444/ffffff",
  "imageAlt": "Gerhold, Vandervort and Koelpin",
  "category_name": "Nystatin"
}, {
  "name": "Bread - Calabrese Baguette",
  "imageSrc": "http://dummyimage.com/153x100.png/dddddd/000000",
  "imageAlt": "Kassulke-Auer",
  "category_name": "Octinoxate and Oxybenzone"
}, {
  "name": "Wine - Red, Concha Y Toro",
  "imageSrc": "http://dummyimage.com/230x100.png/ff4444/ffffff",
  "imageAlt": "O'Reilly-Strosin",
  "category_name": "ZINC OXIDE"
}, {
  "name": "Bay Leaf",
  "imageSrc": "http://dummyimage.com/170x100.png/ff4444/ffffff",
  "imageAlt": "Fahey-Crist",
  "category_name": "Conium maculatum 6X, Graphites 12X, Sulphur 12X"
}, {
  "name": "Tuna - Bluefin",
  "imageSrc": "http://dummyimage.com/149x100.png/5fa2dd/ffffff",
  "imageAlt": "Huels, Braun and Champlin",
  "category_name": "triazolam"
}, {
  "name": "Barley - Pearl",
  "imageSrc": "http://dummyimage.com/114x100.png/5fa2dd/ffffff",
  "imageAlt": "Abshire-Keeling",
  "category_name": "Nicotine Polacrilex"
}, {
  "name": "Bread - Wheat Baguette",
  "imageSrc": "http://dummyimage.com/170x100.png/ff4444/ffffff",
  "imageAlt": "Koepp Inc",
  "category_name": "Nicotine Polacrilex"
}, {
  "name": "Tomatoes - Cherry",
  "imageSrc": "http://dummyimage.com/192x100.png/dddddd/000000",
  "imageAlt": "Daniel-Cruickshank",
  "category_name": "CANDIDA ALBICANS"
}, {
  "name": "Chickensplit Half",
  "imageSrc": "http://dummyimage.com/141x100.png/5fa2dd/ffffff",
  "imageAlt": "Hoeger Group",
  "category_name": "Benzalkonium Chloride"
}, {
  "name": "Turnip - White",
  "imageSrc": "http://dummyimage.com/123x100.png/ff4444/ffffff",
  "imageAlt": "Beahan-Batz",
  "category_name": "Dimethicone"
}, {
  "name": "Pastry - Mini French Pastries",
  "imageSrc": "http://dummyimage.com/131x100.png/5fa2dd/ffffff",
  "imageAlt": "Hegmann, Dickinson and Wisozk",
  "category_name": "Octinoxate, Titanium Dioxide, Zinc Oxide"
}, {
  "name": "Pasta - Gnocchi, Potato",
  "imageSrc": "http://dummyimage.com/127x100.png/ff4444/ffffff",
  "imageAlt": "Abbott, Schoen and Kunze",
  "category_name": "Triclosan"
}, {
  "name": "Energy Drink - Franks Original",
  "imageSrc": "http://dummyimage.com/249x100.png/dddddd/000000",
  "imageAlt": "Glover LLC",
  "category_name": "CLOTRIMAZOLE"
}, {
  "name": "Plasticforkblack",
  "imageSrc": "http://dummyimage.com/250x100.png/dddddd/000000",
  "imageAlt": "Dickinson, Yundt and Sawayn",
  "category_name": "ARNICA MONTANA"
}, {
  "name": "Wine - Manischewitz Concord",
  "imageSrc": "http://dummyimage.com/163x100.png/dddddd/000000",
  "imageAlt": "Nitzsche, Kuhlman and Romaguera",
  "category_name": "Sun Total Protector Color 30 Dark Tint"
}, {
  "name": "Coffee Guatemala Dark",
  "imageSrc": "http://dummyimage.com/248x100.png/5fa2dd/ffffff",
  "imageAlt": "Hyatt-Welch",
  "category_name": "Antiperspirant and Deodorant"
}, {
  "name": "Island Oasis - Ice Cream Mix",
  "imageSrc": "http://dummyimage.com/167x100.png/5fa2dd/ffffff",
  "imageAlt": "O'Keefe-Hermiston",
  "category_name": "Nicotine Polacrilex"
}, {
  "name": "Kellogs Raisan Bran Bars",
  "imageSrc": "http://dummyimage.com/163x100.png/5fa2dd/ffffff",
  "imageAlt": "Murazik, Howell and Dach",
  "category_name": "Quetiapine Fumarate"
}, {
  "name": "Duck - Whole",
  "imageSrc": "http://dummyimage.com/121x100.png/5fa2dd/ffffff",
  "imageAlt": "McGlynn-Turcotte",
  "category_name": "menthol"
}, {
  "name": "Veal - Tenderloin, Untrimmed",
  "imageSrc": "http://dummyimage.com/214x100.png/ff4444/ffffff",
  "imageAlt": "Senger, Braun and Rice",
  "category_name": "cilostazol"
}, {
  "name": "Chocolate - Milk, Callets",
  "imageSrc": "http://dummyimage.com/201x100.png/ff4444/ffffff",
  "imageAlt": "Sporer and Sons",
  "category_name": "Lovastatin"
}, {
  "name": "Soup - Cream Of Broccoli, Dry",
  "imageSrc": "http://dummyimage.com/164x100.png/ff4444/ffffff",
  "imageAlt": "Keeling-Heaney",
  "category_name": "Hydrocortisone, Iodoquinol"
}, {
  "name": "Cheese - Mozzarella",
  "imageSrc": "http://dummyimage.com/148x100.png/5fa2dd/ffffff",
  "imageAlt": "Mayert-Hettinger",
  "category_name": "ZINC OXIDE"
}, {
  "name": "Pasta - Shells, Medium, Dry",
  "imageSrc": "http://dummyimage.com/171x100.png/ff4444/ffffff",
  "imageAlt": "Streich-Farrell",
  "category_name": "LISINOPRIL"
}, {
  "name": "Tart Shells - Barquettes, Savory",
  "imageSrc": "http://dummyimage.com/182x100.png/cc0000/ffffff",
  "imageAlt": "Moore-Muller",
  "category_name": "nitroglycerin"
}, {
  "name": "Olives - Nicoise",
  "imageSrc": "http://dummyimage.com/191x100.png/ff4444/ffffff",
  "imageAlt": "Smith-Bahringer",
  "category_name": "CISplatin"
}, {
  "name": "Catfish - Fillets",
  "imageSrc": "http://dummyimage.com/184x100.png/ff4444/ffffff",
  "imageAlt": "Sauer Inc",
  "category_name": "Acetaminophen, Dextromethorphan Hydrobromide, Phenylephrine Hydrochloride"
}, {
  "name": "Pop - Club Soda Can",
  "imageSrc": "http://dummyimage.com/191x100.png/cc0000/ffffff",
  "imageAlt": "Olson-Runolfsson",
  "category_name": "OCTINOXATE, TITANIUM DIOXIDE, and ZINC OXIDE"
}, {
  "name": "Orange Roughy 4/6 Oz",
  "imageSrc": "http://dummyimage.com/236x100.png/5fa2dd/ffffff",
  "imageAlt": "Kunze, Stoltenberg and Schultz",
  "category_name": "Guaifenesin"
}, {
  "name": "Butter - Salted",
  "imageSrc": "http://dummyimage.com/138x100.png/dddddd/000000",
  "imageAlt": "Weimann Group",
  "category_name": "ixabepilone"
}, {
  "name": "Wasabi Paste",
  "imageSrc": "http://dummyimage.com/232x100.png/5fa2dd/ffffff",
  "imageAlt": "Crist-Runolfsson",
  "category_name": "DAPTOMYCIN"
}, {
  "name": "Veal - Insides, Grains",
  "imageSrc": "http://dummyimage.com/144x100.png/cc0000/ffffff",
  "imageAlt": "Bayer, Douglas and Marks",
  "category_name": "Ascorbic acid, Cholecalciferol, .alpha.-tocopherol acetate, dl-, Thiamine mononitrate, Riboflavin, Niacinamide, Pyridoxine Hydrochloride, Folic Acid, Cyanocobalamin, and Iron"
}, {
  "name": "Squid - Tubes / Tenticles 10/20",
  "imageSrc": "http://dummyimage.com/180x100.png/cc0000/ffffff",
  "imageAlt": "Hayes Group",
  "category_name": "Aluminum hydroxide, Magnesium hydroxide, Simethicone"
}, {
  "name": "Longos - Burritos",
  "imageSrc": "http://dummyimage.com/131x100.png/cc0000/ffffff",
  "imageAlt": "Kozey Group",
  "category_name": "metformin hydrochloride"
}, {
  "name": "Nut - Pine Nuts, Whole",
  "imageSrc": "http://dummyimage.com/219x100.png/ff4444/ffffff",
  "imageAlt": "Oberbrunner Group",
  "category_name": "Bryonia , Cocculus, Gelsemium, Lobelia inf, Acacia gum, lactose, magnesium stearate, corn starch, sucrose"
}, {
  "name": "Appetizer - Sausage Rolls",
  "imageSrc": "http://dummyimage.com/119x100.png/5fa2dd/ffffff",
  "imageAlt": "Shields-Monahan",
  "category_name": "ZINC OXIDE, OCTINOXATE, TITANIUM DIOXIDE, OXYBENZONE"
}, {
  "name": "Tomatoes - Grape",
  "imageSrc": "http://dummyimage.com/203x100.png/cc0000/ffffff",
  "imageAlt": "Bosco-Johnston",
  "category_name": "Abrotanum, Anacardium orientale, Arsenicum album, Baryta muriatica, Helleborus niger, Ignatia amara, Lycopodium clavatum,"
}, {
  "name": "Vaccum Bag 10x13",
  "imageSrc": "http://dummyimage.com/247x100.png/dddddd/000000",
  "imageAlt": "Olson-Goodwin",
  "category_name": "Colloid Oatmeal"
}, {
  "name": "Venison - Racks Frenched",
  "imageSrc": "http://dummyimage.com/128x100.png/ff4444/ffffff",
  "imageAlt": "D'Amore-Jacobi",
  "category_name": "Avobenzone, Homosalate, Octisalate, Octocrylene, and Oxybenzone"
}, {
  "name": "Cheese - Cambozola",
  "imageSrc": "http://dummyimage.com/144x100.png/dddddd/000000",
  "imageAlt": "Williamson Inc",
  "category_name": "Loperamide Hydrochloride"
}, {
  "name": "Foam Tray S2",
  "imageSrc": "http://dummyimage.com/123x100.png/cc0000/ffffff",
  "imageAlt": "Thompson Inc",
  "category_name": "valsartan and hydrochlorothiazide"
}, {
  "name": "Laundry - Bag Cloth",
  "imageSrc": "http://dummyimage.com/131x100.png/dddddd/000000",
  "imageAlt": "Stanton-Reinger",
  "category_name": "metoclopramide"
}, {
  "name": "Chinese Foods - Chicken Wing",
  "imageSrc": "http://dummyimage.com/164x100.png/ff4444/ffffff",
  "imageAlt": "Abernathy-Mohr",
  "category_name": "Salicylic acid"
}, {
  "name": "Steamers White",
  "imageSrc": "http://dummyimage.com/135x100.png/dddddd/000000",
  "imageAlt": "Beier, Wunsch and Jast",
  "category_name": "Gabapentin"
}, {
  "name": "Sloe Gin - Mcguinness",
  "imageSrc": "http://dummyimage.com/103x100.png/ff4444/ffffff",
  "imageAlt": "Zieme Inc",
  "category_name": "zinc oxide, titanium dioxide"
}, {
  "name": "Muffin - Mix - Mango Sour Cherry",
  "imageSrc": "http://dummyimage.com/243x100.png/cc0000/ffffff",
  "imageAlt": "Fisher Group",
  "category_name": "Acetaminophen, Phenylephrine HCl"
}, {
  "name": "Water - Spring 1.5lit",
  "imageSrc": "http://dummyimage.com/171x100.png/5fa2dd/ffffff",
  "imageAlt": "Kshlerin-Rosenbaum",
  "category_name": "ZINC ACETATE ANHYDROUS and ZINC GLUCONATE"
}, {
  "name": "Lettuce - Mini Greens, Whole",
  "imageSrc": "http://dummyimage.com/212x100.png/ff4444/ffffff",
  "imageAlt": "Hodkiewicz-Sporer",
  "category_name": "tranexamic acid"
}, {
  "name": "Rhubarb",
  "imageSrc": "http://dummyimage.com/180x100.png/dddddd/000000",
  "imageAlt": "Schiller, Klocko and Monahan",
  "category_name": "Rabbitbush"
}, {
  "name": "Mangoes",
  "imageSrc": "http://dummyimage.com/144x100.png/dddddd/000000",
  "imageAlt": "Wisoky Group",
  "category_name": "Allantoin 0.5%, Benzethonium Chloride 0.5%"
}, {
  "name": "Bread - Raisin",
  "imageSrc": "http://dummyimage.com/184x100.png/dddddd/000000",
  "imageAlt": "Bergnaum, Reynolds and Effertz",
  "category_name": "Asafoetida, Astragalus Menziesii, Illicium Anisatum, Lonicera Zylosteum"
}, {
  "name": "Fennel - Seeds",
  "imageSrc": "http://dummyimage.com/190x100.png/dddddd/000000",
  "imageAlt": "Ward, Hahn and Carroll",
  "category_name": "CONIUM MACULATUM"
}, {
  "name": "Eggroll",
  "imageSrc": "http://dummyimage.com/145x100.png/ff4444/ffffff",
  "imageAlt": "Farrell, O'Reilly and Corwin",
  "category_name": "Montelukast Sodium"
}, {
  "name": "Wine - Sake",
  "imageSrc": "http://dummyimage.com/130x100.png/cc0000/ffffff",
  "imageAlt": "Volkman and Sons",
  "category_name": "Ash, White Fraxinus americana"
}, {
  "name": "Cakes Assorted",
  "imageSrc": "http://dummyimage.com/116x100.png/dddddd/000000",
  "imageAlt": "White, Walsh and Douglas",
  "category_name": "levothyroxine sodium tablets"
}, {
  "name": "Cake Slab",
  "imageSrc": "http://dummyimage.com/222x100.png/cc0000/ffffff",
  "imageAlt": "Ankunding-Bayer",
  "category_name": "nateglinide"
}, {
  "name": "Crawfish",
  "imageSrc": "http://dummyimage.com/212x100.png/cc0000/ffffff",
  "imageAlt": "Nicolas and Sons",
  "category_name": "ZINC OXIDE"
}, {
  "name": "Garbage Bags - Clear",
  "imageSrc": "http://dummyimage.com/234x100.png/dddddd/000000",
  "imageAlt": "Labadie, MacGyver and Moen",
  "category_name": "Niacinamide"
}, {
  "name": "Tray - Foam, Square 4 - S",
  "imageSrc": "http://dummyimage.com/203x100.png/cc0000/ffffff",
  "imageAlt": "Streich-Herman",
  "category_name": "Oregano"
}, {
  "name": "Beans - Soya Bean",
  "imageSrc": "http://dummyimage.com/125x100.png/5fa2dd/ffffff",
  "imageAlt": "Rau-D'Amore",
  "category_name": "OCTINOXATE, OCTISALATE, AVOBENZONE"
}, {
  "name": "Pepper - Black, Ground",
  "imageSrc": "http://dummyimage.com/114x100.png/dddddd/000000",
  "imageAlt": "Jenkins Inc",
  "category_name": "OXYMORPHONE HYDROCHLORIDE"
}, {
  "name": "Longos - Chicken Curried",
  "imageSrc": "http://dummyimage.com/190x100.png/5fa2dd/ffffff",
  "imageAlt": "Daniel-O'Keefe",
  "category_name": "tizanidine hydrochloride"
}, {
  "name": "Wine - Red, Cooking",
  "imageSrc": "http://dummyimage.com/227x100.png/cc0000/ffffff",
  "imageAlt": "Schaden, Douglas and Huels",
  "category_name": "Isopropyl Alcohol"
}, {
  "name": "Gloves - Goldtouch Disposable",
  "imageSrc": "http://dummyimage.com/196x100.png/cc0000/ffffff",
  "imageAlt": "Effertz Inc",
  "category_name": "Potassium Chloride"
}, {
  "name": "Pastry - Apple Muffins - Mini",
  "imageSrc": "http://dummyimage.com/242x100.png/5fa2dd/ffffff",
  "imageAlt": "Schuppe Inc",
  "category_name": "Propafenone hydrochloride"
}, {
  "name": "Garlic - Peeled",
  "imageSrc": "http://dummyimage.com/112x100.png/dddddd/000000",
  "imageAlt": "Renner, Pagac and Stanton",
  "category_name": "Triclosan"
}, {
  "name": "Pancetta",
  "imageSrc": "http://dummyimage.com/131x100.png/ff4444/ffffff",
  "imageAlt": "Stiedemann Inc",
  "category_name": "TITANIUM DIOXIDE"
}]
fake = Faker()
bcrypt = Bcrypt(app)


def create_fake_orders(num_orders=5):
    for _ in range(num_orders):
        user_id = rc(User.query.all()).id
        order = Order(user_id=user_id)
        db.session.add(order)

    try:
        db.session.commit()
        print(f"Added {num_orders} fake orders.")
    except Exception as e:
        print(f"Error adding orders: {e}")


def create_fake_order_details(num_details=10):
    products = Product.query.all()
    if not products:
        print("No products available to create order details.")
        return

    for _ in range(num_details):
        order_id = rc(Order.query.all()).id
        product_id = rc(products).id
        quantity = randint(1, 5)

        order_detail = OrderDetail(
            order_id=order_id, product_id=product_id, quantity=quantity
        )
        db.session.add(order_detail)

    try:
        db.session.commit()
        print(f"Added {num_details} fake order details.")
    except Exception as e:
        print(f"Error adding order details: {e}")


def create_fake_users(num_users=2):
    for _ in range(num_users):
        try:
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}.{last_name.lower()}"
            email = fake.email()

            existing_user = User.query.filter(
                (User.username == username) | (User.email == email)
            ).first()
            if existing_user:
                continue

            user = User(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                shipping_address=fake.address(),
                shipping_city=fake.city(),
                shipping_state=fake.state(),
                shipping_zip=fake.zipcode(),
                password=bcrypt.generate_password_hash(fake.password()).decode("utf-8"),
            )

            db.session.add(user)
            db.session.commit()
            print(f"Added user: {username}")

        except Exception as e:
            print(f"Error adding user {username}: {e}")
            db.session.rollback()


def add_product_to_categories(product, category_names):
    for name in category_names:
        category = get_or_create_category(name)
        product_category = ProductCategory(product=product, category=category)
        db.session.add(product_category)


def create_fake_products():
    for product_data in products_data:
        product_name = product_data["name"].strip()
        if not product_name:
            product_name = fake.unique.company()

        existing_product = Product.query.filter_by(name=product_name).first()
        if existing_product:
            print(f"Product '{existing_product.name}' already exists. Skipping.")
            continue

        product = Product(
            name=product_name,
            description=fake.text(),
            price=fake.random_int(min=30000, max=150000),
            item_quantity=fake.random_int(min=0, max=50),
            image_url=f"/{product_data['imageSrc']}",
            imageAlt=product_data["imageAlt"],
        )

        category_names = (
            product_data["category_name"]
            if isinstance(product_data["category_name"], list)
            else [product_data["category_name"]]
        )
        add_product_to_categories(product, category_names)

        db.session.add(product)

    try:
        commit_session(db.session)
        print("Products added successfully")
    except IntegrityError as error:
        print(f"Failed to add products. Error: {error}")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_fake_users()
        create_fake_orders()
        create_fake_products()
        create_fake_order_details()
        print("Database seeded successfully!")
