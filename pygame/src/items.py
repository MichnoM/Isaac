magic_mushroom = "magic mushroom", ["max_health", "health", "damage", "damage_multiplier", "range", "speed", "size"], [1, 1, 0.3, 0.5, 5.25, 3, 1]
sad_onion = "sad onion", ["attack_speed"], [7]
pentagram = "pentagram", ["damage"], [1]
lunch = "lunch", ["max_health", "health"], [1, 1]
breakfast = "breakfast", ["max_health", "health"], [1, 1]
dinner = "dinner", ["max_health", "health"], [1, 1]
halo = "the halo", ["max_health", "health", "damage", "attack_speed", "range", "speed"], [1, 1, 0.3, 2, 0.25, 3]
quarter = "a quarter", ["coins"], [25]
cat_o_nine_tails = "cat-o-nine-tails", ["damage", "shot_speed"], [1, 0.23]
meat = "meat!", ["max_health", "health", "damage"], [1, 1, 0.3]
toothpicks = "toothpicks", ["attack_speed", "shot_speed"], [7, 0.16]
stem_cells = "stem cells", ["max_health", "health", "shot_speed"], [1, 1, 0.16]
wire_coat_hanger = "wire coat hanger", ["attack_speed"], [7]
roid_rage = "roid rage", ["speed", "range"], [6, 5.25]
yum = "<3", ["max_health", "health"], [1, 1]
boom = "boom!", ["bombs"], [10]
dessert = "dessert", ["max_health", "health"], [1, 1]
rotten_meat = "rotten meat", ["max_health", "health"], [1, 1]
wooden_spoon = "wooden spoon", ["speed"], [3]
the_belt = "the belt", ["speed"], [3]
mom_heels = "mom's heels", ["range"], [5.25]
mom_lipstick = "mom's lipstick", ["range"], [5.25]
growth_hormones = "growth hormones", ["damage", "speed"], [1, 4]
bucket_of_lard = "bucket of lard", ["max_health"], [2]
speed_ball = "speed ball", ["speed", "shot_speed"], [3, 0.2]
synthoil = "synthoil", ["damage", "range"], [1, 5.25]
snack = "a snack", ["max_health", "health"], [1, 1]

item_list = [
    pentagram, magic_mushroom, sad_onion, lunch, breakfast, dinner, halo, quarter, cat_o_nine_tails,
    meat, toothpicks, stem_cells, wire_coat_hanger, roid_rage, yum, boom, dessert, rotten_meat,
    wooden_spoon, the_belt, mom_heels, mom_lipstick, growth_hormones, bucket_of_lard, speed_ball,
    synthoil, snack
    ]

moms_key = "mom's key", ["keys"], [2] # doubles the pickups spawn
piggy_bank = "piggy bank", ["coins"], [3] # when taking damage, spawn 1-2 coins
steam_sale = "steam sale", [""], [""] # shop prices -50%
bogo_bombs = "bogo bombs", [""], [""] # all bomb pickups are now doubled

shop_items = [moms_key, piggy_bank, steam_sale, bogo_bombs]

heart_container = "heart", ["health"], [1]
key = "key", ["keys"], [1]
bomb = "bomb", ["bombs"], [1]
coin = "coin", ["coins"], [1]

pickup_list = [heart_container, key, bomb, coin]